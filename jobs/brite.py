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

from eventbrite import Eventbrite
import os
import sys
import re
import json
import dateutil.parser
import brico.common.html as html
from brico.common.short import shorten

pwd = os.path.dirname(sys.argv[0])
token_file = ".keys/eventbrite_token"
with open('/'.join([pwd, token_file])) as x: token = x.read().rstrip()
eventbrite = Eventbrite(token)

venues = {}
ratpark = []

def noisy(s):
  return html.span().clss('noisy').inner(s).str() \
         + html.span().clss('noisemoji').inner(u"🔊🎶").str()

def short(s):
  h = shorten(s).replace("https://", "", 1).split("/")
  s1 = "%s%s" % (h[1], html.a().src(s).inner("🔗").str())
  return html.span().clss('thiny').inner("%s/" % h[0]).str() \
         + html.span().clss('shorty').inner(s1).str()

query = '/events/search?q=Secret Loft&location.address=137 West 14th Street, New York, NY&location.within=1km&sort_by=date'
result = eventbrite.get(query)
events = result['events']

query = '/events/search?q=Offside Tavern&location.address=137 West 14th Street, New York, NY&location.within=1km&sort_by=date'
result = eventbrite.get(query)
events = events + result['events']

for event in events:
  if event['venue_id'] not in venues:
    venues[event['venue_id']] = eventbrite.get('/venues/' + event['venue_id'])
  venue = venues[event['venue_id']]
  if venue['name'] == "Offside Tavern" or venue['name'] == "Secret Loft":
    name = event['name']['text']
    name = name.replace("at Secret Loft", "")
    name = name.replace("at Offside Tavern", "")
    ratpark.append( {"start": event['start']['local'],
                     "venue": venue['name'],
                     "event": "%s %s" % (noisy(name), short(event['url'])) } )

ratpark = [ (dateutil.parser.parse(e["start"]), e["event"], e["venue"]) for e in ratpark ]
ratpark.sort()
ratpark = [ {"start": e[0].isoformat(), "event": e[1], "venue": e[2]} for e in ratpark ]

filename = pwd + "/../html/pull/brite.json"
file = open(filename + ".new", "w")
file.write( json.dumps(ratpark[:5]) )
os.rename(filename + ".new", filename)
