#!/usr/bin/env python

import json
import requests
import dateparser
import humanize
import re
import os
import json
import sys

pwd = os.path.dirname(sys.argv[0])
sig_file = "../.keys/meetup_sig"
with open('/'.join([pwd, sig_file])) as x: sig = x.read().rstrip()
query = "https://api.meetup.com/hackmanhattan/events?photo-host=public&page=20&sig_id=1998556&sig="
query = query + sig

response = requests.get(query)
data = json.loads(response.text)


dump = []

for item in data[:6]:
  dt = dateparser.parse(item['local_date'] + " " + item['local_time'])
  date = humanize.naturalday(dt)
  time = dt.strftime("%-I:%M %p").lower()
  time = re.sub(r':00', '', time)
  item['name'] = re.sub(r' at Hack Manhattan', '', item['name'])

  dt = "%s, %s" % (date, time)

  dd = item['name'];
  if item['yes_rsvp_count'] > 4:  dd += " (%s)" % item['yes_rsvp_count']

  dump.append("<dt>%s<dd>%s" % (dt, dd))

filename = pwd + "/../html/pull/events.html"
file = open(filename + ".new", "w")
file.write( "\n".join(dump) )
os.rename(filename + ".new", filename)
