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
filename = pwd + "/../html/pull/brite.json"
with open(filename) as f: brite = json.load(f)

filename = pwd + "/../html/pull/upmeet.json"
with open(filename) as f: upmeet = json.load(f)

filename = pwd + "/../html/pull/holiday.json"
with open(filename) as f: holiday = json.load(f)

ratpark = brite + upmeet + holiday;

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
def wddhm(s): return "<span class='hm-event'>%s</span>" % (s)
def evt(s): return "<div class='event-line'>%s</div>" % (s)

evtSpce = []
evtBldg = []

evtBldg.append( wdd('<span id="ratparkHdr">Rat Park Building Calendar</span>') )

for item in ratpark:
  dt = dateutil.parser.parse(item["start"])
  today = datetime.datetime.combine(datetime.date.today(), datetime.datetime.min.time())
  if (today + datetime.timedelta(days=1,seconds=-1)) \
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
file = open(filename + ".new", "w")
file.write( u"\n".join(evtSpce[:11]).encode('utf-8') )
os.rename(filename + ".new", filename)

filename = pwd + "/../html/pull/building_events.html"
file = open(filename + ".new", "w")
file.write( u"\n".join(evtBldg[:11]).encode('utf-8') )
os.rename(filename + ".new", filename)
