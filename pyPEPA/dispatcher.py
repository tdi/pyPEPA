#!/usr/bin/env python
import requests
import time
from math import ceil
from experiments.experiment import range_maker
from threading import Thread
import json

workers = {"a" : ["127.0.0.1", "8090"], "b": ["127.0.0.1", "8080"]}
# workers = {"a" : ["127.0.0.1", "8090"]}
values =  [1,2,3,4,5,6,7,8,9,10,11,12,13]

def carousel(sequence, m):
    n = float(len(sequence))
    return [sequence[((i+0)*int(n/m)):((i+1)*int(n/m))] for i in range(m)]

def req(addr, port, task):
    start = time.time()
    r = requests.get("http://" + addr + ":" + str(port) + "/models/test/th")
    d = json.loads(r.text)
    print("his time %s"% d["time"])
    print("my time %s" % (time.time() - start))


def send():
    tasks = carousel(values, len(workers))
    i = 0
    for worker in list(workers.keys()):
        task = values.pop(0)
        t = Thread(target=req, args=(workers[worker][0], workers[worker][1], tasks))
        t.start()
        print("worker %s has task %s" % (worker, task))




if __name__ == "__main__":
    send()
