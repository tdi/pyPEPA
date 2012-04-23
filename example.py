from model import Model
from port import Port
from comp import Component
from link import Link


m = Model()
client = Component("client", "Client")
client.beh = "Client:=wait->send->Client + wait->send2->Client;"
send = Port("send")
send2 = Port("send2")
client.add_port(send)
client.add_port(send2)
send.parent = client
send2.parent = client
# Bind port to action from beh, we will construct later the action name upon
# this
client.bind(send, "send")
client.bind(send2, "send2")

server2 = Component("server2", "Server")
recv2 = Port("receive")
server2.add_port(recv2)
recv2.parent = server2
server2.bind(recv2, "receive")

server = Component("server", "Server")
recv = Port("receive")
server.add_port(recv)
recv.parent = server

server2.bind(recv, "receive")

channel = Link("channel", "Channel")
rec = Port("rec")
se = Port("se")
channel.add_port(rec)
channel.add_port(se)
rec.parent = channel
se.parent = channel

channel.bind(rec, "rec")
channel.bind(se, "se")

channel2 = Link("channel2", "Channel")
rec2 = Port("rec2")
se2 = Port("se2")
channel2.add_port(rec2)
channel2.add_port(se2)
rec2.parent = channel2
se2.parent = channel2

channel2.bind(rec2, "rec2")
channel2.bind(se2, "se2")
# dodaje do modelu

m.components.append(client)
m.components.append(server)
m.components.append(server2)
m.components.append(channel)
m.components.append(channel2)

m.connect_ports(send, rec)
m.connect_ports(send2, rec2)
m.connect_ports(se, recv)
m.connect_ports(se2, recv2)

def daj():
    return client
