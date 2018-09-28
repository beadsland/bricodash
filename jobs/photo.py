#!/usr/bin/env python
# -*- coding: utf-8 -*-

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

import os
import sys
import json
import requests
import random
import time

pwd = os.path.dirname(sys.argv[0])
query = "https://api.meetup.com/HackManhattan/photos?&sign=true&photo-host=public&page=100"

response = requests.get(query)
if response.status_code != 200:   sys.exit(response.status_code);
data = json.loads(response.text)

img = random.choice(data)['photo_link']
html = ['<img id="peekaboo" style="display: none" src="' + img + '">']

html.append( '<span id="timestamp" epoch="' + str(time.time()) + '"></span>' )

filename = pwd + "/../html/pull/photo.html"
file = open(filename + ".new", "w")
file.write( '<div class="centered">' + "\n".join(html) + '</div>')
os.rename(filename + ".new", filename)
