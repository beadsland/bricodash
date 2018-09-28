#!/usr/bin/env python3

import pychromecast
import os
import sys
import time

chromecasts = pychromecast.get_chromecasts()

cast = next(cc for cc in chromecasts if cc.device.friendly_name == "Hackerspace")
cast.wait()

if cast.status.display_name == "DashCast":
  sid = cast.status.session_id
  pwd = os.path.dirname(sys.argv[0])
  path = pwd + "/sid/" + sid
  if os.path.exists(path):
    up = time.time() - os.path.getmtime(path)
    if up > 60 * 20:
      cast.quit_app()
