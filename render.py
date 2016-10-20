from datetime import datetime
from config import npanels
from math import sqrt

def multiply((r1, g1, b1), (r2, g2, b2)):
    '''multiply function for combining colors'''
    return (r1 * r2, g1 * g2, b1 * b2)

def amplitude((r, g, b)):
    return sqrt(r*r + g*g + b*b)

def blend(x, y):
    if amplitude(x) - amplitude(y) > 0.5: return x
    if amplitude(y) - amplitude(x) > 0.5: return y
    return multiply(x, y)

def combine_one(l1, l2):
    '''combine renders from two actions'''
    # assert(len(l1) == len(l2))
    if l1 is None: return l2
    elif l2 is None: return l1
    return map(lambda (a, b): blend(a, b), zip(l1, l2))

def combine(actions):
    '''combine all actions'''
    now = datetime.now()
    if len(actions) > 0:
        result = reduce(combine_one, map(lambda (f, end): f(now), actions))
        if result: return result
    return [(0, 0, 0) for i in range(npanels)]

def update(actions):
    '''remove finished actions'''
    now = datetime.now()
    return filter(lambda (f, end): now < end, actions)

def render(actions):
    '''render all action'''
    actions = update(actions)
    return (actions, combine(actions))
