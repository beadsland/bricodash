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

import humanize
import datetime
import re

token = brico.common.get_token("slacker_token")
slack = brico.slack.Slack( token )

##
# Time and user
##
durdict = { "second": "sec", "minute": "min", "hour": "hr",
            "day": "dy", "week": "wk", " ago": "" }
@memoized
def avuser(u): return "%s %s" % (slack.avatars(u, html.logo), slack.names(u));
def whn(s): return html.span().clss("slacked").inner(s).str()
def who(s): return html.span().clss("slackee").inner(s).str()

###
# Link, image and emoji formatting
##
@memoized
def slemoji(u): return html.img().clss('slemoji').src( u ).str()

# no memoize because links tend to be one-offs
def linky(u):
  file = u if len(u) < 55 else "%s…%s" % (u[:30], u[-20:])
  return html.span().style("font-size: 75%;").inner("<%s>" % file).str()

emotags = { 'emotag': html.emoji, 'imgtag': html.logo, 'lnktag': linky,
            'slemotag': slemoji }

###
# Outer formatting
###
def div(s): return html.div().clss("slacking").inner(s).str()
def usp(s): return html.span().clss("slacker").inner("@%s" % s).str()
def chn(s): return html.span().clss("slackchan").inner("#%s" % s).str()

txtdict = [ ("<(http[^>]+)>", lambda m: slack.link(m.group(1), html.logo) ),
            ("<#[^\|>]+\|([^>]+)?>", lambda m: chn(m.group(1)) ),
            ("<@([^\|>]+)(\|[^>]+)?>", lambda m: usp(slack.names(m.group(1))) ),
            (":([A-Za-z\-_]+):", lambda m: slack.emoji(m.group(1), emotags) ) ]

###
#  Prettify sequential posts by same user
###

hist = []
lstwhn = ""
lstwho = ""
def hid(s): return html.span().style("opacity: .25;").inner(s).str()

###
# Format each message
###
for message in reversed(slack.messages('hackerspace', 11)):
  delta = datetime.datetime.now().timestamp() - float(message['ts'])
  when = multiple_replace( humanize.naturaltime(delta), durdict )
  user = avuser(message['user']) if 'user' in message else message['username'];

  text = message['text'];
  for tup in txtdict: text = re.compile(tup[0]).sub(tup[1], text)
  text += " %s" % " ".join( slack.attachments(message, html.logo, linky) )

  if lstwhn == when and lstwho == user:
    hist.append( div(hid(whn(when) + " &mdash; " +  who(user) + ": ") + text) )
  else:
    lstwhn = when
    lstwho = user
    hist.append( div(whn(when) + " &mdash; " +  who(user) + ": " + text) )

###
# And dump it out for polling
###
brico.common.write_pull( "slack.html", hist )
