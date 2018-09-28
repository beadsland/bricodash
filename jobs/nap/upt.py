#!/usr/bin/env python3

import pychromecast
import os
import sys
import time

chromecasts = pychromecast.get_chromecasts()

cast = next(cc for cc in chromecasts if cc.device.friendly_name == "Hackerspace")
cast.wait()
sid = cast.status.session_id

pwd = os.path.dirname(sys.argv[0])
path = pwd + "/sid"
sid = os.path.join(path, sid)
if not os.path.exists(sid):
  open(sid, 'a').close()

for f in os.listdir(path):
  f = os.path.join(path, f)
  if os.stat(f).st_mtime < time.time() - 60 * 60 * 24:
    if os.path.isfile(f):
      os.remove(f)
