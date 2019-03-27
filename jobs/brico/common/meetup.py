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
import datetime
import time

import brico.common
from vend.memoize import memoized

API = "https://api.meetup.com"

@memoized
def events(group, count=20):
  path = "/".join([API , group, "events" ])
  params = { 'sign': "true", 'photo-host': "public", 'page': count }
  response = brico.common.get_response(path, params)
  return json.loads(response.text)

@memoized
def rsvps(group, eid):
  path = "/".join([ API, group, "events", eid, "rsvps" ])
  response = brico.common.get_response(path)
  return json.loads(response.text)

@memoized
def find(text, sigfile):
  path = "/".join([ API, "find", "upcoming_events" ])
  params = { 'photo-host': "public", 'page': 20, 'text': text, 'radius': 5,
             'lat': brico.common.lat(), 'lon': brico.common.lon() }
  sigfile = os.path.join( brico.common.pwd(), sigfile )
  with open(sigfile) as x: sig = x.read().rstrip()

  response = brico.common.get_response(path, params, sig)
  result = json.loads(response.text)
  return result['events']

def photos(group, offset=0):
  file = "meetup_photos.json"

  diff = (datetime.datetime.now() - brico.common.mtime(file))
  if diff < datetime.timedelta(minutes = 15):
    result = json.loads(brico.common.slurp(file))
  else:
    page = 200
    path = "/".join([ API, group, "photos" ])
    params = { 'sign': "true", 'photo-host': "public",
               'page': page, 'offset': offset  }
    response = brico.common.get_response(path, params)

    if ((offset+1)*page) < int(response.headers['X-Total-Count']):
      time.sleep(1)
      result = json.loads(response.text) + photos(group, offset+1)
    else:
      result = json.loads(response.text)

    brico.common.write_json(file, result)

  return result
