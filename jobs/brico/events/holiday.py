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

import dateutil.parser
import dateutil.tz
from dateutil.relativedelta import relativedelta
import datetime
import subprocess
import json
import os
import sys
import re

import brico.common
import brico.common.html as html

import brico.events.birth
import brico.events.extra
import brico.events.lunar.geeky

def main():
  brico.events.birth.main()
  brico.events.extra.main()

  geek = "cal/geek.cal"
  birth = "../html/pull/birth.cal"
  usnat = "cal/usnat.cal"
  local = "cal/local.cal"
  extra = "../html/pull/extra.cal"
  trivia = "cal/trivia.cal"

  ###
  # Holidays and Special Events
  ###
  arr = [ (evt, 'Special') for evt in parse_cal(extra) ] \
          + [ (evt, 'Local') for evt in parse_cal(local) ] \
          + [ (evt, 'Holiday') for evt in parse_cal(usnat) ]
  arr = sorted(arr)
  arr = [ { 'start': t[0][0].decode('utf-8'),
            'venue': t[1],
            'event': t[0][1].encode().decode('utf-8') } for t in arr ]
  brico.common.write_json("holiday.json", arr[:10])

  ###
  # Geek holidays, birthdays and trivia
  ###
  arr = parse_cal(trivia, 1) + parse_cal(birth, 3) + parse_cal(geek, 7)
  arr = [ { 'start': t[0].decode('utf-8'),
            'venue': "Holiday",
            'event': t[1].encode().decode('utf-8') } for t in arr ]

  now = datetime.datetime.now(dateutil.tz.tzlocal())
  arr = arr + brico.events.lunar.geeky.main(now)
  arr = sorted( arr, key = lambda i: i['start'].replace('-', '/'))

  brico.common.write_json("geekday.json", arr[:10])

###
# Process a human-readable calendar file
###
def parse_cal(filename, days=30):
  arr = []

  with open(os.path.join(brico.common.pwd(), filename), "rb") as f:
    for line in f.readlines():
      if line.strip() != "" and not line.startswith(b'#'):
        spl = line.strip().decode().split("::")
        if len(spl) > 2 and spl[2].strip() != "":
          moji = spl[2].strip()
          isascii = all(ord(char) < 128 for char in moji)
          if isascii:
            moji = html.logo(moji)
          else:
            moji = html.emoji(moji)
          arr.append( (spl[0], "%s %s" % (spl[1], moji)) )
        elif len(spl) > 1:
          arr.append( (spl[0], spl[1]) )

  arr = (( recur(t[0]), t[1].strip() ) for t in arr)
  arr = sorted(arr, key = lambda x: x[0])

  n = 0
  cap = datetime.datetime.now() + relativedelta(days = +days)
  while len(arr) >= n and dateutil.parser.parse(arr[n][0]) < cap: n += 1

  return arr[:n]

###
# Haven't found a python module that does this for all our use cases
###
def recur(str):
  if re.match("[0-9]{4,}-[0-9]{2}-[0-9]{2}", str): return one_shot_kludge(str)

  recur = os.path.join(brico.common.pwd(), "brico/events/recur.pl")
  return subprocess.check_output([recur, str])

###
# Handle one-shot future (non-recurring) events
###
def one_shot_kludge(str):
  date = dateutil.parser.parse(str)
  now = datetime.datetime.now()
  if date < now - datetime.timedelta(days = 1):
    date = now + datetime.timedelta(days = 1000)
  return bytes(date.isoformat().replace('-', '/'), 'utf-8')
