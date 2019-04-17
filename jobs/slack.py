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
import brico.common
import brico.common.html as html
import brico.slack

import re
import math

#token = brico.common.get_token("slacker_token")
#slack = brico.slack.Slack( token )

app_token = brico.common.get_token("slack_app_token")
bot_token = brico.common.get_token("slack_bot_token")
slack = brico.slack.Slack( app_token, bot_token )

##
# Time and user
##
@memoized
def avuser(u): return "%s %s" % (slack.avatars(u, html.logo), slack.names(u));
def whn(s, ts):
  return html.span().clss("slacked").attr("timestamp", ts).inner( s ).str()
def who(s): return html.span().clss("slackee").inner( s ).str()

###
#  Prettify sequential posts by same user
###

hist = []
lstwhn = ""
lstwho = ""
def hid(s): return html.span().clss('shide').inner(s).str()
def sub(s): return html.span().clss('ssubt').inner(s).str()
###
# Format each message
###
for message in reversed(slack.messages('hackerspace', 11)):
  when = slack.human_time( message['ts'] )
  user = avuser(message['user']) if 'user' in message else message['username'];

  text = slack.format_text(message)

  if 'subtype' in message and message['subtype'] != 'thread_broadcast':
    line = brico.slack.div( "%s &mdash; %s: %s" % (whn(when, message['ts']),
                                                   who(user),
                                                   sub(text)) )
    hist.append( line )
  else:
    if lstwhn == when and lstwho == user:
      line = brico.slack.div( "%s &mdash; %s: %s" % (hid(whn(when, message['ts'])),
                                                     who(user), text) )
      hist.append( line )
    else:
      lstwhn = when
      lstwho = user
      hist.append(brico.slack.div( "%s &mdash; %s: %s" % (whn(when, message['ts']),
                                                          who(user), text) ))

###
# Trim excess lines
###
def linecount(s): return math.ceil( len( tag.sub("", img.sub("[]", s)) ) / 80 )
img = re.compile(r'<img[^>]+>')
tag = re.compile(r'<[^>]+>')
lines = 11

while lines > 10:
  lines = 0
  for h in hist: lines += linecount(h)
  if lines - linecount(hist[0]) > 11:     hist.pop(0)
  else:                                   break

###
# And dump it out for polling
###
brico.common.write_pull( "slack.html", hist )
