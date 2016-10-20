import lumiversepython as lumiverse
from datetime import datetime, timedelta
from threading import Thread
from time import sleep
import sys

from actions import beat, all_beat, ping, pong
from config import npanels, path
from data import fetch, renderq
from render import render

rig = lumiverse.Rig(path)
rig.init()
rig.run()
panels = [rig.select('$panel=%d' % p) for p in xrange(1, npanels + 1)]

def apply(colors):
    '''set the colors of the panels accoridingly'''
    map(lambda (p, c): p.setRGBRaw(*c), zip(panels, colors))

def main():
    dummy = '-d' in sys.argv or '--dummy' in sys.argv
    silent = '-s' in sys.argv or '--silent' in sys.argv

    nverions = 3
    pingpong = 0
    current_version = 2
    change_interval = timedelta(seconds=30)
    next_change = datetime.now() + change_interval

    update_interval = timedelta(minutes=5)
    next_update = datetime.now() + update_interval

    fetch(dummy)

    actions = []
    t, wait = (datetime.now(), timedelta(0.8))
    if not renderq.empty(): t, wait = renderq.get()

    while True:
        if datetime.now() > next_change:
            current_version = (current_version + 1) % nverions
            next_change += change_interval

        if datetime.now() > next_update:
            Thread(target=fetch, args=(dummy,)).start()
            next_update += update_interval

        while t < datetime.now():
            if current_version == 0:
                actions.append(beat(t, wait * 3, wait))
            elif current_version == 1:
                if wait.total_seconds() > 0.75:
                    actions.append(all_beat(t, wait / 4, wait))
                    actions.append(all_beat(t + wait / 4, wait * 3 / 4, wait))
                else:
                    actions.append(all_beat(t, wait))
            else:
                if pingpong:
                    actions.append(ping(t, wait))
                else:
                    actions.append(pong(t, wait))
                pingpong = not pingpong

            t, wait = (t + wait, wait) if renderq.empty() else renderq.get()
            if not silent:
                print 60 / wait.total_seconds()
        actions, result = render(actions)
        apply(result)

if __name__ == '__main__':
    main()
