#!/usr/bin/env python

import datetime
import subprocess
import json
import os
import sys

geek = "cal/geek.cal"
birth = "cal/birth.cal"
usnat = "cal/usnat.cal"

def recur(str): return subprocess.check_output(["./recur.pl", str])

def emoji(s): return '<span class="emoji">' + s + '</span>'

def parse_cal(filename):
  arr = []
  with open(filename, "rb") as f:
    for line in f.readlines():
      if line.strip() != "":
        spl = line.strip().split("::")
        if len(spl) > 2 and spl[2].strip() != "":
          full = "%s %s" % (spl[1], emoji(spl[2].strip()))
          arr.append( (spl[0], full) )
        else:
          arr.append( (spl[0], spl[1]) )

  arr = (( recur(t[0]), t[1].strip() ) for t in arr)
  arr = sorted(arr)
  return arr

arr = sorted( parse_cal(geek)[:3] + parse_cal(birth)[:3] + parse_cal(usnat)[:3] )
arr = ( { "start": t[0], "venue": "Holiday", "event": t[1] } for t in arr )

holidays = list(arr)

pwd = os.path.dirname(sys.argv[0])
filename = pwd + "/../html/pull/holiday.json"
file = open(filename + ".new", "w")
file.write( json.dumps(holidays) )
os.rename(filename + ".new", filename)
