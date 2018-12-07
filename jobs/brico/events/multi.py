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
import brico.events.lunar.jewish

import ephem
import datetime
import dateutil
import dateutil.tz as tz

def main():
  now = datetime.datetime.now(dateutil.tz.tzlocal());
  hols = [ brico.events.lunar.jewish.hanukkah(now), kwanzaa(now) ]
  hols = hols + solar(now)
  brico.common.write_json("multi.json", hols)

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
