#!/usr/bin/env python3

from eventbrite import Eventbrite
import os
import sys
import re
import json

pwd = os.path.dirname(sys.argv[0])
token_file = ".keys/eventbrite_token"
with open('/'.join([pwd, token_file])) as x: token = x.read().rstrip()
eventbrite = Eventbrite(token)

venues = {}
ratpark = []

def noisy(s): return '<span class="noisy">' + s + '</span> <span class="emoji">' + u"🔊🎶" + "</span>"

for page in range(1,20):
  query = '/events/search?location.address=137 West 14th Street, New York, NY&location.within=1km&sort_by=date&page='
  result = eventbrite.get(query + str(page))
  events = result['events']

  for event in events:
    if event['venue_id'] not in venues:
      venues[event['venue_id']] = eventbrite.get('/venues/' + event['venue_id'])
    venue = venues[event['venue_id']]
    if venue['name'] == "Offside Tavern" or venue['name'] == "Secret Loft":
      ratpark.append( {"start": event['start']['local'], "venue": venue['name'], "event": noisy(event['name']['text'])} )

  if len(ratpark) > 2: break

filename = pwd + "/../html/pull/brite.json"
file = open(filename + ".new", "w")
file.write( json.dumps(ratpark) )
os.rename(filename + ".new", filename)
