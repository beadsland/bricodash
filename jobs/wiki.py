#!/usr/bin/env python3

####
## Copyright © 2018 Beads Land-Trujillo.
##
## This program is free software: you can redistribute it and/or modify
## it under the terms of the GNU Affero General Public License as published
## by the Free Software Foundation, either version 3 of the License, or
## (at your option) any later version.
##
## This program is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU Affero General Public License for more details.
##
## You should have received a copy of the GNU Affero General Public License
## along with this program.  If not, see <https://www.gnu.org/licenses/>.
####

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
wlogo = '<img class="logo" src="img/mediawiki.png">&thinsp;'
glogo = '<img class="logo" src="img/github.png">&thinsp;'

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
report = list(s for (t,s) in report)[-10:]

report.append( '<span id="timestamp" epoch="' + str(time.time()) + '"></span>' )

pwd = os.path.dirname(sys.argv[0])
filename = pwd + "/../html/pull/wiki.html"
file = open(filename + ".new", "w")
file.write( u"\n".join(report) )
os.rename(filename + ".new", filename)
