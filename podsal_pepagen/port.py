class Port(object):
    def __init__(self):
        self.port_con = None
        self.archparent = None

    def __init__(self, name):
        self.port_con = None
        self.pname = name
        self.archparent = None

    @property
    def name(self):
        return self.pname
    
    @name.setter
    def name(self, val):
        self.pname = val

    @property
    def other(self):
        return self.port_con

    @other.setter
    def other(self, val):
        self.port_con = val
  
    @property
    def parent(self):
        return self.archparent

    @parent.setter
    def parent(self, val):
        self.archparent = val

    def __str__(self):
        return self.pname


