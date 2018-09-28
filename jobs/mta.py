#!/usr/bin/env python3

import requests
from bs4 import BeautifulSoup
import cssutils
import logging
cssutils.log.setLevel(logging.CRITICAL)

import os
import sys
import time

query = "http://service.mta.info/ServiceStatus/status.html?widget=yes"
response = requests.get(query)
if response.status_code != 200:   sys.exit(response.status_code)

text = response.text.replace("white", "#101010")
text = text.replace("silver", "#101010")

soup = BeautifulSoup(text, "html.parser")
[s.extract() for s in soup('script')]
body = soup.find("body")
del body.attrs["onload"]

head = soup.find("head")
base = soup.new_tag('base')
#base.attrs['href'] = "http://service.mta.info/ServiceStatus/"
base.attrs['href'] = "../prox/"
head.insert(0, base)

shad = soup.new_tag('style')
shad.string = ".subwayCategory { text-shadow: 1px 1px #303030, -1px -1px #303030; }"
head.insert(0, shad)

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
mtal.attrs['src'] = "widgetImages/mta_widget_logo.png"
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

text = soup.encode_contents(formatter='html')

#text.append( '<span id="timestamp" epoch="' + str(time.time()) + '"></span>' )

pwd = os.path.dirname(sys.argv[0])
filename = pwd + "/../html/pull/mta.html"
file = open(filename + ".new", "wb")
file.write( text )
os.rename(filename + ".new", filename)
