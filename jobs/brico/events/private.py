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

import icalevents.icalevents
import os
import dateparser
import copy
import dateutil.tz as tz
import re
import requests
import datetime

import brico.common
import brico.common.html as html
import brico.events

calendar = "hackmanhattan.com_jh33a7fosc2n010ukfr9lftfuo%40group.calendar.google.com"
gcal = html.logo("img/gcal.png")

def main():
  style = "margin-left: -.05em; vertical-align: -10%;"

  path = os.path.join( "https://calendar.google.com/calendar/ical",
                       calendar, "public/basic.ics" )
  space = brico.events.load_cals(["space.json"])

  file = requests.get(path).text
  file = re.sub(r'(UNTIL=[0-9]+);', r'\1T000000Z;', file)

  private = icalevents.icalevents.events(string_content = file.encode('utf-8'))
  for i, e in enumerate(private):
    if e.end - e.start < datetime.timedelta(hours = 3):
      e.end = e.start + datetime.timedelta(hours = 3)
    e.start = e.start.astimezone(tz.tzlocal()).strftime("%Y-%m-%dT%H:%M:%S")
    e.end = e.end.astimezone(tz.tzlocal()).strftime("%Y-%m-%dT%H:%M:%S")
  new = private

  for sp in space:
    end = dateparser.parse(sp['end'])
    start = dateparser.parse(sp['start'])
    if end - start < datetime.timedelta(hours = 3):
      sp['end'] = start + datetime.timedelta(hours = 3)
      sp['end'] = sp['end'].astimezone(tz.tzlocal()).strftime("%Y-%m-%dT%H:%M:%S")

  while len(space) > 0:
    new = []
    for e in private:
      if e.end <= space[0]['start']:      new.append(e)
      elif e.start >= space[0]['end']:    new.append(e)

      elif e.start >= space[0]['start']:
        if e.end <= space[0]['end']:
          pass
        else:
          e.start = space[0]['end']
          new.append(e)

      else:
        if e.end <= space[0]['end']:
          e.end = space[0]['start']
          new.append(e)
        else:
          f = copy.copy(e)
          f.start = space[0]['end']
          e.end = space[0]['start']
          new.append(e)
          new.append(f)
    private = new
    space.pop(0)

  ev = []
  for e in private:
    name = e.summary
    name = re.sub(r'Potluck *', "Potluck 🍲 ", name)
    ev.append( { 'start': e.start, 'end': e.end, 'venue': "Hack Manhattan",
                 'event': "%s %s: %s" % (gcal, "Reserved for", name) } )
  brico.common.write_json("private.json", brico.events.datesort(ev))
