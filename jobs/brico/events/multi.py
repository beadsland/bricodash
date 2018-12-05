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
import brico.common.html

import re
import datetime

def main():
  # stopgap to deal with hanukkah until we have lunar calendar module
  first = datetime.date(2018, 12, 2)

  sets = []
  shamash = brico.common.html.span().style("font-size:150%").inner("🕯").str()

  for i in range(9):
    sunset = brico.common.sunset( first + datetime.timedelta(days=i) )

    menorah = " " * (8-i-1) + "🕯" * (i+1)
    left = menorah[:4]
    right = menorah[4:]
    unlit = brico.common.html.span().style("opacity: .15").inner("🕯").str()
    space = re.compile(r' ')
    left  = space.sub(unlit, left)
    right = space.sub(unlit, right)
    menorah = "%s%s%s" % (left, shamash, right)

    sets.append( { 'start': sunset.replace(tzinfo=None),
                   'venue': "Holiday",
                   'event': brico.common.html.emoji(menorah) } )

  now = datetime.datetime.now()
  if   now < sets[0]['start']: arr = []
  elif now > sets[8]['start']: arr = []
  else:
    while now > sets[1]['start']: sets.pop(0)
    arr = [ { 'start': sets[0]['start'].isoformat(),
              'venue': "Holiday",
              'event': sets[0]['event'].encode().decode('utf-8') } ]

  brico.common.write_json("multi.json", arr)
