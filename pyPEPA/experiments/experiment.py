#!/usr/bin/env python

import sys

def get_rate_from_actset(action, actset):
    """ Returns rate from actset returned from solver """
    for act in actset:
        if act[0] == action:
            return float(act[1])


def rate_experiment(rate_x, var_rate, rate_y, pepa_model, llist=False):
    """ var_rate is a generator
        rate_y is the resulting rate on the Y axis
    """
    rate_ys = []
    rate_xs = []
    rates = pepa_model.get_rates()
    if rate_x not in rates:
        print("No such rate {}".format(rate_x))
        exit(1)
    if hasattr(var_rate, '__call__'):
        for i in var_rate():
                rates[rate_x] = str(i)
                rate_xs.append(float(i))
                pepa_model.recalculate(rates)
                pepa_model.steady_state()
                rate_ys.append( get_rate_from_actset(rate_y, pepa_model.get_throughoutput()))
    else:
        for i in var_rate:
                rates[rate_x] = str(i)
                rate_xs.append(float(i))
                pepa_model.recalculate(rates)
                pepa_model.steady_state()
                rate_ys.append( get_rate_from_actset(rate_y, pepa_model.get_throughoutput()))

    return (rate_xs, rate_ys)

def rate_experiment_two(rate_x, var_rate, rate_y, rate_z, pepa_model, llist=False):
    """ var_rate is a generator
        rate_y is the resulting rate on the Y axis
    """
    rate_ys = []
    rate_xs = []
    rate_zs = []
    rates = pepa_model.get_rates()
    if rate_x not in rates:
        print("No such rate {}".format(rate_x))
        exit(1)
    for i in var_rate():
            rates[rate_x] = str(i)
            rate_xs.append(float(i))
            pepa_model.recalculate(rates)
            pepa_model.steady_state()
            rate_ys.append( get_rate_from_actset(rate_y, pepa_model.get_throughoutput()))
            rate_zs.append( get_rate_from_actset(rate_z, pepa_model.get_throughoutput()))
    return (rate_xs, rate_ys, rate_zs)

def range_maker(low, hi, step):
    """
    Returns a generator function
    """
    n = { 'low': low, 'hi':hi, 'step':step}
    def counter():
        low = n['low']
        hi = n['hi']
        step = n['step']
        cur = low
        while cur <= hi:
            yield cur
            cur += step
    return counter

