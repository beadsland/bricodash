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

import brico.common
import os
from slacker import Slacker
import re
import emoji_data_python
import time
import humanize
import datetime
import requests
from resizeimage import resizeimage
from PIL import Image

token_file = ".keys/slacker_token"
with open('/'.join([brico.common.pwd(), token_file])) as x: token = x.read().rstrip()
slack = Slacker(token)
channels = slack.channels.list().body['channels']

names = { user['id']: (user['profile']['display_name'], user['name'])
	  for user in slack.users.list().body['members'] }
avatr = { user['id']: user['profile']['image_32']
    for user in slack.users.list().body['members'] }
for id in names:
  if names[id][0] == "":          names[id] = names[id][1]
  else:                           names[id] = names[id][0]

for channel in channels:
  if channel['name'] == 'hackerspace':
    break

response = slack.channels.history(channel = channel['id'],
                                  latest = None,
                                  oldest = 0,
                                  count = 11)

def div(s): return "<div class='slacking'>" + s + "</div>"
def hid(s): return "<span style='opacity: .25;'>" + s + "</span>"
def whn(s): return "<span class='slacked'>" + s + "</span>"
def usp(s): return "<span class='slacker'>@" + s + "</span>"
def chn(s): return "<span class='slackchan'>#" + s + "</span>"
def who(s): return "<span class='slackee'>" + s + "</span>"
def avt(s): return "<img class='logo' src='" + s + "' alt='" + s + "' onerror=\"this.src='img/broken.png';\">"
def sml(s): return "<span style='font-size: 75%'>" + s + "</span>"

emjex = re.compile(r":([A-Za-z\-_]+):")
usrex = re.compile(r"<@([^\|>]+)\|([^>]+)>")
us2ex = re.compile(r"<@([^\|>]+)>")
chnex = re.compile(r"<#[A-Z0-9]+\|([^>]+)>")
lnkex = re.compile(r"<(http.*)>")

def fetch_image(file, url, token):
  if token is None:   headers = {}
  else:               headers = { "Authorization": "Bearer " + token }
  response = requests.get(url, headers=headers, stream=True)
  if response.status_code != 200:   sys.exit(response.status_code);
  with open(file, 'wb') as handle:
    for block in response.iter_content(1024):
      handle.write(block)

imgext = ('.gif', '.jpg', '.jpeg', '.png')

def clnlnk(thmb):
  for f in os.listdir(thmb):
    f = os.path.join(thmb, f)
    if os.stat(f).st_mtime < time.time() - 20 * 60:
      if os.path.isfile(f):
        os.remove(f)

def intlnk(u):
  file = time.strftime("%Y%m%d-%H%M%S_") + u.split("?")[0].split("/")[-1]
  thmb = os.path.join(brico.common.pwd(), "../html/thmb/")
  fetch_image(thmb + file, u, token)
  clnlnk(thmb)
  return ' ' + avt("thmb/" + file)

def extlnk(o, u, c):
  if u.split("?")[0].lower().endswith(imgext) and o == "&lt;":
    file = time.strftime("%Y%m%d-%H%M%S_") + u.split("?")[0].split("/")[-1]
    thmb = os.path.join(brico.common.pwd(), "../html/thmb/")
    fetch_image(thmb + file, u, token)
    with open(thmb+file, 'r+b') as f:
      with Image.open(f) as image:
        small = resizeimage.resize_height(image, 32)
        small.save(thmb + "small_" + file, image.format)
    clnlnk(thmb)
    return ' ' + avt("thmb/" + "small_" + file)
  else:
    if u.split("?")[0].lower().endswith(imgext) and o == "[":
      return intlnk(u)
    else:
      if len(u) < 55:   return sml(' ' + o + u + c)
      else:             return sml(' ' + o + u[:30] + '…' + u[-20:] + c)


semoji = slack.emoji.list().body["emoji"];
def emjlnk(name):
  if name in semoji:
    if semoji[name].startswith("alias:"):
      alias = semoji[name].replace("alias:", "")
      return emjlnk(alias)
    else:
      return "<img class='slemoji' src='" + semoji[name] + "'>"
  else:
    return "<span class='emoji'>:" + name + ":</span>"

hist = []
lstwhn = ""
lstwho = ""

for message in reversed(response.body['messages']):
  delta = datetime.datetime.now().timestamp() - float(message['ts'])
  when = humanize.naturaltime(delta)
  when = when.replace("second", "sec")
  when = when.replace("minute", "min")
  when = when.replace("hour", "hr")
  when = when.replace("day", "dy")
  when = when.replace("week", "wk")
  when = when.replace(" ago", "")

  user = names[message['user']] if 'user' in message else message['username']
  if 'user' in message:
    user = avt(avatr[message['user']]) + " " + user

  text = message['text'];

  if 'files' in message:
    for file in message['files']:
      if 'thumb_64' in file:
        text += ' ' + extlnk("[", file['thumb_64'], "]")
      else:
        text += ' ' + extlnk("[", file['permalink'], "]")

  text = lnkex.sub(lambda m: extlnk("&lt;", m.group(1), "&gt;"), text)
  text = chnex.sub(lambda m: chn(m.group(1)), text)
  text = usrex.sub(lambda m: usp(names.get(m.group(1), m.group(2))), text)
  text = us2ex.sub(lambda m: usp(names.get(m.group(1), m.group())), text)
  text = emjex.sub(lambda m: emjlnk(m.group(1)), text)
  text = emoji_data_python.replace_colons(text)

  if lstwhn == when and lstwho == user:
    hist.append( div(hid(whn(when) + " &mdash; " +  who(user) + ": ") + text) )
  else:
    lstwhn = when
    lstwho = user
    hist.append( div(whn(when) + " &mdash; " +  who(user) + ": " + text) )

hist.append( '<span id="timestamp" epoch="' + str(time.time()) + '"></span>' )

# new path
filename = brico.common.pwd() + "/../html/pull/slack.html"
file = open(filename + ".new", "wb")
file.write( u"\n".join(hist).encode("utf-8") )
os.rename(filename + ".new", filename)
