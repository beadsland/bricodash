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

import brico.common.html
from brico.events.lunar import sunrise, sunset

import cl4py
import datetime
lisp = cl4py.Lisp()

def iso(dt): return dt.replace(tzinfo=None).isoformat()

def main(now):
  lisp.function('load')('vend/calendar.l')
  return holi(now)

def holi(now):
  today = lunar_date(now)
  holika = sunset(gregorian(next_happens(today, (12, (), 15, today[3]))))
  holimorn = sunrise(gregorian(next_happens(today, (12, (), 16, today[3]))))

  return [{'start': iso(holika), 'venue': 'Holiday',
           'event': "Holika Dahan %s" % brico.common.html.emoji("🔥")},
          {'start': iso(holimorn), 'venue': 'Holiday',
           'event': "Rangwali Holi %s" % brico.common.html.emoji("💛💚💙💜")},
           ]

def next_happens(today, lunar):
  if lisp.function('old-hindu-lunar-precedes')(today, lunar):
    return lunar
  else:
    return (lunar[0], lunar[1], lunar[2], lunar[3]+1)

def lunar_date(date):
  greg = (date.month, date.day, date.year)
  abs = lisp.function('absolute-from-gregorian')(greg)
  hind = lisp.function('old-hindu-lunar-from-absolute')(abs)
  return hind

def gregorian(lunar):
  abs = lisp.function('absolute-from-old-hindu-lunar')(lunar)
  greg = lisp.function('gregorian-from-absolute')(abs)
  date = datetime.date(greg[2], greg[0], greg[1])
  return date
