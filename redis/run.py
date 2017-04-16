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
  computeCPU()
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

@app.route('/stat')
def getStat():
  system = request.args.get('system')
  #res = systemStat(system)
  res = computeCPU(system)  
  return json.dumps(res)

@app.route('/getLatency')
def getLatencyTime():
  instance_ip = request.args.get('ip')
  res = getLatency()
  res = res[str(instance_ip)]
  data = res["Read"]
  val = {"label":"latency" , "data":[]}
  val["data"] = data
  return json.dumps(val)

@app.route('/memory')
def memory():
  app = request.args.get('ip')
  res = memoryFree()
  res = res[app]
  value1 = res['node_memory_MemTotal'][0]
  value2 = res['node_memory_MemFree'][0]
  val = float(value1)-float(value2)
  return val

@app.route('/clusterStats')
def cluster():
  request_string = "http://10.10.1.71:5050/metrics/snapshot"
  response = requests.get(request_string)
  array = json.loads(response.text)
  print array
  res = { "total_cpus" : array["master/cpus_total"] , "used_cpus" : array["master/cpus_used"] , "total_mem" : array["master/mem_total"] , "used_mem" : array["master/mem_used"]}
  return json.dumps(res)
@app.route('/latency')
def latency():
  return json.dumps(getLatency())

app.run(host='10.10.1.71' ,threaded=True , port=1234)
