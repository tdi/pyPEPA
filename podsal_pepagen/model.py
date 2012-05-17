

class Model(object):
    
    def __init__(self, components, links, instances):
        self.components = components
        self.links = links
        self.instances = instances

    def __init__(self):
        self.components = []
        self.links = []
        self.instances = []

    def connect_ports(self, port1, port2):
        port1.other = port2
        port2.other = port1

