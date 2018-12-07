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
 hols =  hanukkah()
 brico.common.write_json("multi.json", hols)

def hanukkah():
  # stopgap to deal with hanukkah until we have lunar calendar module
  first = datetime.date(2018, 12, 2)
  firsteve = brico.common.sunset( first )
  lasteve = brico.common.sunset( first + datetime.timedelta(days=8) )

  now = datetime.datetime.now(datetime.timezone.utc)
  sunset = brico.common.sunset(datetime.datetime.today())
  if now < firsteve:      event = "First Night of Hanukkah"
  elif now < lasteve:     event = menorah(first, sunset, now)

  try:
    return [ { 'start': sunset.replace(tzinfo=None).isoformat(),
               'venue': "Holiday", 'event': event } ]
  except:
    return []

def menorah(first, sunset, now):
  shamash = brico.common.html.span().style("font-size:150%").inner("🕯").str()

  day = sunset.date() - first
  if sunset > now:   day = day.days + 2
  else:              day = day.days + 1

  menorah = " " * (8-day) + "🕯" * day
  left = menorah[:4]
  right = menorah[4:]
  unlit = brico.common.html.span().style("opacity: .15").inner("🕯").str()
  space = re.compile(r' ')
  left  = space.sub(unlit, left)
  right = space.sub(unlit, right)
  menorah = "%s%s%s" % (left, shamash, right)

  return brico.common.html.emoji(menorah)
