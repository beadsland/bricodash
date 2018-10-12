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

import os
import sys
import requests
import json
import dateutil.parser
import re

def main():
  pwd = os.path.dirname(sys.argv[0])
  sig_file = ".keys/meetup_hacktoberfest"
  with open('/'.join([pwd, sig_file])) as x: sig = x.read().rstrip()
  query = "https://api.meetup.com/find/upcoming_events?photo-host=public&page=20&text=Hacktoberfest&sig_id=1998556&radius=5"
  query = query + sig

  response = requests.get(query)
  if response.status_code != 200:   sys.exit(response.status_code)
  result = json.loads(response.text)
  events = result['events']


  pwd = os.path.dirname(sys.argv[0])
  sig_file = ".keys/meetup_hacktober"
  with open('/'.join([pwd, sig_file])) as x: sig = x.read().rstrip()
  query = "https://api.meetup.com/find/upcoming_events?photo-host=public&page=20&text=Hacktober&sig_id=1998556&radius=5"
  query = query + sig

  response = requests.get(query)
  if response.status_code != 200:   sys.exit(response.status_code)
  result = json.loads(response.text)
  events = events + result['events']

  def logoit(l): return '<img class="logo" src="' + l + '">'
  def dateit(e): return " ".join([ e['local_date'], e['local_time'] ])
  def nameit(e): return u"".join([ e['name'].strip(), " ",
                                   logoit("img/tober.png"), " (",
                                   e['group']['name'].strip(), " ",
                                   logoit("img/meetup.png") + ")" ])

  events = [ { "start": dateit(e), "event": nameit(e), "venue": "Holiday" } for e in events ]
  events = [ (dateutil.parser.parse(e["start"]), e["event"], e["venue"]) for e in events ]
  events.sort()
  events = [ {"start": e[0].isoformat(), "event": e[1], "venue": e[2]} for e in events ]

  filename = pwd + "/../html/pull/tober.json"
  file = open(filename + ".new", "w")
  file.write( json.dumps(events) )
  os.rename(filename + ".new", filename)
