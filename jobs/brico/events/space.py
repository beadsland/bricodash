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

import brico.common.html as html
import brico.common
import brico.common.meetup
from vend.memoize import memoized

import datetime
import calendar
import dateparser
import re

def main():
  ###
  # Identify last Tuesday of month for General Meeting
  ###
  today = datetime.date.today()
  lasttues = max( week[calendar.TUESDAY]
                  for week in calendar.monthcalendar(today.year, today.month) )

  ###
  # Prepare to munge names of regular event listings
  ###
  def append(s): return r'\1 ' + s
  freecodestyle = "height:1.05em; vertical-align: bottom;"

  freecode = html.img().style(freecodestyle).src("img/freeCodeCamp.png")
  freecode = freecode.alt("freeCodeCamp").str()

  toool = html.img().style(freecodestyle).src("img/toool.png")
  toool = toool.alt("(TOOOL)").str()

  evtdict = [ ( ' at Hack Manhattan', '' ),
              ( '(Open House)', append(html.logo("img/balloons.png")) ),
              ( '(Fixers\' Collective)', append(html.logo("img/fixers.png")) ),
              ( '\(TOOOL\)', toool ),
              ( 'freeCodeCamp', freecode ),
              ( '(Midnight Games)', append(html.emoji("🌌🎲")) ),
              ( '(Electronics Night)', append(html.emoji("💡")) ),
              ( '(Shakespeare Night.*$)', append(html.emoji("🎭📖")) ) ]

  ###
  # Generate event json
  ###
  events = []

  for item in brico.common.meetup.events(brico.common.grp())[:8]:
    evt = item['name']
    for tup in evtdict: evt = re.compile(tup[0]).sub(tup[1], evt)
    dt = dateparser.parse(item['local_date'] + " " + item['local_time'])
    if (dt.day == lasttues) and (dt.month == today.month):
      evt = re.sub(r'(Tech Tuesday)', r'\1 / General Meeting', evt)

    if (dt.day == 8) and (dt.month == 1) and (dt.year == 2019):
      evt = re.sub(r'(Tech Tuesday)', r'\1 / Rescheduled General Meeting', evt)

    mevt = re.sub(r'Math talk: +', '', evt)
    if mevt in colist("nyc-math"):
      rsvp = colist_rsvps("nyc-math", item, mevt)
      evt = '%s %s' % ( evt, html.logo("img/math.png") )
    else:
      rsvp = item['yes_rsvp_count']

    end = dt + datetime.timedelta(seconds = item['duration'] / 1000)

    events.append( { "start": dt.isoformat(), "end": end.isoformat(),
                     "event":  evt, "venue": "Hack Manhattan",
                     "rsvp": rsvp } )

  brico.common.write_json("space.json", events)

###
# Get RSVP counts for co-listed events
###
@memoized
def colist(group):  # will break on identically named events -- not a problem
  return { e["name"]: e["id"] for e in brico.common.meetup.events(group) }

def colist_rsvps(group, item, mevt):
  us =   brico.common.meetup.rsvps( brico.common.grp(), item['id'] )
  them = brico.common.meetup.rsvps( group, colist(group)[mevt] )

  rsvps = {};
  for ans in us + them:
    if ans['response'] == "yes":
      id = ans['member']['id']
      if id not in rsvps:   rsvps[id] = ans["guests"]
      else:                 rsvps[id] = max(rsvps[id], ans["guests"])
  return len(rsvps) + sum(rsvps.values())
