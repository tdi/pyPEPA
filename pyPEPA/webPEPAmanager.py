import json
from bottle import route, run, request, abort, response, error
from pprint import pprint
import uuid
import time
import sys

try:
    import requests
except ImportError:
    print("Install python-requests")
    sys.exit(1)

workers = {}

@route('/workers', method="POST")
def reg_worker():
    if request.remote_addr not in workers:
        workers[request.remote_addr]  = request.remote_addr
    else:
        print("Already registered")
    return {"success": True, "id": str(workers[request.remote_addr])}

@route('/workers')
def print_workers():
    return {'success': True, "workers": workers}

def initialize():
    pass

initialize()
run(reloader=True, host='localhost', port=8081)
