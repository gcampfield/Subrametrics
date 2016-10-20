from __future__ import division

from datetime import datetime, timedelta
from config import npanels
from utils import darken
import colorsys

start = datetime.now()

def get_color(duration):
    '''get color based on the heartrate'''
    time = duration.total_seconds()
    min_hue = 275
    max_hue = 360
    rate = 60 / time
    percent = min(1, max(0, rate - 60) / 60)

    hue = percent * (max_hue - min_hue) + min_hue

    return colorsys.hsv_to_rgb(hue / 360, 1, 1)

def get_rainbow_color(duration):
    '''get color based on the heartrate'''
    hue = ((datetime.now() - start).total_seconds() * 10) % 360

    return colorsys.hsv_to_rgb(hue / 360, 1, 1)

def beat(start, duration, full=None):
    '''beat action sweepnig from middle out'''
    if full is None: full = duration
    color = get_color(full)
    mid = npanels // 2
    tail = 15
    total = mid + tail
    colors = [darken(color, i/tail) for i in range(tail)]

    def action(current):
        if current < start: return None
        res = [(0, 0, 0)] * npanels
        percent = (current - start).total_seconds() / duration.total_seconds()

        diff = int(round(percent * total))
        fl = mid - diff
        fr = mid + diff

        for i in reversed(range(tail)):
            p = min(mid, fl + i)
            if p >= 0:
                res[p] = colors[i]

            p = max(mid, fr - i)
            if p < npanels:
                res[p] = colors[i]

        return res

    return (action, start+duration)

def all_beat(start, duration, full=None):
    '''beat action pulse all'''
    if full is None: full = duration
    color = get_color(full)

    def action(current):
        if current < start: return None
        percent = (current - start).total_seconds() / duration.total_seconds()
        new_color = darken(color, percent)
        res = [new_color] * npanels
        return res

    return (action, start+duration)

def ping(start, duration, full=None):
    '''left to right ping'''
    if full is None: full = duration
    color = get_color(full)
    tail = 15
    total = npanels + tail
    colors = [darken(color, i/tail) for i in range(tail)]

    def action(current):
        if current < start: return None
        res = [(0, 0, 0)] * npanels
        percent = (current - start).total_seconds() / duration.total_seconds()
        head = int(round(percent * total))

        for i in reversed(range(tail)):
            p = head - i
            if p >= 0 and p < npanels:
                res[p] = colors[i]

        return res

    return (action, start+duration)

def pong(start, duration, full=None):
    '''left to right ping'''
    if full is None: full = duration
    color = get_color(full)
    tail = 30
    total = npanels + tail
    colors = [darken(color, i/tail) for i in range(tail)]

    def action(current):
        if current < start: return None
        res = [(0, 0, 0)] * npanels
        percent = (current - start).total_seconds() / duration.total_seconds()
        head = npanels - int(round(percent * total))

        for i in reversed(range(tail)):
            p = head + i
            if p >= 0 and p < npanels:
                res[p] = colors[i]

        return res

    return (action, start+duration)
