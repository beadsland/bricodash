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

import brico.events.lunar

import re
import datetime
import dateutil
import convertdate

def hanukkah():
  now = datetime.datetime.now(datetime.timezone.utc)
  today = datetime.datetime.today()

  first = datetime.date( *convertdate.holidays.hanukkah(today.year) ) \
          - datetime.timedelta(days=1)
  if first + datetime.timedelta(days=10) < now.date():
    first = datetime.date( *convertdate.holidays.hanukkah(today.year + 1) ) \
            - datetime.timedelta(days=1)

  firsteve = brico.events.lunar.sunset( first )
  lasteve = brico.events.lunar.sunset( first + datetime.timedelta(days=8) )

  if now < firsteve:
    event = "First Night of Hanukkah " + html.emoji("🕎");
    eve = firsteve
  elif now < lasteve:
    (event, eve) = menorah(first, now, today)

  try:
    return [ { 'start': eve.replace(tzinfo=None).isoformat(),
               'venue': "Holiday", 'event': event } ]
  except:
    return []

def menorah(first, now, today):
  sunset = brico.events.lunar.sunset( today )

  day = sunset.date() - first
  if sunset > now:
    sunset = brico.events.lunar.sunset( today - datetime.timedelta(days=1) )
    day = day.days
  else:
    day = day.days + 1

  shamash = brico.common.html.span().style("font-size:150%").inner("🕯").str()
  menorah = " " * (8-day) + "🕯" * day
  left = menorah[:4]
  right = menorah[4:]
  unlit = brico.common.html.span().style("opacity: .15").inner("🕯").str()
  space = re.compile(r' ')
  left  = space.sub(unlit, left)
  right = space.sub(unlit, right)
  menorah = "%s%s%s" % (left, shamash, right)

  return (brico.common.html.emoji(menorah), sunset)
