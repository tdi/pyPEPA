#!/usr/bin/env python
"""
Module with classes for PEPA model.

"""

class BaseNode():
    left,right = None, None
    data = None
    asttype = None

    def __init__(self, data, asttype):
        self.data = data
        self.asttype = asttype

    def __str__(self):
        print(self.asttype)

class ChoiceNode(BaseNode):
    lhs, rhs = None, None
    reolved = None

    def __init__(self, data, asttype):
        super().__init__(data, asttype)

class PrefixNode(BaseNode):
    action, resolved,rate = None, None, None

    def __init__(self, data, asttype):
        super().__init__(data, asttype)

class DefNode(BaseNode):
    process, resolved = None, None

    def __init__(self, data, asttype):
        super().__init__(data, asttype)

class ActivityNode(BaseNode):

    action, rate = "", ""

    def __init__(self, data, asttype):
        super().__init__(data, asttype)

class ProcdefNode(BaseNode):
    name  = None

    def __init__(self, data, asttype):
        super().__init__(data, asttype)

class CoopNode(BaseNode):
    cooptype, actionset = None, None

    def __init__(self, data, asttype):
        super().__init__(data, asttype)

class SyncsetNode(BaseNode):
    actionset = None

    def __init__(self, data, asttype):
        super().__init__(data, asttype)

