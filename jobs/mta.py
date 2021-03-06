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

import requests
from bs4 import BeautifulSoup
import cssutils
import logging
cssutils.log.setLevel(logging.CRITICAL)

import os
import sys
import time
import re

query = "http://service.mta.info/ServiceStatus/status.html?widget=yes"
response = requests.get(query)
if response.status_code != 200:   sys.exit(response.status_code)

text = response.text.replace("white", "#101010")
text = text.replace("silver", "#101010")
text = text.replace("widgetImages", "prox/widgetImages")

soup = BeautifulSoup(text, "html.parser")
[s.extract() for s in soup('script')]
body = soup.find("body")
del body.attrs["onload"]

body.insert(0, soup('style')[0].extract())
shad = soup.new_tag('style')
shad.string = ".subwayCategory { text-shadow: 1px 1px #303030, -1px -1px #303030; }"
body.insert(0, shad)

stmp = soup.findAll("td", {"class": "statusDateTime"})[0]
stmp_style = cssutils.parseStyle("")
stmp_style['color'] = "white";
stmp.attrs['style'] = stmp_style.cssText

head = soup.find("head")
base = soup.new_tag('base')
#base.attrs['href'] = "http://service.mta.info/ServiceStatus/"
#base.attrs['href'] = "../prox/"
#head.insert(0, base)

outr = soup.find(id="outerDiv")
#outr_style = cssutils.parseStyle(outr.attrs['style']) # no style
outr_style = cssutils.parseStyle("")
outr_style['height'] = "360px";
outr.attrs['style'] = outr_style.cssText

hedr = soup.find(id="headerDiv")
hedr_style = cssutils.parseStyle(hedr.attrs['style'])
hedr_style['top'] = "2px";
hedr.attrs['style'] = hedr_style.cssText

mtal = soup.find(id="MTAwidgetlogo")
mtal.attrs['src'] = "prox/widgetImages/mta_widget_logo.png"
mtal_style = cssutils.parseStyle("")
mtal_style['height'] = "auto";
mtal_style['width'] = "1em";
mtal_style['display'] = "inline";
mtal.attrs['style'] = mtal_style.cssText

cbar = soup.find(id="controlBar2")
##cbar_top = cssutils.parseStyle(cbar.attrs['style']).top
cbar.attrs['style'] = "display: none;"


sdiv = soup.find(id="subwayDiv")
_ = sdiv.find("tr").extract()
sdiv_style = cssutils.parseStyle(sdiv.attrs['style'])
del sdiv_style['height']
sdiv_style['top'] = "25px"
sdiv.attrs['style'] = sdiv_style.cssText

stbl = sdiv.find("table")
stbl_style = cssutils.parseStyle(stbl.attrs['style'])
del stbl_style['top']
stbl.attrs['style'] = stbl_style.cssText


sdiv = soup.find(id="railDiv")
_ = sdiv.find("table").extract()
sdiv_style = cssutils.parseStyle(sdiv.attrs['style'])
del sdiv_style['height']
sdiv.attrs['style'] = sdiv_style.cssText

sdiv = soup.find(id="busDiv")
_ = sdiv.find("table").extract()
sdiv_style = cssutils.parseStyle(sdiv.attrs['style'])
del sdiv_style['height']
sdiv.attrs['style'] = sdiv_style.cssText

sdiv = soup.find(id="BTDiv")
_ = sdiv.find("table").extract()
sdiv_style = cssutils.parseStyle(sdiv.attrs['style'])
del sdiv_style['height']
sdiv.attrs['style'] = sdiv_style.cssText


_ = soup.find_all('div')[-1].extract()

text = body.encode_contents(formatter='html')

stamp = '<span id="timestamp" epoch="' + str(time.time()) + '"></span>'
text = text + stamp.encode('utf-8')

pwd = os.path.dirname(sys.argv[0])
filename = pwd + "/../html/pull/mta.html"
file = open(filename + ".new", "wb")
file.write( text )
os.rename(filename + ".new", filename)
