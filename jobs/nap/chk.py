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

import pychromecast
import os
import sys
import time
import configparser

pwd = os.path.dirname(sys.argv[0])

config = configparser.ConfigParser()
config.read(pwd + '/../../sysd/environment.file')
device = config['DEFAULT']['DISPLAY_NAME']

chromecasts = pychromecast.get_chromecasts()
cast = next(cc for cc in chromecasts if cc.device.friendly_name == device)
cast.wait()

if cast.status.display_name == "DashCast":
  sid = cast.status.session_id
  path = pwd + "/sid/" + sid
  if os.path.exists(path):
    up = time.time() - os.path.getmtime(path)
    if up > 60 * 20:
      cast.quit_app()
