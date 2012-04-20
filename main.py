
import sys
import getopt
from comp import Component
from link import Link
from elem import Port
from utils import printcol

#
#  Client(send) --- Channel(recv)*Channel(se) --- Server(recv)
#        (send2) --- Channel2

def main():
    client = Component("client", "Client")
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
   
    
    # Port connecting
    
    send.other = rec
    rec.other = send

    send2.other = rec2
    rec2.other = send2

    se.other = recv
    recv.other = se

    se2.other = recv2
    recv2.other = se2


    #DFS

    explored = []
    nastos = []
    def dfs_visit(vert):
        print("Visitłem", vert.name)
        nastos.append(vert)
        explored.append(vert.name)
        for con in vert.get_connections():
            if con.name not in explored:
                dfs_visit(con)
         

    dfs_visit(client)

    for element in nastos:
        first = 1
        last = 0
        if (element.__class__.__name__ == "Component"):
            if (first == 1):
                print("("+element.name,end="")
            else:
                print(




    




if __name__ == "__main__":
    main()
