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

import brico.events
import brico.events.brite
import brico.events.upmeet
import brico.events.multi
import brico.events.holiday
import brico.events.tober
import brico.events.space
import brico.events.castles
import brico.events.private
import brico.events.lunar
import brico.events.lunar.jewish

import brico.slack
import brico.common.html as html

import datetime
import os
import sys
import re
from vend.multisub import multiple_replace
import importlib
import traceback

###
# Update event source files
###

now = datetime.datetime.now()
min = now.minute
hr  = now.hour

# IMPORTANT:
# This script is fired off at interval specified in sysd/cron.py
# Be sure than any interval defined below will occur coincident with the
# master cron.py interval. Otherwise the rule in question below won't fire.

EXC = True

def trymain(mod):
  try:
    mod = importlib.import_module("brico.events.%s" % mod)
    getattr(mod, 'main')()
  except:
    if EXC:
      exc_info = sys.exc_info()
      traceback.print_exception(*exc_info)
      del exc_info

# Make sure sunset items actually update by firing in passes immediately after
sunset = brico.events.lunar.sunset(datetime.datetime.today())
max_bein_hashmashot = brico.events.lunar.jewish.max_bein_hashmashot()
if datetime.timedelta(seconds=0) \
   < (datetime.datetime.now(datetime.timezone.utc) - sunset) \
   < datetime.timedelta(minutes=30) + max_bein_hashmashot:
                                              trymain("multi")

# Same for sunrise items (e.g., Hindu calendar)
sunrise = brico.events.lunar.sunrise(datetime.datetime.today())
if datetime.timedelta(seconds=0) \
   < (datetime.datetime.now(datetime.timezone.utc) - sunrise) \
   < datetime.timedelta(minutes=30):
                                              trymain("multi")

# Run after yesteray (several times to ensure it happens)
if min < 30 and hr == 0:
                                              trymain("holiday")
                                              trymain("multi")

# Run before thehaps
if min == 50 and hr % 12 == 5 or 'holiday' in sys.argv:
                                              trymain("holiday")
if min == 50 and hr % 12 == 5 or 'multi' in sys.argv:
                                              trymain("multi")

#if min % 60 == 0 or 'upmeet' in sys.argv or 'brite' in sys.argv:
#                                              trymain("brite")
#                                              trymain("upmeet")
#if min % 60 == 0 or 'tober' in sys.argv:      trymain("tober")
if min % 60 == 0 or 'castles' in sys.argv:    trymain("castles")
if min % 10 == 0 or 'space' in sys.argv:      trymain("space")
if min % 60 == 0 or 'private' in sys.argv:
                                              trymain("space")
                                              trymain("private")

###
# Build events component divs
###
evtSpce = []
for item in brico.events.ourspace()[:10]:
  evtSpce.append( brico.events.line(brico.events.format(item)) )

evtCity = []
header = html.span().id('ratparkHdr').inner("NYC / Community Calendar")
evtCity.append( html.span().clss('event').inner(header.str()).str() )

events = brico.events.community()[:10]
for item in events:
  if item['venue'] in ["Offside Tavern", "Secret Loft"]:
    venue = item['venue'].replace(" ", "&nbsp;")
    item['event'] = "%s (%s)" % (item['event'], venue)
    evtCity.append( brico.events.line(brico.events.format(item)) )
  elif item['venue'] == "Local":
    evtCity.append( brico.events.line(brico.events.format(item, 'nys-event')) )
  elif item['venue'] == "Special":
    evtCity.append( brico.events.line(brico.events.format(item, 'nyc-event')) )
  else:
    evtCity.append( brico.events.line(brico.events.format(item)) )

evtBldg = []
header = html.span().id('ratparkHdr').inner("Rat Park — Building Calendar")
evtBldg.append( html.span().clss('event').inner(header.str()).str() )
for item in brico.events.building()[:10]:
  venue = brico.events.venue(item['venue'])
  event = brico.events.format(item)
  evtBldg.append( brico.events.line("%s %s" % (venue, event)) )

###
# Build event list for posting to slack
###
slkThree = ["*_Full 72-Hour Calendar_*"]
three = datetime.datetime.now() + datetime.timedelta(days=3)
three = re.sub('T', ' ', three.isoformat())
combo = brico.events.combo()
for item in combo:
  if item['start'] < three:
    venue = "(%s)" % brico.slack.bold(item['venue'])
    if item['venue'] == "Hack Manhattan": venue = ":hm:"
    elif item['venue'] in ['Holiday', 'Special', 'Local']:    venue = ""
    start = brico.slack.ital( brico.events.format_dt(item['start']) )

    event = item['event']
    event = re.sub(r'</?em\ ?>', "_", event)
    event = re.sub(brico.events.lunar.jewish.unlit(), "\u202F‗\u202F", event)
    event = re.sub(r'<img[^>]+alt="([^"]*)"[^>]+>', r'\1', event)
    event = re.sub(r'<[^>]+>', '', event)

    cleandict = [ ("&mdash;", "—"), ("(Babycastles)", ""),
                  ("&thinsp;", ""), ("&ensp;", " "), ("&nbsp;", " ") ]
    event = multiple_replace( event, cleandict )
    event = re.sub(r'  +', ' ', event).rstrip().lstrip()

    if item['venue'] == "Hack Manhattan":
      event = brico.slack.bold(event)

    line = "%s: %s %s" % (start, event, venue)
    slkThree.append( brico.slack.quot( line ) )

brico.common.write_pull("space_events.html", evtSpce)
brico.common.write_pull("building_events.html", evtBldg)
brico.common.write_pull("city_events.html", evtCity)
brico.common.write_text("threeday_events.slack", slkThree)
