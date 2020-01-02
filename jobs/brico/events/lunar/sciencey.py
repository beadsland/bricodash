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

import ephem
import datetime
import dateutil
import dateutil.tz as tz
import calendar

def main(now):
  return astron(now) + solar(now) + leap(now)

def leap(now):
  lday = "Leap Day " + brico.common.html.emoji("🤸‍♀️")
  if calendar.isleap(now.year) \
      and now < datetime.datetime(now.year, 3, 1, 0, 0, 0, tzinfo=tz.UTC):
    return [ { 'start': datetime.date(now.year, 2, 29).isoformat(),
               'venue': "Holiday", 'event': lday } ]
  elif calendar.isleap(now.year + 1):
    return [ { 'start': datetime.date(now.year+1, 2, 29).isoformat(),
               'venue': "Holiday", 'event': lday } ]
  else:
    return []

# saturday nearest first quarter moon nearest mid-april mid may
def astron(now):
  before = now - datetime.timedelta(days=60)
  dates = [ephem.next_spring_equinox(before), ephem.next_autumn_equinox(before)]
  dates = ["%s %s" % (d, ephem.next_first_quarter_moon(d)) for d in dates]
#  dates = [d.datetime().date() for d in dates]
#  print(dates)
  return []

def solar(now):
  yester = now - datetime.timedelta(days=1)
  return [ { 'start': toiso(ephem.next_spring_equinox(yester)),
             'venue': "Holiday",
             'event': "Vernal Equinox " + brico.common.html.emoji("♈︎") },
           { 'start': toiso(ephem.next_autumn_equinox(yester)),
             'venue': "Holiday",
             'event': "Autumnal Equinox " + brico.common.html.emoji("♎︎") },
           { 'start': toiso(ephem.next_summer_solstice(yester)),
             'venue': "Holiday",
             'event': "Summer Solstice " + brico.common.html.emoji("♋︎") },
           { 'start': toiso(ephem.next_winter_solstice(yester)),
             'venue': "Holiday",
             'event': "Winter Solstice " + brico.common.html.emoji("♑︎") },
         ]

def toiso(edate):
  utc = edate.datetime().replace(tzinfo=tz.UTC)
  return utc.astimezone(tz.tzlocal()).replace(tzinfo=None).isoformat()
