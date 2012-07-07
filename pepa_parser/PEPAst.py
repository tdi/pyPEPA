class Model():
    processes = {}
    systemeq = None
    rates = None
    costam = ""


class SSNode():
    succ = []
    data = ""

    def __init__(self, data):
        self.data = data

class ProcessGraph():
    firstnode = None
    vertices = []

    def __init__(self,name):
        self.name = name


class Transition():
    action = ""
    rate = ""

class GraphNode():
    succ = []


class Node():
    left, right, data, asttype, actions, visited = None, None, 0, None, None, 0
    activity, rate = "",""
    resolved = ""

    def __init__(self,data,asttype):
        self.right = None
        self.left = None
        self.data = data
        self.asttype = asttype
        self.lhs = ""
        self.activity = ""
        self.action = None
        self.visited = 0
        self.process = ""
        self.resolved = ""

    def __str__(self):
        print(self.asttype)


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
    action, resolved = None, None

    def __init__(self, data, asttype):
        super().__init__(data, asttype)

class DefNode(BaseNode):
    process, resolved = None, None

    def __init__(self, data, asttype):
        super().__init__(data, asttype)



