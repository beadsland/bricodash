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

###
# Sunset for holidays and triggering holiday cron
###

from vend.memoize import memoized
import brico.common
import astral
import ephem

@memoized
def sunrise(date):
  a = astral.Astral()
  a.solar_depression = 'civil'
  city = a[brico.common.city()]
  sun = city.sun(date=date, local=True)

  return sun['sunrise']

@memoized
def sunset(date):
  a = astral.Astral()
  a.solar_depression = 'civil'
  city = a[brico.common.city()]
  sun = city.sun(date=date, local=True)

  return sun['sunset']

@memoized
def moonrise(date):
  e = ephem.Observer()
  e.lat = str(brico.common.lat())
  e.lon = str(brico.common.lon())
  e.date = date
  return e.previous_rising(ephem.Moon())

@memoized
def moonset(date):
  e = ephem.Observer()
  e.lat = str(brico.common.lat())
  e.lon = str(brico.common.lon())
  e.date = date
  return e.next_setting(ephem.Moon())
