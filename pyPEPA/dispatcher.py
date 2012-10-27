#!/usr/bin/env python
import requests
import Queue
import time
import json
from math import ceil
from experiments.experiment import range_maker
from threading import Thread

workers = {"a" : ["127.0.0.1", "8090"], "b": ["127.0.0.1", "8080"]}
# workers = {}
# workers = {"a" : ["127.0.0.1", "8090"]}
values =  [1,2,3,4,5,6,7,8,9,10,11,12,13]
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
    print("my time %s" % (time.time() - start))
    res = json.loads(r.text)
    res2 = json.loads(res["result"])
    queue.put(res2[1])


def check_alive():
    for worker in workers:
        try:
            addr = workers[worker][0]
            port = workers[worker][1]
            r = requests.head("http://" + addr + ":" + str(port) +"/models")
        except Exception:
            print("Worker %s dead" % worker)


def map():
    myq = Queue.Queue()
    check_alive()
    tasks = carousel(values, len(workers))
    i = 0
    for worker in list(workers.keys()):
        task = tasks.pop(0)
        experiment = {"actionth": "use", "rate": "userate", "values": task, "q": myq }
        t = Thread(target=req, args=(workers[worker][0], workers[worker][1], experiment, i))
        t.start()
        i = i + 1
        print("worker %s has task %s" % (worker, task))
    vals = []
    while i != 0:
        if not myq.empty():
            i = i - 1
            val = myq.get()
            vals = vals + val
    print(vals)




if __name__ == "__main__":
    map()
