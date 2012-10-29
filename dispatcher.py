#!/usr/bin/env python
import requests
import time
import json
from math import ceil
from experiments.experiment import range_maker
from multiprocessing import Process, Queue

workers_avail = {"a" : ["127.0.0.1", "8090"], "b": ["127.0.0.1", "8080"]}
# workers = {"a" : ["127.0.0.1", "8090"], "b": ["127.0.0.1", "8080"]}
# workers = {"a" : ["127.0.0.1", "8090"]}
values =  [1,2,3,4,5,6,7,8,9,10,11,12,13]
#values =  [i for i in range(1,22)]
#values =  [1,2,3,4,5]

def carousel(sequence, m):
    n = float(len(sequence))
    return [sequence[((i+0)*int(n/m)):((i+1)*int(ceil(n/m)))] for i in range(m)]

def req(addr, port, experiment, name):
    print("Sender thread %s" % name)
    start = time.time()
    vals = json.dumps(experiment["values"])
    queue = experiment["q"]
    data = {"actionth":experiment["actionth"], "values": vals, "rate":experiment["rate"]}
    r = requests.post("http://" + addr + ":" + str(port) + "/models/test/experiment", data=data)
    res = json.loads(r.text)
    res2 = json.loads(res["result"])
    queue.put((res2[1], name))


def check_alive(w):
    for worker in workers_avail:
        try:
            addr = workers_avail[worker][0]
            port = workers_avail[worker][1]
            r = requests.head("http://" + addr + ":" + str(port) +"/models")
            w[worker] = workers_avail[worker]
        except Exception:
            print("Worker %s dead" % worker)
    return w


def map_tasks():
    myq =Queue()
    workers = {}
    workers = check_alive(workers)
    print(workers)
    tasks = carousel(values, len(workers))
    i = 0
    start = time.time()
    for worker in list(workers.keys()):
        task = tasks.pop(0)
        experiment = {"actionth": "use", "rate": "userate", "values": task, "q": myq }
        t = Process(target=req, args=(workers[worker][0], workers[worker][1], experiment, i))
        t.start()
        i = i + 1
        print("worker %s has task %s" % (worker, task))
    vals = []
    for worker in list(workers.keys()):
        val = myq.get()[0]
        vals = vals + val
    print("Time: %s" % (time.time()-start))
    print(vals)

if __name__ == "__main__":
    map_tasks()
