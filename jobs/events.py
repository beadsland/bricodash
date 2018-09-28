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

import json
import requests
import dateparser
import humanize
import re
import os
import json
import sys
import time
import datetime
import calendar
import dateutil.parser


pwd = os.path.dirname(sys.argv[0])
filename = pwd + "/../html/pull/brite.json"
with open(filename) as f: brite = json.load(f)

filename = pwd + "/../html/pull/upmeet.json"
with open(filename) as f: upmeet = json.load(f)

filename = pwd + "/../html/pull/holiday.json"
with open(filename) as f: holiday = json.load(f)

ratpark = brite + upmeet + holiday;

d = datetime.date.today()
while d.weekday() != 4:
  d += datetime.timedelta(1)
def noisy(s): return '<span class="noisy">' + s + '</span> <span class="noisemoji">' + u"🔊🎶" + "</span>"
ratpark.append( { "start": " ".join( [d.isoformat(), "8:00 pm"] ),
                  "event": noisy("Friday Night Live Music"), "venue": "Offside Tavern" } )


sig_file = ".keys/meetup_events"
with open('/'.join([pwd, sig_file])) as x: sig = x.read().rstrip()
query = "https://api.meetup.com/HackManhattan/events?photo-host=public&page=20&"
query = query + sig

response = requests.get(query)
if response.status_code != 200:   sys.exit(response.status_code);
data = json.loads(response.text)


maths = requests.get("https://api.meetup.com/nyc-math/events?&sign=true&photo-host=public&page=20")
maths = json.loads(maths.text)
maths = { e["name"]: (e["yes_rsvp_count"], e["id"]) for e in maths }

today = datetime.date.today()
lasttuesday = max( week[calendar.TUESDAY]
                   for week in calendar.monthcalendar(today.year, today.month) )

for item in data[:8]:
  dt = dateparser.parse(item['local_date'] + " " + item['local_time'])

  evt = item['name']
  evt = re.sub(r' at Hack Manhattan', '', evt)
  if (dt.day == lasttuesday) and (dt.month == today.month):
    evt = re.sub(r'(Tech Tuesday)', r'\1 / General Meeting', evt)
  evt = re.sub(r'(Open House)', r'\1 <img class="logo" src="img/balloons.png">', evt)
  evt = re.sub(r'(Fixers\' Collective)', r'\1 <img class="logo" src="img/fixers.png">', evt)
  if evt.startswith("Shakespeare Night"): evt += ' <span class="emoji">🎭📖</span>'
  evt = re.sub(r'freeCodeCamp', '<img style="height:1.05em; vertical-align: bottom;" src="img/freeCodeCamp.png">', evt)
  evt = re.sub(r'(Midnight Games)', r'\1 <span class="emoji">🌌🎲</span>', evt)

  if evt in maths:
    rsvp = item['yes_rsvp_count'] + maths[evt][0] - 2
    req = [ "http://api.meetup.com/hackmanhattan/events/" + item["id"] + "/rsvps",
            "http://api.meetup.com/nyc-math/events/" + maths[evt][1] + "/rsvps" ]
    rsvps = {};
    for r in req:
      resp = requests.get(r)
      if resp.status_code != 200:   sys.exit(resp.status_code);
      for ans in json.loads(resp.text):
        id = ans["member"]["id"]
        if id in rsvps and rsvps[id] > ans["guests"]:
          pass
        elif ans["response"] == "yes":
          rsvps[id] = ans["guests"]
    rsvp = len(rsvps) + sum(rsvps.values())
    evt += ' <img class="logo" src="img/math.png">'
  else:
    rsvp = item['yes_rsvp_count']

  ratpark.append( { "start": dt.isoformat(), "event":  evt,
                    "venue": "Hack Manhattan", "rsvp": rsvp } )

ratpark = [ (dateutil.parser.parse(e["start"]), e["event"], e["venue"],
                                   e["rsvp"] if "rsvp" in e else 0) for e in ratpark ]
ratpark.sort()
ratpark = [ {"start": e[0].isoformat(), "event": e[1], "venue": e[2], "rsvp": e[3]} for e in ratpark ]

def wdv(s): return "<span class='venue'>%s</span>" % (s)
def wdt(s): return "<span class='date'>%s</span>" % (s)
def wdd(s): return "<span class='event'>%s</span>" % (s)
def wddhm(s): return "<span class='hm-event'>%s</span>" % (s)
def evt(s): return "<div class='event-line'>%s</div>" % (s)

evtSpce = []
evtBldg = []

evtBldg.append( wdd('<span id="ratparkHdr">Rat Park Building Calendar</span>') )

for item in ratpark:
  dt = dateutil.parser.parse(item["start"])
  today = datetime.datetime.combine(datetime.date.today(), datetime.datetime.min.time())
  if (today + datetime.timedelta(days=2,seconds=-1)) \
                                < dt < (today + datetime.timedelta(days=7)):
    date = dt.strftime('%a')
  else:
    date = humanize.naturalday(dt)

  start = dt.strftime("%-I:%M %p").lower()
  start = re.sub(r':00', '', start)
  dt = "%s, %s" % (date, start) if start != "12 am" else date

  dd = item["event"];
  if item["rsvp"] > 4:  dd += " (%s)" % item["rsvp"]

  if item["venue"] == "Hack Manhattan":
    evtSpce.append( evt("%s &mdash; %s" % (wdt(dt), wddhm(dd)) ) )
    evtBldg.append( evt ("%s %s &mdash; %s") % (wdv(item["venue"]),
                                                wdt(dt), wddhm(dd) ) )
  elif item["venue"] == "Holiday":
    evtSpce.append( evt("%s &mdash; %s" % (wdt(dt), wdd(dd)) ) )
  else:
    evtBldg.append( evt ("%s %s &mdash; %s") % (wdv(item["venue"]),
                                                wdt(dt), wdd(dd) ) )

evtSpce = evtSpce[:10]
evtBldg = evtBldg[:10]
evtSpce.append( '<span id="timestamp" epoch="' + str(time.time()) + '"></span>' )
evtBldg.append( '<span id="timestamp" epoch="' + str(time.time()) + '"></span>' )

filename = pwd + "/../html/pull/space_events.html"
file = open(filename + ".new", "wb")
file.write( u"\n".join(evtSpce[:11]).encode('utf-8') )
os.rename(filename + ".new", filename)

filename = pwd + "/../html/pull/building_events.html"
file = open(filename + ".new", "wb")
file.write( u"\n".join(evtBldg[:11]).encode('utf-8') )
os.rename(filename + ".new", filename)
