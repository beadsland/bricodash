#!/usr/bin/env python3

from subprocess import call
import time
import pychromecast
import pychromecast.controllers.dashcast as dashcast

chromecasts = pychromecast.get_chromecasts()
cast = next(cc for cc in chromecasts if cc.device.friendly_name == "Hackerspace")

cast.wait()

path = "http://hackmanhattan.duckdns.org:8888/hm/dash.php";
patharr = "/usr/local/bin/catt cast_site".split()
patharr.append(path)
if cast.status.display_name == "Backdrop":
  call(patharr)
