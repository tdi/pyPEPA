
class Element(object):
    
    def __init__(self):
        self.ports = []
        self.beh = None
        self.bindings = {}

    def bind(self, port, action):
        self.bindings[port] = action

    def get_bindings(self):
        return self.bindings

    def add_port(self, port):
        self.ports.append(port)

    def get_ports(self):
        return self.ports

    def get_connections(self):
        connections = {}
        for port in self.ports:
            connections[port.other.parent]=port
        return connections
            
