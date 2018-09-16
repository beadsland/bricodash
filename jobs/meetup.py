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

pwd = os.path.dirname(sys.argv[0])
sig_file = "../.keys/meetup_sig"
with open('/'.join([pwd, sig_file])) as x: sig = x.read().rstrip()
query = "https://api.meetup.com/hackmanhattan/events?photo-host=public&page=20&sig_id=1998556&sig="
query = query + sig

response = requests.get(query)
data = json.loads(response.text)

dump = []

def wdt(s): return "<span class='date'>%s</span>" % (s)
def wdd(s): return "<span class='event'>%s</span>" % (s)
def evt(s): return "<div class='event-line'>%s</div>" % (s)

for item in data[:6]:
  dt = dateparser.parse(item['local_date'] + " " + item['local_time'])
  date = humanize.naturalday(dt)
  start = dt.strftime("%-I:%M %p").lower()
  start = re.sub(r':00', '', start)
  item['name'] = re.sub(r' at Hack Manhattan', '', item['name'])

  dt = "%s, %s" % (date, start)

  dd = item['name'];
  if item['yes_rsvp_count'] > 4:  dd += " (%s)" % item['yes_rsvp_count']

  dt = wdt(dt)
  dd = wdd(dd)
  dump.append( evt("%s &mdash; %s" % (dt, dd)) )

dump.append( '<span id="timestamp" epoch="' + str(time.time()) + '"></span>' )

filename = pwd + "/../html/pull/events.html"
file = open(filename + ".new", "w")
file.write( "\n".join(dump) )
os.rename(filename + ".new", filename)
