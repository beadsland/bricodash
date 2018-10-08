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
import brico.common.thumb
import brico.common.html as html
import brico.slack

import re
import emoji_data_python
import humanize
import datetime
import requests
import os
import urllib.parse

token = brico.common.get_token("slacker_token")
slack = brico.slack.Slack( token )
thumb = brico.common.thumb.Cache()

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
def sml(s): return html.span().style("font-size: 75%;").inner(s).str()

emjex = re.compile(r":([A-Za-z\-_]+):")
usrex = re.compile(r"<@([^\|>]+)\|([^>]+)>")
us2ex = re.compile(r"<@([^\|>]+)>")
chnex = re.compile(r"<#[A-Z0-9]+\|([^>]+)>")
lnkex = re.compile(r"<(http.*)>")
thbex = re.compile(r"/files-tmb/")

def extlnk(o, u, c):
  parse = urllib.parse.urlparse(u)
  if (parse.path.endswith( ('.gif', '.jpg', '.jpeg', '.png') )):
    if ( thbex.match(parse.path) ):
      file = thumb.get(u, { "Authorization": "Bearer " + token })
    else:
      file = thumb.get_thumb(u, None)
    return html.logo(file)
  else:
    if len(u) < 55:   return sml('%s%s%s' % (o, u, c))
    else:             return sml('%s%s…%s%s' % (o, u[:30], u[-20:], c))

semoji = slack.emoji()
def emjlnk(name):
  if name in semoji:
    if semoji[name].startswith("alias:"):
      alias = semoji[name].replace("alias:", "")
      return emjlnk(alias)
    else:
      return html.img().clss("slemoji").src(semoji[name]).str()
  else:
    return html.span().clss("emoji").inner(":%s:" % name).str()

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
    user = html.logo(avatr[message['user']]) + " " + user

  text = message['text'];

  if 'files' in message:
    for file in message['files']:
      if 'thumb_64' in file:
        text += ' ' + extlnk("[", file['thumb_64'], "]")
      else:
        text += ' ' + extlnk("[", file['permalink'], "]")

  text = lnkex.sub(lambda m: ' ' + extlnk("&lt;", m.group(1), "&gt;"), text)

  if 'attachments' in message:
    for file in message['attachments']:
      if 'image_url' in file:
        text += ' ' + extlnk("&lt;", file['image_url'], "&gt;")

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

brico.common.write_pull( "slack.html", hist )
