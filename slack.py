#!/usr/bin/env python

from slacker import Slacker
import re
import json
import os
import sys

pwd = os.path.dirname(sys.argv[0])
token_file = ".keys/slacker_token"
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

regex = re.compile(r"<@([^>]+)>")
hist = []

for message in reversed(response.body['messages']):
  text = regex.sub(lambda m: usp(names.get(m.group(1), m.group())),
                   message['text'])
  hist.append( div(who(names[message['user']]) + ": " + text) + "\n" )

import json
import os

filename = "/var/www/html/hm/slack.json"
file = open(filename + ".new", "w")
file.write( json.dumps(hist) )
os.rename(filename + ".new", filename)
