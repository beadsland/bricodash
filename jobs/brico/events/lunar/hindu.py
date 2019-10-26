####
## Copyright © 2019 Beads Land-Trujillo.
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
def midnight(now):
  return datetime.datetime.combine(now.date(), datetime.datetime.min.time())

def main(now):

#  for i in range(-3, 19):
#    diwali(now + datetime.timedelta(days=365*i))

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
  dwadashi = gregorian((hindu[0], hindu[1], 26, hindu[3]))
  first = gregorian((hindu[0], hindu[1], 27, hindu[3]))
  pratipad = next_pratipad(lunar_date(newmoon))
  last = gregorian((pratipad[0], pratipad[1], 1, pratipad[3]))

  # Library appears to be reporting gregorian day on which lunar tithi ends,
  # thus we use prior tithi to calculate gregorian day on which next tithi begins.

  if sunrise(newmoon.date()) > newmoon:
    diwali = newmoon.date() - datetime.timedelta(days=1)
  else:
    diwali = newmoon.date()

  # All the above is near-useless. The best available F/OSS Hindu calendar
  # library, written in Lisp, only provides for civil, or solar, days (divasa).
  # It does not expose lunar days (tithi). As lunar days vary in length, it is
  # not uncommon for an entire lunar day to begin and end in the course of a
  # solar day, or vice versa.
  #
  # Many Hindu holidays, including Diwali, occur in accordance with the lunar
  # calendar, but are celebrated following the civil calendar. However, which
  # lunar day maps back to any given solar day varies depending on context.
  # Usually, the solar day of a tithi is determined by sunrise. Yet for festivals
  # with evening celebrations, such as diwali, it is determined by sunset.
  # Where more than one sunset (or sunrise) occurs in the same tithi, the practice
  # appears to be to recognize the tithi on the later solar day.
  #
  # Our currently library not only fails to expose tithi, it also works with only
  # rough estimate of sunrise, and takes no account of geographic location. This
  # together with regional differences on the significance of historical events
  # leading up to the festival of lights, means that we really need to accurately
  # determine tithi start and end times to accurately identify local start and
  # end dates, and clearly indicate local vs. various national variants.
  #
  # Reference: http://www.astrojyoti.com/understanding-panchangam.htm
  # Calculation Validation: https://www.drikpanchang.com/diwali/diwali-puja-calendar.html

  emoji = brico.common.html.logo("img/ggl-diya.png", ":diya:")
  vary = brico.common.html.em("(%s)" % "varies")

  # We're hard-coding for now because we aren't calculating tithi correctly
  first = datetime.date(2019, 10, 25)
  diwali = datetime.date(2019, 10, 27)
  last = datetime.date(2019, 10, 29)

  if now < sunrise(first):
    (event, morn) = ("Diwali Begins %s %s" % (vary, emoji), sunrise(first))
  elif now.date() == first:
    (event, morn) = ("Happy Diwali! %s" % emoji, sunrise(first))
  elif now < sunrise(diwali):
    (event, morn) = ("Happy Diwali! %s" % emoji, midnight(now))
  elif now.date() < sunrise(diwali + datetime.timedelta(days=1)):
    (event, morn) = ("Happy Diwali! %s" % ''.join([emoji]*5), midnight.now())
  elif now.date() < sunrise(last + datetime.timedelta(days=1)):
    (event, morn) = ("Happy Diwali! %s" % emoji, midnight.now())
  else:
    (event, morn) = ("n/a", False)

  if not morn:
    return []
  else:
    return [{'start': iso(morn), 'venue': "Holiday", 'event': event},
            {'start': iso(sunrise(last + datetime.timedelta(days=1))),
             'venue': "Holiday", 'event': "Diwali Ends %s %s" % (vary, emoji)}]

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
