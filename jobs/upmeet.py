#!/usr/bin/env python

import os
import sys
import requests
import json
import datetime
import dateutil.parser
import re

pwd = os.path.dirname(sys.argv[0])
filename = pwd + "/../html/pull/brite.json"
with open(filename) as f: ratpark = json.load(f)

sig_file = ".keys/meetup_upmeet"
with open('/'.join([pwd, sig_file])) as x: sig = x.read().rstrip()
query = "https://api.meetup.com/find/upcoming_events?photo-host=public&page=1000&radius=1&lon=-74.000549&lat=40.7383046&"
query = query + sig

response = requests.get(query)
if response.status_code != 200:   sys.exit(response.status_code);
result = json.loads(response.text)
events = result['events']

for event in events:
  if "venue" in event and event['venue']['name'] == "Offside Tavern":
    name = event['name']
    name = re.sub(' FREE!', '', name)
    ratpark.append( { "start": " ".join( [event['local_date'], event['local_time']] ),
                      "event": name, "venue": "Offside Tavern" } )

d = datetime.date.today()
while d.weekday() != 4:
  d += datetime.timedelta(1)
ratpark.append( { "start": " ".join( [d.isoformat(), "8:00 pm"] ),
                  "event": "Friday Night Live Music", "venue": "Offside Tavern" } )

ratpark = [ (dateutil.parser.parse(e["start"]), e["event"], e["venue"]) for e in ratpark ]
ratpark.sort()
ratpark = [ {"start": e[0].isoformat(), "event": e[1], "venue": e[2]} for e in ratpark ]

filename = pwd + "/../html/pull/ratpark.json"
file = open(filename + ".new", "w")
file.write( json.dumps(ratpark) )
os.rename(filename + ".new", filename)
