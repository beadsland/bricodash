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

import brico.common.html

import datetime
import re

# U.S. winter holidays. Not really lunar, but kept here to stay tidy.

def main(now): return [ kwanzaa(now), twelve(now) ]

def kwanzaa(now):
  days = { (12, 26): ("Umoja", "unity"),
           (12, 27): ("Kujichagulia", "self-determination"),
           (12, 28): ("Ujima", "collective work and responsibility"),
           (12, 29): ("Ujamaa", "collective economics"),
           (12, 30): ("Nia", "purpose"),
           (12, 31): ("Kuumba", "creativity"),
           (1, 1):   ("Imani", "faith") }
  key = (now.month, now.day)
  kinara = brico.common.html.logo("img/kwanzaa.png")
  if key in days:
    event = "<em>%s</em> (%s) %s" % (days[key][0], days[key][1], kinara)
    start = now.date().isoformat()
  else:
    event = "Kwanzaa Begins %s" % kinara
    start = datetime.date(now.year, 12, 26).isoformat()
  return { 'start': start, 'venue': "Holiday", 'event': event }

def twelve(now):
  callout = "font-size: 150%"
  partridge = brico.common.html.logo("img/partridge.png", ":partridge:")
  days = [ "", "&ensp;a&ensp;%s&ensp;∈&ensp;a&ensp;🍐&ensp;🌳" % partridge,
           "🐢🕊️", "🇫🇷🐔", "🤙🐦",
           brico.common.html.span().style(callout).inner("🏅&ensp;💍").str(),
           "🦆🥚",
           "%s🏊🏿‍♀️" % brico.common.html.logo("img/ggl-swan.png", ":swan:"),
           "👧🥛", "💃🏽👣", "🤴🐬", "🎺🎶", "🥁🥁" ]

  adj = now - datetime.timedelta(days=12)
  day = datetime.date(adj.year, adj.month, adj.day) \
        - datetime.date(adj.year, 12, 12)
  if day.days < 1 or day.days > 12:
    return { 'start': datetime.date(3333, 3, 3).isoformat(),
             'venue': "Holiday", 'event': "nothing to see here" }
  else:
    list = ["%s×%s" % (i, brico.common.html.emoji(days[i])) \
                      for i in range(0,day.days+1)]
    list = list[1:]
    list.reverse()
    love = "<b>⊤</b>%s" % brico.common.html.emoji("💖🎁🤳")
    event = "%s:&nbsp;&nbsp;%s" % (love, ", ".join( list ))
    event = re.sub(", 1×", " & ", event)
    return { 'start': now.date().isoformat(), 'venue': "Holiday",
             'event': event }
