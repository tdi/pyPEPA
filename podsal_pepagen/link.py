from elem import Element

class Link(Element):

    def __init__(self, name, cclass):
        super(Link,self).__init__()
        self.name = name
        self.cclass = cclass
    
    def __str__(self):
        return "name:" + self.name + ",class:" + self.cclass
