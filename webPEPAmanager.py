#!/usr/bin/env python
import json
from bottle import route, run, request, abort, response, error
from pprint import pprint
import uuid
import time
import sys
import requests

workers = {}
registered = []
worker_id_start = 1

@route('/workers', method="POST")
def reg_worker():
    port = request.forms.get("port")
    radr = request.remote_addr
    wid = uuid.uuid4()
    if (radr, port) not in registered:
        registered.append( (radr,port) )
        workers[str(wid)] = (radr, port)
    else:
        print("Already registered")
        return {"success": False, "info": "Alredy there"}
    return {"success": True, "id": str(wid), "port": port}

@route('/test')
def test():
    r = requests.

@route('/workers')
def print_workers():
    return {'success': True, "workers": workers}

def initialize():
    pass

initialize()
run(reloader=True, host='localhost', port=9090)
