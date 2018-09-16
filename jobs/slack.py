#!/usr/bin/env python3

from slacker import Slacker
import re
import os
import sys
import emoji_data_python
import time

pwd = os.path.dirname(sys.argv[0])
token_file = "../.keys/slacker_token"
with open('/'.join([pwd, token_file])) as x: token = x.read().rstrip()
slack = Slacker(token)
channels = slack.channels.list().body['channels']

names = { user['id']: (user['profile']['display_name'], user['name'])
	  for user in slack.users.list().body['members'] }
for id in names:
  if names[id][0] == "":
    names[id] = names[id][1]
  else:
    names[id] = names[id][0]

for channel in channels:
  if channel['name'] == 'hackerspace':
    break

response = slack.channels.history(channel = channel['id'],
                                  latest = None,
                                  oldest = 0,
                                  count = 11)

def usp(s): return "<span class='slacker'>@" + s + "</span>"
def div(s): return "<div class='slacking'>" + s + "</div>"
def who(s): return "<span class='slackee'>" + s + "</span>"

emjex = re.compile(r":([A-Za-z\-_]+):")
usrex = re.compile(r"<@([^>]+)>")
chnex = re.compile(r"<#[A-Z0-9]+\|([^>]+)>")
lnkex = re.compile(r"<(http.*)>")
hist = []

for message in reversed(response.body['messages']):
  user = names[message['user']] if 'user' in message else message['username']

  text = message['text'];
  text = lnkex.sub(lambda m: "&lt;" + m.group(1) + "&gt;", text)
  text = chnex.sub(lambda m: "#" + m.group(1), text)
  text = usrex.sub(lambda m: usp(names.get(m.group(1), m.group())), text)
  text = emjex.sub(lambda m: "<span class='emoji'>:" + m.group(1) + ":</span>", text)
  text = emoji_data_python.replace_colons(text)

  if 'files' in message:
    for file in message['files']:
      url = file['url_private_download']
      text += " [" + url + "]"

  hist.append( div(who(user) + ": " + text) )

hist.append( '<span id="timestamp" epoch="' + str(time.time()) + '"></span>' )

# new path
filename = pwd + "/../html/pull/slack.html"
file = open(filename + ".new", "wb")
file.write( u"\n".join(hist).encode("utf-8") )
os.rename(filename + ".new", filename)
