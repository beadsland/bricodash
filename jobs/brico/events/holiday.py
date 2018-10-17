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
from dateutil.relativedelta import relativedelta
import datetime
import subprocess
import json
import os
import sys

import brico.common
import brico.common.html as html

def main():
  geek = "cal/geek.cal"
  birth = "cal/birth.cal"
  usnat = "cal/usnat.cal"
  local = "cal/local.cal"

  arr = sorted( parse_cal(birth, 1) + parse_cal(geek, 4) \
                + parse_cal(usnat, 7) + parse_cal(local) )
  arr = ( { 'start': t[0].decode('utf-8'),
            'venue': "Holiday",
            'event': t[1].encode().decode('utf-8') } for t in arr )
  arr = list(arr)

  # Three events minimum.
  n = 3
  # Grab all events for today...
  tomorrow = datetime.datetime.now() + relativedelta(days = +1)
  while n < len(arr) and \
                         dateutil.parser.parse(arr[n]['start']) < tomorrow:
    n += 1
  # ...and up to max 6 total events through tomorrow.
  nextday = tomorrow + relativedelta(days = +1)
  while n < len(arr) < 6 and \
                         dateutil.parser.parse(arr[n]['start']) < nextday:
    n += 1

  brico.common.write_json("holiday.json", arr[:n])

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
          spl[2] = spl[2].strip()
          moji = html.emoji(spl[2]) if len(spl[2]) < 5 else html.logo(spl[2])
          arr.append( (spl[0], "%s %s" % (spl[1], moji)) )
        elif len(spl) > 1:
          arr.append( (spl[0], spl[1]) )

  arr = (( recur(t[0]), t[1].strip() ) for t in arr)
  arr = sorted(arr)

  n = 0
  cap = datetime.datetime.now() + relativedelta(days = +days)
  while dateutil.parser.parse(arr[n][0]) < cap: n += 1

  return arr[:n]

###
# Haven't found a python module that does this for all our use cases
###
def recur(str):
  recur = os.path.join(brico.common.pwd(), "brico/events/recur.pl")
  return subprocess.check_output([recur, str])
