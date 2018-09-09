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
sig_file = ".keys/meetup_sig"
with open('/'.join([pwd, sig_file])) as x: sig = x.read().rstrip()
query = "https://api.meetup.com/hackmanhattan/events?photo-host=public&page=20&sig_id=1998556&sig="
query = query + sig

response = requests.get(query)
data = json.loads(response.text)

filename = "/var/www/html/hm/events.json"

dump = []

for item in data[:6]:
  dt = dateparser.parse(item['local_date'] + " " + item['local_time'])
  date = humanize.naturalday(dt)
  time = dt.strftime("%-I:%M %p").lower()
  time = re.sub(r':00', '', time)
  item['name'] = re.sub(r' at Hack Manhattan', '', item['name'])

  dump.append({ 'dt': "%s, %s" % (date, time), 'name': item['name'],
                'rsvp': item['yes_rsvp_count'] })



file = open(filename + ".new", "w")
file.write( json.dumps(dump) )
os.rename(filename + ".new", filename)
