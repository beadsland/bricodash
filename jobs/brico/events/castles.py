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
import datetime
import json
import requests
import re

import brico.common
import brico.common.html as html

calendar = "e5dh8b6plqo4sift6fbplkcqjg%40group.calendar.google.com"

def main():
  style = "margin-left: -.05em; vertical-align: -10%;"
  castles = html.img().clss('logo').style(style).src("img/babycastles.png")
  castles = castles.alt("Babycastles").str()

  path = os.path.join( "https://calendar.google.com/calendar/ical",
                       calendar, "public/basic.ics" )

  file = requests.get(path).text
  file = re.sub(r'(UNTIL=[0-9]+);', r'\1T000000Z;', file)

  ev = []
  for e in events(string_content = file.encode('utf-8')):
    name = brico.events.polite(e.summary)
    if "Babycastles" in e.summary:
      name = name.replace("Babycastles", castles)
    else:
      name = "%s (%s)" % (name, castles)

    if e.end - e.start > datetime.timedelta(days = 1):
      name = "%s&mdash;<i>ends %s</i>" \
             % (name, e.end.astimezone(tz.tzlocal()).strftime("%-m/%-d"))
      start = datetime.date.today().strftime("%Y-%m-%d %H:%M:%S")
    else:
      start = e.start.astimezone(tz.tzlocal()).strftime("%Y-%m-%d %H:%M:%S")

    ev.append( { 'start': start, 'event': name, 'venue': "Babycastles" } )

  ev = { "%s %s" % (e['start'], e['event']): e for e in ev }
  brico.common.write_json("castles.json", brico.events.datesort(ev.values()))
