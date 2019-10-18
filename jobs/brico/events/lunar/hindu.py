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
from brico.events.lunar import sunrise, sunset

import os
import datetime
import ephem
import pytz
import dateutil

import cl4py
lisp = cl4py.Lisp()
lisp.function('load')(os.path.join(brico.common.pwd(), 'vend/calendar.l'))

def iso(dt): return dt.replace(tzinfo=None).isoformat()

def main(now):

  for i in range(-3, 19):
    diwali(now + datetime.timedelta(days=365*i))

  return holi(now) + diwali(now)

def holi(now):
  today = lunar_date(now)
  holika = sunset(gregorian(next_happens(today, (12, (), 15, today[3]))))
  holimorn = sunrise(gregorian(next_happens(today, (12, (), 16, today[3]))))

  return [{'start': iso(holika), 'venue': 'Holiday',
           'event': "Holika Dahan %s" % brico.common.html.emoji("🔥")},
          {'start': iso(holimorn), 'venue': 'Holiday',
           'event': "Rangwali Holi %s" % brico.common.html.emoji("💛💚💙💜")},
           ]

def diwali(now):
  then = now - datetime.timedelta(days = 30)
  equin = ephem.next_autumn_equinox(then).datetime()
  navaratri = gregorian(next_pratipad(lunar_date(equin)))
  newmoon = ephem.next_new_moon(navaratri).datetime().replace(tzinfo=pytz.UTC)

  hindu = lunar_date(newmoon)

  # Examine whether library actually calculates tithi and whether they can be extracted.

  # Should calculate all dates based on India Standard Timezone

  # "A particular day is ruled by the tithi at Sunrise"

  # Calendar day of a tithi is deemed to be calendar day of start of tithi


  # Library appears to be reporting gregorian day on which lunar tithi ends,
  # thus we use prior tithi to calculate gregorian day on which next tithi begins.

  # 2016 Deepawali started two days earlier???
  # 2018 Deepawali started one day earlier???

  # 2021 Deepawali starts one day earlier, we calculate Diwali for same day but ending day earlier also???

  # If these calculations are correct, Diwali in 2028 ought to be only 4 days.

  ##
  # Solar day is determined by last muharat (sunset period) during the tithi...
  #
  # 2016: Dwadashi tithi Oct 26 2:30 to Oct 27 4:14 <-- muharat on 26th
  #     : Dhantaras ends Oct 28 6:21 <-- second of two muharat, so 28th is solar day
  #
  ##

  dwadashi = gregorian((hindu[0], hindu[1], 26, hindu[3]))
  first = gregorian((hindu[0], hindu[1], 27, hindu[3]))
  pratipad = next_pratipad(lunar_date(newmoon))
  last = gregorian((pratipad[0], pratipad[1], 1, pratipad[3]))

  if sunrise(newmoon.date()) > newmoon:
    diwali = newmoon.date() - datetime.timedelta(days=1)
  else:
    diwali = newmoon.date()

  print(dwadashi, first, diwali, last)

  emoji = brico.common.html.logo("img/ggl-diwa.png")

  if now < sunrise(first):
    (event, morn) = ("Diwali Begins %s" % emoji, sunrise(first))
  elif now.date() == first.date():
    (event, morn) = ("Happy Diwali! %s" % emoji, sunrise(first))
  elif now < sunrise(diwali):
    (event, morn) = ("Happy Diwali! %s" % emoji, now.date())
  elif now.date() < sunrise(diwali + datetime.timedelta(days=1)):
    (event, morn) = ("Happy Diwali! %s" % ''.join([emoji]*5), now.date())
  elif now.date() < sunrise(last + datetime.timedelta(days=1)):
    (event, morn) = ("Happy Diwali! %s" % emoji, now.date())
  else:
    (event, morn) = ("n/a", False)

  if not morn:
    return []
  else:
    return [{'start': iso(morn), 'venue': "Holiday", 'event': event},
            {'start': iso(sunrise(last + datetime.timedelta(days=1))),
             'venue': "Holiday", 'event': "Diwali Ends %s" % emoji}]

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

  if abs == ():
    if lunar[2] < 30:
      return gregorian((lunar[0], lunar[1], lunar[2]+1, lunar[3]))
    else:
      return gregorian(next_pratipad((lunar[0], lunar[1], 1, lunar[3])))

  greg = lisp.function('gregorian-from-absolute')(abs)
  date = datetime.date(greg[2], greg[0], greg[1])
  return date

def next_pratipad(lunar):
  pratipad = gregorian((lunar[0], lunar[1], 1, lunar[3]))
  nextmonth = lunar_date(pratipad + datetime.timedelta(days=31))
  return (nextmonth[0], nextmonth[1], 1, nextmonth[3])
