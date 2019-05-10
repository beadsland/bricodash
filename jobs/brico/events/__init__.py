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
def polite(s): return re.sub('/', "/&thinsp;", re.sub('…', "…&thinsp;", s))

@memoized
def venue(s): return html.span().clss('venue').inner( s ).str()
def line(s): return html.div().clss('event-line').inner( s ).str()

###
# Events of other building tenants
###
def building():
  list = load_cals([ "space.json", "private.json", "brite.json", "upmeet.json" ])
  list = list + livemusic()
  return datesort(list)

###
# Events relevant to our hackerspace
###
def ourspace():
  cals = datesort(load_cals([ "space.json", "private.json" ]))
  geek = datesort(load_cals([ "geekday.json" ]))[:4]
  week = datetime.datetime.now() + datetime.timedelta(days = 6, hours = 18)
  week = week.isoformat().replace("T", " ")
  while len(geek) > 0 and cals[6]['start'] > week:
    cals = datesort( cals + [geek.pop(0)] )
  return cals

###
# Events relevant to broader community
###
def community():
  cals = [ "multi.json", "castles.json", "tober.json", "holiday.json",
            "space.json", "private.json", "brite.json", "upmeet.json" ]
  return datesort( datesort( load_cals(cals) + livemusic() ) )

###
# Combined calendar for next three days
###
def combo():
  list = load_cals([ "space.json", "private.json", "brite.json",
                     "upmeet.json", "multi.json", "castles.json",
                     "tober.json", "holiday.json", "geekday.json" ])
  list = list + livemusic()
  return datesort(list)

###
# This weekly event is rarely listed on Eventbrite or Meetup
###
def livemusic():
  d = datetime.date.today()
  while d.weekday() != 4:     d += datetime.timedelta(1)
  start7 = dateutil.parser.parse(" ".join( [d.isoformat(), "7:00 pm"] ))
  start8 = dateutil.parser.parse(" ".join( [d.isoformat(), "8:00 pm"] ))

  for b in brico.events.load_cals( ["brite.json"] ):
    bstart = dateutil.parser.parse(b['start'])
    if ("Friday Night Live" in b['event'] or "Friday Nights Live" in b['event']) \
          and (bstart == start7 or bstart == start8):
      return []

  return [{ "start": start8.isoformat(), "event": noisy("Friday Night Live Music"),
            "venue": "Offside Tavern" }]

###
# Load a list of calendars
###
def load_cals(files):
  list = []
  for file in files:
    path = os.path.join(brico.common.pull(), file)
    with open(path) as f: list = list + json.load(f)
  return list

###
# Sort event list by date
###
def datesort(list):
  list = [ (dateutil.parser.parse(e["start"]),
           e["event"],
           e["venue"],
           e["rsvp"] if "rsvp" in e else 0) for e in list ]
  list.sort()
  patt = "%Y-%m-%d %H:%M"
  list = [ {"start": (e[0] + datetime.timedelta(seconds=30)).strftime(patt),
            "event": e[1],
            "venue": e[2],
            "rsvp": e[3]} for e in list ]
  return list

###
# Format each event line
###
def format(item, clss='event'):
  dt = format_dt(item["start"])

  dd = item['event']
  if item['rsvp'] > 4:  dd += " (%s)" % item['rsvp']
  if item['venue'] == "Hack Manhattan":
    dd = "%s %s" % ( dd, html.logo("img/hm_neg.png") )
    dd = html.span().clss('hm-event').inner( dd ).str()
  else:
    dd = html.span().clss(clss).inner( dd ).str()

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
  date = re.compile(r' 0').sub(' ', date)

  start = dt.strftime("%-I:%M %p").lower()
  start = re.compile(r':00').sub('', start)
  return "%s, %s" % (date, start) if start != "12 am" else date
