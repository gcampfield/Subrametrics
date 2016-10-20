from __future__ import division

from datetime import datetime, timedelta
from Queue import Queue
import fitbit
import json

from config import key, secret, access_token, refresh_token
from dummy_data import dummy_data

time_offset = timedelta(minutes=30)

renderq = Queue()

last = datetime.now()
di = None
df = None

client = fitbit.Fitbit(key, secret,
    access_token=access_token, refresh_token=refresh_token)

def fetch(dummy=False):
    '''fetch heartrate data'''
    if dummy:
        data = dummy_data[:]
    else:
        global last
        raw = client.intraday_time_series('activities/heart', detail_level='1sec')
        with open('data.json', 'w') as f:
            json.dump(raw, f)
        data = raw['activities-heart-intraday']['dataset']

        now = datetime.now()
        def date(t):
            res = datetime.strptime(t, '%H:%M:%S') + time_offset
            return res.replace(year=now.year, month=now.month, day=now.day)

        map(lambda d: d.update({ 'time': date(d['time']) }), data)
        first = data[0]['time']
        one_day = timedelta(days=1)
        map(lambda d: d.update({ 'time': d['time'] + one_day }) if d['time'] < first else None, data)

    if last: data = filter(lambda d: d['time'] > last, data)
    data = filter(lambda d: d['value'] > 50, data)
    if len(data) > 0: last = data[-1]['time']
    print 'Collected data to run until %s.' % (last.strftime('%H:%M:%S'))

    generate_renders(data)

def update(data, now):
    '''update data, removing old points'''
    global di, df
    if di is None and len(data) > 0: di = data.pop(0)
    if df is None and len(data) > 0: df = data.pop(0)

    while df is not None and df['time'] < now:
        di = df
        df = None if len(data) == 0 else data.pop(0)

def calc_wait(data, now):
    '''calculate the time to wait based on the transition between heart rates'''
    data = update(data, now)
    if di is None: return timedelta(seconds=0.8) # default to 75 bpm
    if now < di['time'] or df is None:
        return timedelta(seconds=60/di['value'])

    hi = di['value']
    ti = di['time']

    hf = df['value']
    tf = df['time']

    passed = (now - ti).total_seconds()
    total = (tf - ti).total_seconds()

    wait_seconds = 60 / ((hf - hi) * passed / total + hi)
    return timedelta(seconds=wait_seconds)

def generate_renders(data):
    '''place the points into a queue to be used for rendering'''
    t = datetime.now()
    while len(data) > 0:
        wait = calc_wait(data, t)
        renderq.put((t, wait))
        t += wait
