import json
from bottle import route, run, request, abort
from pprint import pprint
import uuid

solutions = []
models = {}
master_addr = "http://localhost:8081/"

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

def initialize():
    """ Read config with a master """
    pass

initialize()
run(reloader=True, host='localhost', port=8080)
