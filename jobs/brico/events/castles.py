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

from ics import Calendar
import os
import datetime

import brico.common
import brico.common.html as html

calendar = "e5dh8b6plqo4sift6fbplkcqjg%40group.calendar.google.com"

def main():
  path = os.path.join( "https://calendar.google.com/calendar/ical",
                       calendar, "public/basic.ics" )
  response = brico.common.get_response(path)

  # Bugfix https://github.com/C4ptainCrunch/ics.py/issues/127
  ics = response.text.replace('BEGIN:VALARM\r\nACTION:NONE',
                              'BEGIN:VALARM\r\nACTION:DISPLAY\r\nDESCRIPTION:')

  today = str(datetime.date.today())
  c = Calendar(ics)

  events = []
  for e in c.events:
    if str(e.begin) > today:
      events.append(e)

  castles = html.img().clss('logo').style("margin-left: -.05em; vertical-align: -10%;").src("img/babycastles.png")
  events = [ { 'start': e.begin.to('local').format('YYYY-MM-DD HH:mm:ss'),
               'event': "%s (%s)" % (e.name, castles),
               'venue': "Babycastles" } for e in events ]
  brico.common.write_json("castles.json", brico.events.datesort(events))
