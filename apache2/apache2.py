#!/usr/bin/python
import requests
import sys
import re
import os
import json
import time

template = ["accesses", "kbytes", "cpuloads", "uptime", "avgreq", "avgbytes", "avgreqbytes", "busyworkers", "idleworkers", "totalslots"]
'''
Total Accesses:
Total kBytes:
CPULoad:
Uptime:
ReqPerSec:
BytesPerSec:
BytesPerReq:
BusyWorkers:
IdleWorkers:
ConnsTotal:
ConnsAsyncWriting:
ConnsAsyncKeepAlive:
ConnsAsyncClosing:
'''
status = ''
appname = 'apache'
cache = '/tmp/zabbix-{0}.json'
def get_cache_file(cache_file, ttl = 55, **args):
    base = {}
    if os.path.exists(cache_file) and time.time() - os.path.getmtime(cache_file) < ttl:
        response = json.load(open(cache_file, 'r'))
        response['cache'] = 'read: ' + cache_file
        return response
    else:
        try:
                response = requests.get(args['url'] + "?auto")
                arrayVariable = re.findall(r"[\.0-9]+", response.content)
                base = dict(zip(template, arrayVariable))
                base['ping'] = 'ok'
                try:
                        json.dump(base, open(cache_file, 'w'))
                        base['cache'] = 'write: ' + cache_file
                except IOError:
                        base['cache'] = 'Permission denied: ' + cache_file
        except requests.exceptions.ConnectionError:
                base['ping'] = 'Invalid url'
        return base
try:
        url = sys.argv[2]
        arguments = sys.argv[1]
        cache_file = cache.format(appname)
        response = get_cache_file(cache_file, url=url)
        status = response[arguments]
except IndexError:
        status = "empty argument"
except KeyError:
        pass
print(status)


