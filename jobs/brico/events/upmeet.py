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
import datetime
import dateutil.parser
import re

def main():
  pwd = os.path.dirname(sys.argv[0])
  sig_file = ".keys/meetup_upmeet"
  with open('/'.join([pwd, sig_file])) as x: sig = x.read().rstrip()
  query = "https://api.meetup.com/find/upcoming_events?photo-host=public&page=1000&radius=1&lon=-74.000549&lat=40.7383046&"
  query = query + sig

  response = requests.get(query)
  if response.status_code != 200:   sys.exit(response.status_code);
  result = json.loads(response.text)
  events = result['events']

  ratpark = []

  def meetup(s): return s + ' <img class="logo" src="img/meetup.png">'

  for event in events:
    if "venue" in event and event['venue']['name'] == "Offside Tavern":
      name = event['name']
      name = re.sub(' Wednesday! FREE!', ' Wed!', name)
      ratpark.append( { "start": " ".join( [event['local_date'], event['local_time']] ),
                        "event": meetup(name), "venue": "Offside Tavern" } )

  ratpark = [ (dateutil.parser.parse(e["start"]), e["event"], e["venue"]) for e in ratpark ]
  ratpark.sort()
  ratpark = [ {"start": e[0].isoformat(), "event": e[1], "venue": e[2]} for e in ratpark ]

  filename = pwd + "/../html/pull/upmeet.json"
  file = open(filename + ".new", "w")
  file.write( json.dumps(ratpark) )
  os.rename(filename + ".new", filename)
