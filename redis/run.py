from flask import Flask , request , jsonify
import json
import requests
import threading
import subprocess
from dataCollector import *
app = Flask(__name__)



@app.before_request
def option_autoreply():
    """ Always reply 200 on OPTIONS request """

    if request.method == 'OPTIONS':
        resp = app.make_default_options_response()

        headers = None
        if 'ACCESS_CONTROL_REQUEST_HEADERS' in request.headers:
            headers = request.headers['ACCESS_CONTROL_REQUEST_HEADERS']

        h = resp.headers

        # Allow the origin which made the XHR
        h['Access-Control-Allow-Origin'] = request.headers['Origin']
        # Allow the actual method
        h['Access-Control-Allow-Methods'] = request.headers['Access-Control-Request-Method']
        # Allow for 10 seconds
        h['Access-Control-Max-Age'] = "10"

        # We also keep current headers
        if headers is not None:
            h['Access-Control-Allow-Headers'] = headers

        return resp


@app.after_request
def set_allow_origin(resp):
    """ Set origin for GET, POST, PUT, DELETE requests """

    h = resp.headers

    # Allow crossdomain for other HTTP Verbs
    if request.method != 'OPTIONS' and 'Origin' in request.headers:
        h['Access-Control-Allow-Origin'] = request.headers['Origin']

    return resp




@app.route('/')
def api_root():
  return 'Welcome'

@app.route('/getIdle')
def getIdleTime():
  cpu = request.args.get('cpu')
  initialize_util()
  res = idleStats(cpu)
  val = {"label":"cpu"+cpu , "data":[]}
  #print res
  val["data"] = res["cpu"+cpu]
  return json.dumps(val)
  

app.run(host='127.0.0.1' ,threaded=True , port=1234)
