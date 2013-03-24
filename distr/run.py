import gevent
import gevent.monkey
gevent.monkey.patch_all()
import sys
import socket
import pepa_prot
import time
from math import ceil
import multiprocessing
rid = 1

# workers = [ ('lab-sec-1', 6000),
#  	    ('lab-sec-2', 6000),
 	    # ('lab-sec-3', 6000),
            # ]
workers = [('localhost', 8000)]
config = {"timing":1}


def _sendjob(dat,w, queue):
	queue.put(send_recv(w,dat))
	return

def expproc(data, ran):
    rid = 1000
    dat = data
    vals = [i for i in range(1,ran)]
    cpus = len(workers)
    tasks = _carousel(vals, cpus)
    jobs = []
    if "timing" in config:
        start = time.time()
    queue = multiprocessing.Queue()
    for w in workers:
        job = tasks.pop(0)
        dat["values"] = job
	p = multiprocessing.Process(target=_sendjob, args=(dat, w,queue))
	p.start()
    for w in range(len(workers)):
        result = queue.get()
    if "timing" in config:
        stop = time.time() - start
    return "%s,%d,%s\n" % ( model, ran, stop)


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
    model = "browser.pepa"
    ran = 100
    dat = {"cmd": "exp", "data" : model, "rid" :rid, "action": "display", "ret": "th", "rate":"m", "map":1}
    print("Using %s workers" % len(workers))
    with open("result.txt", "w") as f:
        for i in range(2):
            f.write(exp(dat, ran))
    

