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

    def __init__(self, data):
        super(ChoiceNode, self).__init__(data, "choice")

class PrefixNode(BaseNode):

    def __init__(self, data):
        super(PrefixNode, self).__init__(data, "prefix")

class DefNode(BaseNode):

    def __init__(self, data):
        super(DefNode, self).__init__(data, "definition")

class ActivityNode(BaseNode):

    def __init__(self, data):
        self.action = ""
        self.rate = ""
        super(ActivityNode, self).__init__(data, "activity")

class ProcdefNode(BaseNode):

    def __init__(self, data):
        self.aggregation = None
        self.aggr_num = 0
        super(ProcdefNode, self).__init__(data, "procdef")

class CoopNode(BaseNode):

    def __init__(self, data):
        self.actionset = None
        self.cooptype = None
        super(CoopNode, self).__init__(data, "coop")

class SyncsetNode(BaseNode):

    def __init__(self, data):
        self.actionset = None
        super(SyncsetNode, self).__init__(data, "syncset")

