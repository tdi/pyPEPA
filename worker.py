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
from experiments.experiment import rate_experiment
import multiprocessing
from math import ceil

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
    ret = dict()
    try:
        print("Command : %s" % data["cmd"])
        ret["data"] = doit[ data["cmd"] ](data)
        ret["rid"] = data["rid"]
    except:
        print("Command not found")
        ret["status"] = 0
    # ret = process_cmd(data)
    socket.sendall( pepa_prot.prepare_to_send(ret))
    socket.close()


def list_models(data):
    return models

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
    elif cmd == "exp":
        ret["ret"] = experiment(data, data)
        ret["status"] = 1
    elif cmd == "chk":
        ret["ret"] = "ok"
        ret["status"] = 1
    else:
        print("Command not found")
        ret["status"]  = 0
        return None
    ret["rid"] = data["rid"]
    return ret

def _carousel(sequence, m):
    if len(sequence) < m:
        m = len(sequence)
    n = float(len(sequence))
    return [sequence[((i+0)*int(n/m)):((i+1)*int(ceil(n/m)))] for i in range(m)]

def _job(task, name, queue):
    curproc = multiprocessing.current_process().name
    print("Process %s started"% curproc)
    actionth = task["actionth"]
    rate = task["rate"]
    values = task["values"]
    print("Process %s Calculating %d values " % (curproc, len(values)))
    pargs = { "file": "resource.pepa", "solver": "sparse" }
    pm = PEPAModel(pargs)
    pm.derive()
    result = rate_experiment(rate, values, actionth, pm)
    queue.put(result)

def experiment(data):
    print("Experiment %s, returning bool" % data)
    model = "models/%s" % data["data"]
    rate = data["rate"]
    action = data["action"]
    values = data["values"]
    if "map" not in data:
        pm = PEPAModel({"file": model, "solver": "sparse"})
        pm.derive()
        result = rate_experiment(rate, values, action, pm)
        return result
    else:
        cpus = multiprocessing.cpu_count()
        queue = multiprocessing.Queue()
        tasks = _carousel(values, cpus)
        for t in tasks:
            task = {"actionth": action, "rate": rate, "values" : t}
            p = multiprocessing.Process(target=_job, args=(task, "TASKNAME", queue))
            p.start()
        vals = []
        for i in range(len(tasks)):
            result = queue.get()
            # print(result)
            vals.append(result)
        return vals

def solve_ss(data):
    print("Solving %s" % data)
    model = "models/%s" % data["data"]
    pm = PEPAModel({"file": model, "solver": "sparse"})
    pm.derive()
    pm.steady_state()
    ss = pm.get_steady_state_vector()
    return ss

def solve_th(data):
    print("Solving %s" % data)
    model = "models/%s" % data["data"]
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


doit = {"list_models" : (lambda x: models),
        "solve_ss" : solve_ss,
        "solve_th": solve_th,
        "exp": experiment,
        "chk": lambda x: 1
        }

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
