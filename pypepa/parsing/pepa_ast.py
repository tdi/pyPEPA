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

    def __init__(self, data, asttype):
        super(ChoiceNode, self).__init__(data, asttype)

class PrefixNode(BaseNode):

    def __init__(self, data, asttype):
        super(PrefixNode, self).__init__(data, asttype)

class DefNode(BaseNode):

    def __init__(self, data, asttype):
        super(DefNode, self).__init__(data, asttype)

class ActivityNode(BaseNode):

    def __init__(self, data, asttype):
        self.action = ""
        self.rate = ""
        super(ActivityNode, self).__init__(data, asttype)

class ProcdefNode(BaseNode):

    def __init__(self, data, asttype):
        self.aggregation = None
        self.aggr_num = 0
        super(ProcdefNode, self).__init__(data, asttype)

class CoopNode(BaseNode):

    def __init__(self, data, asttype):
        self.actionset = None
        self.cooptype = None
        super(CoopNode, self).__init__(data, asttype)

class SyncsetNode(BaseNode):

    def __init__(self, data, asttype):
        self.actionset = None
        super(SyncsetNode, self).__init__(data, asttype)

