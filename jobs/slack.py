#!/usr/bin/env python

from slacker import Slacker
import re
import os
import sys

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
                                  count = 15)

def usp(s): return "<span class='slacker'>@" + s + "</span>"
def div(s): return "<div class='slacking'>" + s + "</div>"
def who(s): return "<span class='slackee'>" + s + "</span>"

usrex = re.compile(r"<@([^>]+)>")
chnex = re.compile(r"<#[A-Z0-9]+\|([^>]+)>")
lnkex = re.compile(r"<(http.*)>")
hist = []

for message in reversed(response.body['messages']):
  user = names[message['user']] if 'user' in message else message['username']

  text = lnkex.sub(lambda m: "&lt;" + m.group(1) + "&gt;", text)
  text = chnex.sub(lambda m: "#" + m.group(1), text)
  text = usrex.sub(lambda m: usp(names.get(m.group(1), m.group())),
                   message['text'])

  if 'files' in message:
    for file in message['files']:
      url = file['url_private_download']
      text += " [" + url + "]"

  hist.append( div(who(user) + ": " + text) )

# new path
filename = pwd + "/../html/pull/slack.html"
file = open(filename + ".new", "w")
file.write( u"\n".join(hist).encode("utf-8") )
os.rename(filename + ".new", filename)
