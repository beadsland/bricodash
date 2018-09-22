#!/usr/bin/env python

import requests
import json
import os
import sys
import time

query = "https://wiki.hackmanhattan.com/api.php?action=query&list=recentchanges&rcprop=title%7Cids%7Csizes%7Cflags%7Cuser&rclimit=200&rcshow=!minor&format=json"
response = requests.get(query)
if response.status_code != 200:   sys.exit(response.status_code);
result = json.loads(response.text)

recent = result["query"]["recentchanges"]
seen = []
report = []

for edit in recent:
  if edit["title"] not in seen:
    path = edit["title"].split("/")
    for i in range(len(path)):
      if path[i].find(":") > -1:
        path[i] = '<span class="wiki-special">' + path[i] + "</span>"
    report.append( "/&#x200a;".join(path) )
    seen.append( edit["title"] )

report = list( ('<div class="wiki-line">' + e + "</div>" for e in report) )
report = list( reversed(report[:15]) )

report.append( '<span id="timestamp" epoch="' + str(time.time()) + '"></span>' )

pwd = os.path.dirname(sys.argv[0])
filename = pwd + "/../html/pull/wiki.html"
file = open(filename + ".new", "w")
file.write( u"\n".join(report) )
os.rename(filename + ".new", filename)
