from elem import Element

class Component(Element):

    def __init__(self, name, cclass):
        super(Component,self).__init__()
        self.name = name
        self.cclass = cclass
    
    def __str__(self):
        return "name:" + self.name + ",class:" + self.cclass
