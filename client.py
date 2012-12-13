import socket
import sys
from gevent.server import StreamServer
import pepa_prot

# prepare_to_send = lambda x: struct.pack('!l',len(x)) + x

rid = 1

def callback(socket, address):
    print("Received callback from %s:%s" % address)
    data = socket.recv(5)
    print(data)

if __name__ == "__main__":

    server = StreamServer( ('0.0.0.0', 6001), callback)
    address = ('localhost', 6000)
    dat = {"cmd": "solve_ss", "data":"resource.pepa","rid": rid, "ret":"ss"}
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect(address)
    except Exception as e:
        print("Cannot connect to %s:%s" % address)
        exit(1)
    print("Sending CMD:%s" % dat["cmd"])
    tos = pepa_prot.prepare_to_send(dat)
    sock.send(tos)
    print("Answer")
    header_bytes = sock.recv(5)
    header = pepa_prot.extract_header(header_bytes)

    print ("Length of data %i, protocol version %i" %(header[0], header[1]))
    if not pepa_prot.check_version(header[1]):
        print("Protocol mismatch")
    #TODO: zmienic w petelke
    data_bytes = sock.recv(header[0])
    data = pepa_prot.extract_data(data_bytes)
    print(data)

    server.serve_forever()
