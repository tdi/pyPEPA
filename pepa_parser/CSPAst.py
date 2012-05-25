class Model():
    processes = {}
    costam = ""

class Node():
    left, right, data, asttype = None, None, 0, None

    def __init__(self,data,asttype):
        self.right = None
        self.left = None
        self.data = data
        self.asttype = asttype
        self.lhs = ""

    def __str__(self):
        print(self.asttype)



def visit_tree(node):
    print(node.data,end="")
    if node.left is not None:
        print("(", end="")
        visit_tree(node.left)
        print(" ",end="")
    if node.right is not None:
        visit_tree(node.right)
        print(")", end="")


def tree_walker(node):
    visit_tree(node)
    print("")
