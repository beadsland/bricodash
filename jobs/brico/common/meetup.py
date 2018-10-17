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
import json
import brico.common
from vend.memoize import memoized

@memoized
def grp(): return "HackManhattan"

@memoized
def events(group):
  path = "/".join([ "https://api.meetup.com", group, "events" ])
  params = { 'sign': "true", 'photo-host': "public", 'page': 20 }
  response = brico.common.get_response(path, params)
  return json.loads(response.text)

@memoized
def rsvps(group, eid):
  path = "/".join([ "https://api.meetup.com", group, "events", eid, "rsvps" ])
  response = brico.common.get_response(path)

@memoized
def find(text, sigfile):
  path = "https://api.meetup.com/find/upcoming_events"
  params = { 'photo-host': "public", 'page': 20, 'text': text, 'radius': 5,
             'lat': brico.common.lat(), 'lon': brico.common.lon() }
  sigfile = os.path.join( brico.common.pwd(), sigfile )
  with open(sigfile) as x: sig = x.read().rstrip()

  response = brico.common.get_response(path, params, sig)
  result = json.loads(response.text)
  return result['events']
