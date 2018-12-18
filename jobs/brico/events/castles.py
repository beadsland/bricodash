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

from icalevents.icalevents import events
import os
import dateutil.tz as tz

import brico.common
import brico.common.html as html

calendar = "e5dh8b6plqo4sift6fbplkcqjg%40group.calendar.google.com"

def main():
  style = "margin-left: -.05em; vertical-align: -10%;"
  castles = html.img().clss('logo').style(style).src("img/babycastles.png")
  castles = castles.alt("Babycastles").str()

  path = os.path.join( "https://calendar.google.com/calendar/ical",
                       calendar, "public/basic.ics" )
  ev = []
  for e in events(path):
    name = brico.events.polite(e.summary)
    if "Babycastles" in e.summary:
      name = name.replace("Babycastles", castles)
    else:
      name = "%s (%s)" % (name, castles)

    start = e.start.astimezone(tz.tzlocal()).strftime("%Y-%m-%d %H:%M:%S")
    ev.append( { 'start': start, 'event': name, 'venue': "Babycastles" } )
  brico.common.write_json("castles.json", brico.events.datesort(ev))
