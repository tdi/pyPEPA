#!/usr/bin/env python
"""Simple server that listens on port 6000 and echos back every input to the client.
"""
from gevent.server import StreamServer
import gevent
import socket
import pepa_prot
import glob
import os
import sys
from pepa_model import PEPAModel

clients = set()
models = list()

def send_callback(address):
    ip = (address, 6001)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(ip)

def process(socket, address):
    if address[0] not in clients:
        clients.add(address[0])
    print ('New connection from %s:%s' % address)

    # Receive header LEN(4), VERSION(1)
    header_bytes = socket.recv(5)
    header = pepa_prot.extract_header(header_bytes)

    print ("Length of data %i, protocol version %i" %(header[0], header[1]))
    if not pepa_prot.check_version(header[1]):
        print("Protocol mismatch")

    data_bytes = socket.recv(header[0])
    data = pepa_prot.extract_data(data_bytes)
    ret = process_cmd(data)
    socket.sendall( pepa_prot.prepare_to_send(ret))
    socket.close()

def process_cmd(data):
    cmd = data["cmd"]
    print("CMD:%s" % cmd)
    ret = dict()
    if cmd == "list_models":
        ret["ret"] = models
        ret["status"]  = 1
    elif cmd == "solve_ss":
        ret["ret"] = solve_ss(data["data"], data["ret"])
        ret["status"]  = 1
    elif cmd == "solve_th":
        ret["ret"] = solve_th(data["data"], data["ret"])
        ret["status"] = 1
    else:
        print("Command not found")
        ret["status"]  = 0
        return None
    ret["rid"] = data["rid"]
    return ret


def solve_ss(data, ret):
    print("Solving %s, returning %s" % (data, ret))
    model = "models/%s" % data
    pm = PEPAModel({"file": model, "solver": "sparse"})
    pm.derive()
    pm.steady_state()
    ss = pm.get_steady_state_vector()
    return ss

def solve_th(data, ret):
    print("Solving %s, returning %s" % (data, ret))
    model = "models/%s" % data
    pm = PEPAModel( { "file" : model, "solver" : "sparse"})
    pm.derive()
    pm.steady_state()
    th = pm.get_throughoutput()
    return th

def get_models():
    global models
    cwd = os.getcwd()
    os.chdir("models")
    models = glob.glob("*.pepa")
    os.chdir(cwd)




if __name__ == '__main__':
    if os.path.isdir("models"):
        get_models()
    else:
        print("No models directory")
        exit(1)
    port = int(sys.argv[1])
    server = StreamServer(('0.0.0.0', port), process)
    print ('Starting server on port %d' % port)
    server.serve_forever()
