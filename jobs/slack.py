#!/usr/bin/env python3

from slacker import Slacker
import re
import os
import sys
import emoji_data_python
import time
import humanize
import datetime
import requests

pwd = os.path.dirname(sys.argv[0])
token_file = ".keys/slacker_token"
with open('/'.join([pwd, token_file])) as x: token = x.read().rstrip()
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
def who(s): return "<span class='slackee'>" + s + "</span>"
def avt(s): return "<img class='logo' src='" + s + "' alt='" + s + "'>"

emjex = re.compile(r":([A-Za-z\-_]+):")
usrex = re.compile(r"<@([^\|>]+)\|([^>]+)>")
us2ex = re.compile(r"<@([^\|>]+)>")
chnex = re.compile(r"<#[A-Z0-9]+\|([^>]+)>")
lnkex = re.compile(r"<(http.*)>")

def fetch_image(file, url, token):
  headers = { "Authorization": "Bearer " + token }
  response = requests.get(url, headers=headers, stream=True)
  if response.status_code != 200:   sys.exit(response.status_code);
  with open(file, 'wb') as handle:
    for block in response.iter_content(1024):
      handle.write(block)

imgext = ('.gif', '.jpg', '.jpeg', '.png')

def intlnk(u):
  file = time.strftime("%Y%m%d-%H%M%S_") + u.split("?")[0].split("/")[-1]
  thmb = os.path.join(pwd, "../html/thmb/")
  fetch_image(thmb + file, u, token)

  for f in os.listdir(thmb):
    f = os.path.join(thmb, f)
    if os.stat(f).st_mtime < time.time() - 20 * 60:
      if os.path.isfile(f):
        os.remove(f)

  return ' ' + avt("thmb/" + file)

def extlnk(o, u, c):
  if u.split("?")[0].lower().endswith(imgext) and o == "&lt;":
    return ' ' + avt(u)
  else:
    if u.split("?")[0].lower().endswith(imgext) and o == "[":
      return intlnk(u)
    else:
      if len(u) < 50:
        start = len(u) - 20
      else:
        start = 30
      return ' ' + o + u[:start] + '…' + u[-20:] + c


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
  text = chnex.sub(lambda m: "#" + m.group(1), text)
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
filename = pwd + "/../html/pull/slack.html"
file = open(filename + ".new", "wb")
file.write( u"\n".join(hist).encode("utf-8") )
os.rename(filename + ".new", filename)
