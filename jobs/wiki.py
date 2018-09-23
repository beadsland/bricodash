#!/usr/bin/env python

import requests
import json
import os
import sys
import time

query = "https://wiki.hackmanhattan.com/api.php?action=query&list=recentchanges&rcprop=title%7Cids%7Csizes%7Cflags%7Cuser%7Ctimestamp&rclimit=200&rcshow=!minor&format=json"
response = requests.get(query)
if response.status_code != 200:   sys.exit(response.status_code);
result = json.loads(response.text)

recent = result["query"]["recentchanges"]
seen = []
report = []
wlogo = '<img class="logo" src="img/mediawiki.png">'
glogo = '<img class="logo" src="img/github.png">'

for edit in recent:
  if edit["title"] not in seen:
    path = edit["title"].split("/")
    for i in range(len(path)):
      if path[i].find(":") > -1:
        path[i] = '<span class="wiki-special">' + path[i] + "</span>"
    title = wlogo + "/&#x200a;".join(path)
    html = '<div class="wiki-line">' + title + "</div>"
    report.append( (edit["timestamp"], html) )
    seen.append( edit["title"] )

query = "https://api.github.com/users/hackmanhattan/events?page="

for p in range(1,10):
  response = requests.get(query + str(p))
  if response.status_code != 200:   sys.exit(response.status_code);
  result = json.loads(response.text)
  for push in result:
    if push["repo"]["name"] not in seen:
      repo = push["repo"]["name"].replace("hackmanhattan/", "")
      title = glogo + repo
      html = '<div class="wiki-line">' + title + "</div>"
      report.append( (push["created_at"], html) )
      seen.append( push["repo"]["name"] )

report = sorted(report)
report = list(s for (t,s) in report)[15:]

report.append( '<span id="timestamp" epoch="' + str(time.time()) + '"></span>' )

pwd = os.path.dirname(sys.argv[0])
filename = pwd + "/../html/pull/wiki.html"
file = open(filename + ".new", "w")
file.write( u"\n".join(report) )
os.rename(filename + ".new", filename)
