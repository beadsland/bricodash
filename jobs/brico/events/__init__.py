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

import brico.common
import brico.common.html as html
from vend.memoize import memoized

import os
import json
import dateutil
import datetime
import humanize
import re

@memoized
def noisemoji(): return html.span().clss("noisemoji").inner(u"🔊🎶").str()
def noisy(s): return html.span().clss("noisy").inner( s ).str() + noisemoji()

@memoized
def venue(s): return html.span().clss('venue').inner( s ).str()
def line(s): return html.div().clss('event-line').inner( s ).str()

###
# Events of other building tenants
###
def building():
  list = []
  for file in ["space.json", "brite.json", "upmeet.json"]:
    path = os.path.join(brico.common.pull(), file)
    with open(path) as f: list = list + json.load(f)

  d = datetime.date.today()
  while d.weekday() != 4:     d += datetime.timedelta(1)
  list.append( { "start": " ".join( [d.isoformat(), "8:00 pm"] ),
                 "event": noisy("Friday Night Live Music"),
                 "venue": "Offside Tavern" } )

  return datesort(list)

###
# Events relevant to our community
###
def community():
  list = []
  for file in ["space.json", "holiday.json", "tober.json"]:
    path = os.path.join(brico.common.pull(), file)
    with open(path) as f: list = list + json.load(f)
  return datesort(list)

###
# Sort event list by date
###
def datesort(list):
  list = [ (dateutil.parser.parse(e["start"]),
           e["event"],
           e["venue"],
           e["rsvp"] if "rsvp" in e else 0) for e in list ]
  list.sort()
  list = [ {"start": e[0].isoformat(),
            "event": e[1],
            "venue": e[2],
            "rsvp": e[3]} for e in list ]
  return list

###
# Format each event line
###
def format(item):
  dt = format_dt(item["start"])

  dd = item['event']
  if item['rsvp'] > 4:  dd += " (%s)" % item['rsvp']
  if item['venue'] == "Hack Manhattan":
    dd = html.span().clss('hm-event').inner( dd ).str()
  else:
    dd = html.span().clss('event').inner( dd ).str()

  return " &mdash; ".join([ html.span().clss('date').inner( dt ).str(),
                            dd ])

@memoized
def format_dt(start):
  dt = dateutil.parser.parse(start)
  today = datetime.datetime.combine(datetime.date.today(),
                                    datetime.datetime.min.time())
  if (today + datetime.timedelta(days=2,seconds=-1)) \
                                < dt < (today + datetime.timedelta(days=7)):
    date = dt.strftime('%a')
  else:
    date = humanize.naturalday(dt)

  start = dt.strftime("%-I:%M %p").lower()
  start = re.sub(r':00', '', start)
  return "%s, %s" % (date, start) if start != "12 am" else date
