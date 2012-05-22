
class ASTNode(object)

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, val):
        self._name = val

class ModelNode(ASTNode):
    pass


class SystemEquationNode(ASTNode):

    @property
    def processNode(self)
        return self._processNode

    @processNode.setter
    def processNode(self, val)
        self._processNode = val


class CoopNode(ASTNode):

    right = None
    left = None
    actionset = None



