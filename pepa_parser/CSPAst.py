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




# def visit_tree(node):
#     print(node.data,end="")
#     if node.left is not None:
#         print("(", end="")
#         visit_tree(node.left)
#         print(" ",end="")
#     if node.right is not None:
#         visit_tree(node.right)
#         print(")", end="")
#

def tree_walker(node):
    visit_tree(node)
    print("")
