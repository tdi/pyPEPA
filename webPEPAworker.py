#!/usr/bin/env python
import json
from bottle import route, run, request, abort, response, error
from pprint import pprint
from pepa_model import PEPAModel
from experiments.experiment import rate_experiment
from math import ceil
import multiprocessing
import requests
import uuid
import time
import sys

solutions = []
models = {}
master_addr = "http://localhost:9090/"
_port = None
config = { "timing" : 1 }


@route('/models/<name>', method="PUT")
def submit_model(name):
    """ Submits new model, just a name and a filename from a form
    """
    model = request.forms.get("modelfile")
    if name not in models:
        models[name] = model
    else:
        return { "success" : False, "error": "Model with this name already exists" }
    return { "success" : True, "modelfile": model, "id": name}


@route('/models/<name>/modelfile')
def get_modelfile(name):
    if name not in models:
        return { "success": False, "error": "Model with this name does not exist" }
    return { "success": True, "modelfile" : models[name], "id": name }

def carousel(sequence, m):
    if len(sequence) < m:
        m = len(sequence)
    n = float(len(sequence))
    return [sequence[((i+0)*int(n/m)):((i+1)*int(ceil(n/m)))] for i in range(m)]

def job(task, name, queue):
    print("Process %s started"% multiprocessing.current_process().name)
    actionth = task["actionth"]
    rate = task["rate"]
    values = task["values"]
    pargs = { "file": "resource.pepa", "solver": "sparse" }
    pm = PEPAModel(pargs)
    pm.derive()
    result = rate_experiment(rate, values, actionth, pm)
    queue.put(result)

@route('/models/<name>/experimentp', method="POST")
def experimentp(name):
    cpus = multiprocessing.cpu_count()
    queue = multiprocessing.Queue()
    actionth = request.forms.get("actionth")
    rate = request.forms.get("rate")
    values = request.forms.get("values")
    vals = json.loads(values)
    # task = {"actionth": actionth, "rate": rate, "values" : vals}
    pargs = {"file" : "resource.pepa", "solver": "sparse"}
    tasks = carousel(vals, cpus)
    for t in tasks:
        task = {"actionth": actionth, "rate": rate, "values" : t}
        p = multiprocessing.Process(target=job, args=(task, "lala", queue))
        p.start()
    vals = []
    for i in range(len(tasks)):
        result = queue.get()
        print(result)
        vals.append(result)
    return {"success": True, "result": json.dumps(vals)}


@route('/models/<name>/experiment', method="POST")
def experiment(name):
    actionth = request.forms.get("actionth")
    rate = request.forms.get("rate")
    values = request.forms.get("values")
    vals = json.loads(values)
    pargs = {"file" : "resource.pepa", "solver": "sparse"}
    pm = PEPAModel(pargs)
    pm.derive()
    result = rate_experiment(rate, vals, actionth, pm)
    return {"success": True, "result": json.dumps(result)}

@route('/models/<name>/ss')
def ss_model(name):
    if name not in models:
        return { "success": False, "error": "Nah"}
    model = models[name]
    start = time.time()
    pm = PEPAModel({"file": model, "solver": "sparse"})
    pm.derive()
    pm.steady_state()
    stop = time.time() - start
    ss = pm.get_steady_state_vector()
    ss2 = []
    for s in ss:
        ss2.append(str(s))
    ss2 = ",".join(ss2)
    return {"success": True, "ss": ss2, "time": stop}

@route('/models/<name>/th')
def th_model(name):
    if name not in models:
        return { "success": False, "error": "Nah"}
    model = models[name]
    start = time.time()
    pm = PEPAModel({"file": model, "solver": "sparse"})
    pm.derive()
    pm.steady_state()
    stop = time.time() - start
    th = pm.get_throughoutput()
    return {"success": True, "th": th, "time": stop}


@route('/models/<name>', method="GET")
def print_model(name):
    """ Return representation of a model
    """
    if name in models:
        return { "success" : True, "model": models[name] }
    else:
        return { "success" : False, "info": "no such model" }

@route('/models', method="POST")
def submit_model_noname():
    model = request.forms.get("modelfile")
    mid = uuid.uuid1()
    models[str(mid)] = model
    return { "success": True, "model": models[str(mid)], "id": str(mid) }

@route('/models', method="GET")
def list_models():
    return { "success": True, "models": models }

def _initialize(port):
    """ Read config with a master """
    _port = port
    models["test"] = "resource.pepa"
    # _register(port)


def _register(port):
    try:
        r = requests.post(master_addr + "workers", data={'port': port})
    except Exception as e:
        print("Cannot connect to %s" %master_addr )
        sys.exit(1)

@route('/onet')
def redircheck():
    response.status=301
    response.add_header("Location", "http://onet.pl/")

@error(404)
def error_404(code):
    return "404 not found"


if __name__ == '__main__':
    _initialize(sys.argv[1])
    run(host='localhost', port=sys.argv[1])
