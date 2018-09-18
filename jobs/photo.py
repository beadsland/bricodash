#!/usr/bin/env python

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
