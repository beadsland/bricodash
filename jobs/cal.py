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

import datetime
import subprocess
import json
import os
import sys

geek = "cal/geek.cal"
birth = "cal/birth.cal"
usnat = "cal/usnat.cal"
local = "cal/local.cal"

def recur(str): return subprocess.check_output(["./recur.pl", str])

def emoji(s): return '<span class="emoji">' + s + '</span>'

def parse_cal(filename):
  arr = []
  with open(filename, "rb") as f:
    for line in f.readlines():
      if line.strip() != "":
        spl = line.strip().decode().split("::")
        if len(spl) > 2 and spl[2].strip() != "":
          full = "%s %s" % (spl[1], emoji(spl[2].strip()))
          arr.append( (spl[0], full) )
        elif len(spl) > 1:
          arr.append( (spl[0], spl[1]) )

  arr = (( recur(t[0]), t[1].strip() ) for t in arr)
  arr = sorted(arr)
  return arr

arr = sorted( parse_cal(geek)[:3] + parse_cal(birth)[:3] + parse_cal(usnat)[:3] + parse_cal(local)[:3] )
arr = ( { "start": t[0].decode('utf-8'), "venue": "Holiday", "event": t[1].encode().decode('utf-8') } for t in arr )

holidays = list(arr)

pwd = os.path.dirname(sys.argv[0])
filename = pwd + "/../html/pull/holiday.json"
file = open(filename + ".new", "w")
file.write( json.dumps(holidays[:4]) )
os.rename(filename + ".new", filename)
