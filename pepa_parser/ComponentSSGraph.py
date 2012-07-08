#!/usr/bin/env python


class ComponentState():

    def __init__(self):
        self.name = None
        self.resolved = None
        self.transitions = []

class Transition():

    def __init__(self, action, rate, to):
        self.rate = rate
        self.action = action
        self.to = to


class ComponnetSSGraph():
    """
    self.ss is a hash table, the keys are state names e.g. P1 or resolved where not possible -> ComponenStates

    """

    def __init__(self):
        self.name = ""
        self.ss = {}
        self.firstnode = None
        self.dotrepr = ""


