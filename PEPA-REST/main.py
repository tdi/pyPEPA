import json
from bottle import route, run, request, abort
from pprint import pprint

solutions = []
models = {}
master_addr = "http://localhost:8081/"

@route('/models/<name>', method="PUT")
def submit_model(name):
    """ Submits new model, just a name and a filename from a form
    """
    model = request.forms.get("modelfile")
    models[name] = model
    return { "success" : True, "path": name}

@route('/models/<name>', method="GET")
def print_model(name):
    """ Return representation of a model
    """
    if name in models:
        return { "success" : True, "model": models[name] }
    else:
        return { "success" : False, "info": "no such model" }

@route('/')
def forma():
    return ''' <form method="POST" action="/add">
                <input name="model"  type="text" />
                </form> '''

@route('/list')
def index():
    return "{}".format(solutions)

@route('/add', method='POST')
def add():
    data = request.forms.get('model')
    solutions.append(data)
    return "Success"


def initialize():
    """ Read config with a master """
    pass

initialize()
run(reloader=True, host='localhost', port=8080)
