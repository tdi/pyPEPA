import socket
import sys
import gevent
import pepa_prot
import time
from math import ceil
rid = 1

workers = [ ('localhost', 6000),
            ]

config = {"timing":1}


def exp(data, ran):
    rid = 1000
    dat = data
    vals = [i for i in range(1,ran)]
    cpus = len(workers)
    tasks = _carousel(vals, cpus)
    jobs = []
    if "timing" in config:
        start = time.time()
    for w in workers:
        job = tasks.pop(0)
        dat["values"] = job
        jobs.append(gevent.spawn(send_recv, w, dat))
    gevent.joinall(jobs)
    if "timing" in config:
        stop = time.time() - start
    return "%s,%d,%s\n" % ( model, ran, stop)

def do_solve_ss(self, arg):
    """ solve_ss MODEL WORKER """
    args = self._parse(arg)
    if len(args) != 2:
        print("Wrong arguments")
        return
    try:
        workers[int(args[1])]
    except:
        print("No such worker")
        return
    global rid
    rid = rid + 1
    dat = {"cmd": "solve_ss", "data" : args[0], "rid" :rid, "ret": "ss"}
    data = send_recv( workers[int(args[1])], dat)
    print(data["data"])


def send_recv( address, dat):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # sock.settimeout(1)
        sock.connect(address)
    except Exception as e:
        raise
    tos = pepa_prot.prepare_to_send(dat)
    sock.send(tos)
    header_bytes = sock.recv(5)
    header = pepa_prot.extract_header(header_bytes)
    if not pepa_prot.check_version(header[1]):
        print("Protocol mismatch")
        exit(1)
    #TODO: zmienic w petelke
    print(header[0])
    data_bytes = sock.recv(header[0])
    sock.shutdown(socket.SHUT_RDWR)
    sock.close()
    return pepa_prot.extract_data(data_bytes)

def _carousel(sequence, m):
    if len(sequence) < m:
        m = len(sequence)
    n = float(len(sequence))
    return [sequence[((i+0)*int(n/m)):((i+1)*int(ceil(n/m)))] for i in range(m)]



if __name__ == "__main__":
    import sys
    model = "resource.pepa"
    ran = 100
    dat = {"cmd": "exp", "data" : model, "rid" :rid, "action": "use", "ret": "th", "rate":"userate","map":1}
    print("Using %s workers" % len(workers))
    with open("result.txt", "w") as f:
        for i in range(2):
            f.write(exp(dat, ran))
    

