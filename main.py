
import sys
import getopt
from comp import Component
from link import Link
from elem import Port
from utils import printcol

#
#  Client(send) --- Channel(recv)*Channel(se) --- Server(recv)
#

def main():
    client = Component("client", "Client")
    send = Port("send")
    client.add_port(send)
    send.parent = client

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

    # Port connecting
    
    send.port = rec
    rec.port = send
    
    se.port = recv
    recv.port = se

    model = (client, server)
    
    for el in model:
        print("Component", el)
        for p in el.get_ports():
            print(" ",p.port.parent)


if __name__ == "__main__":
    main()
