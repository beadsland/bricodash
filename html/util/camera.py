#!/usr/bin/env python3

#debug=True
if ('debug' in locals()):
  import cgitb; cgitb.enable(); print("Content-Type: text/html\n"); print("")

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

import cgi
import os
import sys
import requests
import time
import logging
from PIL import Image
import io

SWEET = .30  # This value is the time to sleep between frames, to avoid
             # flooding the chromecast. Sweet spot depends on local network
             # conditions and performance of source camera.

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
handler = logging.FileHandler('hello.log')
handler.setLevel(logging.WARN)
logger.addHandler(handler)

logger.info('Handle request.')
handler.flush()

filename = "../img/ceilingcat.jpg"

mjpg = {
        'space': "http://wrtnode-webcam:8080/",
        'door': "http://rfid-access-building:8080/",
        'cr10': "http://octoprint-main:8080/",
        'hydro': "http://hydrocontroller:8081/"
      }

form = cgi.FieldStorage()
view =    "space"   if not 'view' in form     else form['view'].value
logger.info(view)
action =  "stream"  if not 'action' in form   else form['action'].value
logger.info(action)
query = mjpg[view] + "?action=snapshot"
logger.info(query)
handler.flush()

def catsnap():
  sys.stdout.flush()
  sys.stdout.buffer.write(open(filename, "rb").read())
  sys.stdout.flush()

def snap():
  response = requests.get(query, stream=True)
  if response.status_code != 200:   sys.exit(response.status_code);

  sys.stdout.flush()

#  for block in response.iter_content(1024):
#    sys.stdout.buffer.write(block)
  bstr = b''
  for block in response.iter_content(1024):
    bstr += block
  img = Image.open(io.BytesIO(bstr))
  try:
    img.getpixel( (img.width-1, img.height-1) )
  except Exception as e:
    if str(e).startswith("broken data stream"):
      logging.error(e)
      snap()
    else:
      sys.stdout.buffer.write(bstr)
  else:
    sys.stdout.buffer.write(bstr)

boundary = '--SNAP-HACKLE-STOP--'

if action == "snapshot":
  print("Content-Type: image/jpg")
#  print('Content-Length: %s' % os.path.getsize(filename))
  print("")
  snap()
elif action == "stream":
  # drawn from: https://stackoverflow.com/questions/21197638/create-a-mjpeg-stream-from-jpeg-images-in-python
  print('Cache-Control: no-store, no-cache, must-revalidate, pre-check=0, post-check=0, max-age=0')
  print('Connection: close')
  print('Content-Type: multipart/x-mixed-replace;boundary=%s' % boundary)
  print('Expires: Mon, 3 Jan 2000 12:34:56 GMT')
  print('Pragma: no-cache')
  while 1:
    time.sleep(SWEET)
#    logger.info(time.time())
    handler.flush()
    print("")
    print(boundary)
    print('X-Timestamp: %s' % time.time())
    print("Content-Type: image/jpg")
    print("")
    snap()
else:
  sys.exit("bad action")
