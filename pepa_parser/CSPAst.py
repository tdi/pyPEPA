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



explored = []
def visit_tree(node):
    print(node.data)
    if node.left is not None and node.left not in explored:
        visit_tree(node.left)
    if node.right is not None and node.right not in explored:
        visit_tree(node.right)
    


def tree_walker(node):
    visit_tree(node)
