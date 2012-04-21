
import sys
import getopt
import pprint
import pickle
from comp import Component
from link import Link
from port import Port
from model import Model

#
#  Client(send) --- Channel(recv)*Channel(se) --- Server(recv)
#        (send2) --- Channel2

def main():
    m = Model()
    client = Component("client", "Client")
    client.beh = "Client:=wait->send->Client + wait->send2.Client;"
    send = Port("send")
    send2 = Port("send2")
    client.add_port(send)
    client.add_port(send2)
    send.parent = client
    send2.parent = client

    server2 = Component("server2", "Server")
    recv2 = Port("receive")
    server2.add_port(recv2)
    recv2.parent = server2

    server = Component("server", "Server")
    recv = Port("receive")
    server.add_port(recv)
    recv.parent = server


    channel = Link("channel", "Channel")
    rec = Port("rec")
    se  = Port("se")
    channel.add_port(rec)
    channel.add_port(se)
    rec.parent = channel
    se.parent = channel

    channel2 = Link("channel2", "Channel")
    rec2 = Port("rec2")
    se2  = Port("se2")
    channel2.add_port(rec2)
    channel2.add_port(se2)
    rec2.parent = channel2
    se2.parent = channel2
   
    
    m.components.append(client)
    m.components.append(server)
    m.components.append(server2)
    m.components.append(channel)
    m.components.append(channel2)
    
    m.connect_ports(send, rec)
    m.connect_ports(send2, rec2)
    m.connect_ports(se, recv)
    m.connect_ports(se2, recv2)

    

    #DFS
def sraka():
    explored = []
    nastos = []
    def dfs_visit(vert):
        if vert.beh is not None:
            print(vert.beh)
        print(vert.name,end="")
        nastos.append(vert)
        explored.append(vert.name)
        connections = vert.get_connections()
        for con in connections.keys():
            if con.name not in explored:
                print("<"+connections[con].name+""+connections[con].other.name+">", end="")
                dfs_visit(con)
         

    dfs_visit(client)
    

    first = 1
    last = 0
    for element in nastos:
        if (element.__class__.__name__ == "Component"):
            if (first == 1):
#                print("("+element.name,end="")
                first = 0
            else:
 #               print(element.name+")",end="")
                pass
        else:
 #           print("<>"+element.name+"<>", end="")
            pass
    print() 




    




if __name__ == "__main__":
    main()
