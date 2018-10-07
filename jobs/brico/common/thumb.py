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

import atexit
import os
import requests
from resizeimage import resizeimage
from PIL import Image
import time
import re

import urllib.parse
import brico.common
from brico.common.memoize import memoized

class Cache():
  def __init__(self):
    self.local = "../html/thmb"
    self.route = "thmb"
    self.localre = re.compile(r"^.*%s" % self.local)
    atexit.register(self.cleanup)

  def cleanup(self):
    dir = self.paths('')['local']['full']
    for f in os.listdir(dir):
      f = os.path.join(dir, f)
      if os.stat(f).st_mtime < time.time() - 10 * 60:
        if os.path.isfile(f):
          os.remove(f)

  def fetch(self, file, url, headers):
    response = requests.get(url, stream=True,
                            headers=headers if headers is not None else {})
    if response.status_code != 200:   sys.exit(response.status_code);
    with open(file, 'wb') as handle:
      for block in response.iter_content(1024):
        handle.write(block)
    handle.close()
    os.chown(file, -1, brico.common.gid())

  @memoized
  def paths(self, url):
    ext = urllib.parse.urlparse(url).path.split(".")[-1]
    enc = "%s.%s" % ( urllib.parse.quote(url, safe='').replace("%", "!")[-100:],
                      ext )
    sml = "sm_%s" % enc
    local = { "full": os.path.join(brico.common.pwd(), self.local, enc),
              "smll": os.path.join(brico.common.pwd(), self.local, sml) }
    route = { "full": "/".join(( self.route, enc )),
              "smll": "/".join(( self.route, sml )) }
    return { "local": local, "route": route }

  def get(self, url, headers):
    file = self.paths(url)['local']['full']
    if os.path.isfile(file):
      brico.common.touch(file)
    else:
      self.fetch(file, url, headers)
    return self.paths(url)['route']['full']

  def get_thumb(self, url, headers):
    smll = self.paths(url)['local']['smll']
    if os.path.isfile(smll):
      brico.common.touch(smll)
    else:
      self.get(url, headers)
      full = self.paths(url)['local']['full']
      with open(full, 'r+b') as handle:
        with Image.open(handle) as image:
          thumb = resizeimage.resize_height(image, 32)
          thumb.save(smll, image.format)
      handle.close()
      os.chown(smll, -1, brico.common.gid())
      os.remove(full)
    return self.paths(url)['route']['smll']
