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
import sys
import time

import brico.cloud

def main():
  query = "https://api.github.com/users/hackmanhattan/events?page="

  seen = []
  report = []
  glogo = "%s%s" % (brico.common.html.logo("img/github.png"), '&thinsp;')

  for p in range(1,10):
    cache = "github_hm_%02d.json" % p
    try:
      old = json.loads(brico.common.slurp(cache))
      etag = old['etag']
    except:
      etag = None

    response = brico.common.get_response(query + str(p), etag=etag)
    if response.status_code == 304:
      result = old['result']
    else:
      result = json.loads(response.text)
      etag = response.headers['ETag'] #[3:-1]   # arrives as: 'W/"(.*)"''
      print(etag)
      save = { 'etag': etag, 'result': result }
      brico.common.write_json(cache, save)

    print(response.headers['X-RateLimit-Remaining'])
    try:
      sleep = int(response.headers['X-Poll-Interval'])
    except:
      sleep = 1
    time.sleep(sleep)

    for push in result:
      if push["repo"]["name"] not in seen:
        repo = push["repo"]["name"].replace("hackmanhattan/", "")
        title = glogo + repo
        html = brico.cloud.line(title)
        report.append( (push["created_at"], html) )
        seen.append( push["repo"]["name"] )

  brico.common.write_json("github.json", report)
  return report
