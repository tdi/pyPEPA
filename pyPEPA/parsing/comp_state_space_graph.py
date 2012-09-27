#!/usr/bin/env python


class ComponentState():

    def __init__(self):
        self.name = None
        self.resolved = None
        self.transitions = []

class Transition():

    def __init__(self, action, rate, to):
        self.rate = rate
        self.var_rate = None
        self.action = action
        self.to = to


class SystemEquation():

    def __init__(self):
        self.processes = {}


class ComponentSSGraph():

    def __init__(self, name=""):
        self.name = name
        self.ss = {}
        self.activities = []
        self.shared = []

    def __str__(self):
        return "Component " + self.name + " " + len(self.ss.keys())


class ModelSSGraph():
    """
    self.ss is a hash table, the keys are state names e.g. P1 or resolved where not possible -> ComponenStates

    """
    def __init__(self):
        self.name = ""
        self.ss = {}
        self.dotrepr = ""
        self.shared_actions = None


