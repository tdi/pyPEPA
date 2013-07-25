#!/usr/bin/env python
"""
Module with classes for PEPA model.

"""

class BaseNode(object):
 
    def __init__(self, data, asttype):
        self.left, self.right = None, None
        self.length = None
        self.data = data
        self.asttype = asttype

    def __str__(self):
        return self.data

class ChoiceNode(BaseNode):
    asttype = "choice"
    def __init__(self, data):
        super(ChoiceNode, self).__init__(data, self.asttype)

class PrefixNode(BaseNode):
    asttype = "prefix"
    def __init__(self, data):
        super(PrefixNode, self).__init__(data, self.asttype)

class DefNode(BaseNode):
    asttype = "definition"
    def __init__(self, data):
        super(DefNode, self).__init__(data, self.asttype)

class ActivityNode(BaseNode):
    asttype = "activity"
    def __init__(self, data):
        self.action = ""
        self.rate = ""
        super(ActivityNode, self).__init__(data, self.asttype)

class ProcdefNode(BaseNode):
    asttype = "procdef"
    def __init__(self, data):
        self.aggregation = None
        self.aggr_num = 0
        super(ProcdefNode, self).__init__(data, self.asttype)

class CoopNode(BaseNode):
    asttype = "coop"
    def __init__(self, data):
        self.actionset = None
        self.cooptype = None
        super(CoopNode, self).__init__(data, self.asttype)

class SyncsetNode(BaseNode):
    asttype = "syncset"
    def __init__(self, data):
        self.actionset = None
        super(SyncsetNode, self).__init__(data, self.asttype)

