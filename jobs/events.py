#!/usr/bin/env python

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
filename = pwd + "/../html/pull/ratpark.json"
with open(filename) as f: ratpark = json.load(f)

sig_file = ".keys/meetup_events"
with open('/'.join([pwd, sig_file])) as x: sig = x.read().rstrip()
query = "https://api.meetup.com/HackManhattan/events?photo-host=public&page=20&"
query = query + sig

response = requests.get(query)
if response.status_code != 200:   sys.exit(response.status_code);
data = json.loads(response.text)


today = datetime.date.today()
lasttuesday = max( week[calendar.TUESDAY]
                   for week in calendar.monthcalendar(today.year, today.month) )

for item in data[:8]:
  dt = dateparser.parse(item['local_date'] + " " + item['local_time'])

  evt = item['name']
  evt = re.sub(r' at Hack Manhattan', '', evt)
  if (dt.day == lasttuesday) and (dt.month == today.month):
    evt = re.sub(r'(Tech Tuesday)', r'\1 / General Meeting', evt)

  ratpark.append( { "start": dt.isoformat(), "event":  evt,
                    "venue": "Hack Manhattan", "rsvp": item['yes_rsvp_count'] } )

ratpark = [ (dateutil.parser.parse(e["start"]), e["event"], e["venue"],
                                   e["rsvp"] if "rsvp" in e else 0) for e in ratpark ]
ratpark.sort()
ratpark = [ {"start": e[0].isoformat(), "event": e[1], "venue": e[2], "rsvp": e[3]} for e in ratpark ]

def wdv(s): return "<span class='venue'>%s</span>" % (s)
def wdt(s): return "<span class='date'>%s</span>" % (s)
def wdd(s): return "<span class='event'>%s</span>" % (s)
def evt(s): return "<div class='event-line'>%s</div>" % (s)

evtSpce = []
evtBldg = []

evtBldg.append( wdd('<span id="ratparkHdr">Rat Park Building Calendar</span>') )

for item in ratpark:
  dt = dateutil.parser.parse(item["start"])
  date = humanize.naturalday(dt)
  start = dt.strftime("%-I:%M %p").lower()
  start = re.sub(r':00', '', start)
  dt = "%s, %s" % (date, start)

  dd = item["event"];
  if item["rsvp"] > 4:  dd += " (%s)" % item["rsvp"]

  if item["venue"] == "Hack Manhattan":
    evtSpce.append( evt("%s &mdash; %s" % (wdt(dt), wdd(dd)) ) )
  evtBldg.append( evt ("%s %s &mdash; %s") % (wdv(item["venue"]),
                                              wdt(dt), wdd(dd) ) )

evtSpce.append( '<span id="timestamp" epoch="' + str(time.time()) + '"></span>' )
evtBldg.append( '<span id="timestamp" epoch="' + str(time.time()) + '"></span>' )

filename = pwd + "/../html/pull/space_events.html"
file = open(filename + ".new", "w")
file.write( "\n".join(evtSpce) )
os.rename(filename + ".new", filename)

filename = pwd + "/../html/pull/building_events.html"
file = open(filename + ".new", "w")
file.write( "\n".join(evtBldg) )
os.rename(filename + ".new", filename)
