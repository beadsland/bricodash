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
import brico.common.html as html
from brico.common.short import shorten

pwd = os.path.dirname(sys.argv[0])
token_file = ".keys/eventbrite_token"
with open('/'.join([pwd, token_file])) as x: token = x.read().rstrip()
eventbrite = Eventbrite(token)

venues = {}
ratpark = []

def noisy(s): return html.span().clss('noisy').inner(s).str() \
                     + html.span().clss('noisemoji').inner(u"🔊🎶").str()

def shortest(s): return shorten(s).replace("https://", "", 1)
def short(s): return html.span().clss('shorty').inner(shortest(s)).str()

for page in range(1,20):
  query = '/events/search?location.address=137 West 14th Street, New York, NY&location.within=1km&sort_by=date&page='
  result = eventbrite.get(query + str(page))
  events = result['events']

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

  if len(ratpark) > 2: break

filename = pwd + "/../html/pull/brite.json"
file = open(filename + ".new", "w")
file.write( json.dumps(ratpark) )
os.rename(filename + ".new", filename)
