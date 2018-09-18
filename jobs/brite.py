#!/usr/bin/env python

from eventbrite import Eventbrite
import os
import sys
import re

pwd = os.path.dirname(sys.argv[0])
token_file = ".keys/eventbrite_token"
with open('/'.join([pwd, token_file])) as x: token = x.read().rstrip()
eventbrite = Eventbrite(token)

venues = {}

for page in range(1,30):
  print page
  result = eventbrite.get('/events/search?location.address=137 West 14th Street, New York, NY&location.within=1km&sort_by=date&page=' + str(page))
  print result.keys()
  events = result['events']

  for event in events:
    if event['venue_id'] not in venues:
      venues[event['venue_id']] = eventbrite.get('/venues/' + event['venue_id'])
    venue = venues[event['venue_id']]
    if venue['name'] == "Offside Tavern" or venue['name'] == "Secret Loft":
      print "-----"
      print event['start']
      print event['name']
      print venue['name']
