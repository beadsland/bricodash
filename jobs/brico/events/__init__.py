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
import brico.common
import brico.common.html as html
import brico.common.meetup
from vend.memoize import memoized

def noisy(s):
  return html.span().clss("noisy").inner(s).str() \
       + html.span().clss("noisemoji").inner(u"🔊🎶").str()

###
# Events of other building tenants
###
def building():
  list = []
  for file in ["brite.json", "upmeet.json"]:
    path = os.path.join(brico.common.pull(), file)
    with open(path) as f: list = list + json.load(f)

  d = datetime.date.today()
  while d.weekday() != 4:     d += datetime.timedelta(1)
  list.append( { "start": " ".join( [d.isoformat(), "8:00 pm"] ),
                 "event": noisy("Friday Night Live Music"),
                 "venue": "Offside Tavern" } )

  return list

###
# Events relevant to our community
###
def community():
  list = []
  for file in ["space.json", "holiday.json", "tober.json"]:
    path = os.path.join(brico.common.pull(), file)
    with open(path) as f: list = list + json.load(f)
  return list

###
# Cron job
###
def main():
  pwd = brico.common.pwd()
  ratpark = building() + community()

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
