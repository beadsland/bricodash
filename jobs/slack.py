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

from vend.memoize import memoized
from vend.multisub import multiple_replace
import brico.common
import brico.common.html as html
import brico.slack

import re
import humanize
import datetime
import requests
import os

token = brico.common.get_token("slacker_token")
slack = brico.slack.Slack( token )

names = slack.names()
avatr = slack.avatars()
channel = slack.channels()['hackerspace']

response = slack.history(channel = channel['id'], latest = None,
                         oldest = 0, count = 11)

def div(s): return html.div().clss("slacking").inner(s).str()
def hid(s): return html.span().style("opacity: .25;").inner(s).str()
def whn(s): return html.span().clss("slacked").inner(s).str()
def usp(s): return html.span().clss("slacker").inner("@%s" % s).str()
def chn(s): return html.span().clss("slackchan").inner("#%s" % s).str()
def who(s): return html.span().clss("slackee").inner(s).str()

emjex = re.compile(r":([A-Za-z\-_]+):")
usrex = re.compile(r"<@([^\|>]+)\|([^>]+)>")
us2ex = re.compile(r"<@([^\|>]+)>")
chnex = re.compile(r"<#[A-Z0-9]+\|([^>]+)>")
lnkex = re.compile(r"<(http.*)>")

hist = []
lstwhn = ""
lstwho = ""

durdict = { "second": "sec", "minute": "min", "hour": "hr",
            "day": "dy", "week": "wk", " ago": "" }

for message in reversed(response.body['messages']):
  delta = datetime.datetime.now().timestamp() - float(message['ts'])
  when = multiple_replace( humanize.naturaltime(delta), durdict )

  user = names[message['user']] if 'user' in message else message['username']
  if 'user' in message:
    user = html.logo(avatr[message['user']]) + " " + user

  text = message['text'];

  if 'files' in message:
    for file in message['files']:
      if 'thumb_64' in file:
        text += "%s " % slack.link(file['thumb_64'])
      else:
        text += "%s " % slack.link(file['permalink'])

  text = lnkex.sub(lambda m: ' ' + slack.link(m.group(1)), text)

  if 'attachments' in message:
    for file in message['attachments']:
      if 'image_url' in file:
        text += " %s" % slack.link(file['image_url'])

  text = chnex.sub(lambda m: chn(m.group(1)), text)
  text = usrex.sub(lambda m: usp(names.get(m.group(1), m.group(2))), text)
  text = us2ex.sub(lambda m: usp(names.get(m.group(1), m.group())), text)
  text = emjex.sub(lambda m: slack.emoji(m.group(1)), text)

  if lstwhn == when and lstwho == user:
    hist.append( div(hid(whn(when) + " &mdash; " +  who(user) + ": ") + text) )
  else:
    lstwhn = when
    lstwho = user
    hist.append( div(whn(when) + " &mdash; " +  who(user) + ": " + text) )

brico.common.write_pull( "slack.html", hist )
