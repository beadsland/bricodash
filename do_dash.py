#!/usr/bin/env python

from subprocess import call
import time
import pychromecast
import pychromecast.controllers.dashcast as dashcast

chromecasts = pychromecast.get_chromecasts()
cast = next(cc for cc in chromecasts if cc.device.friendly_name == "Hackerspace")

cast.wait()

print cast.status

if cast.status.display_name == "Backdrop":
  call("/usr/local/bin/catt cast_site http://192.168.43.191/hm/dash.php".split())


## Get's stuck on "loading" screen unless forced
#  d = dashcast.DashCastController()
#  cast.register_handler(d)

#  warning_message = "hello world!"
#  d.load_url('http://hackmanhattan.duckdns.org:8080/hm/camera.php')
#  time.sleep(30)

