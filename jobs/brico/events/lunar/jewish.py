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
import brico.events.lunar

import re
import datetime
import dateutil.tz
import convertdate

def main(now): return purim(now) + passover(now) + hanukkah(now) \
                      + rosh_hashanah(now) + yom_kippur(now) + sukkot(now)

def iso(dt): return dt.replace(tzinfo=None).isoformat()

def purim(now): return one_day(now, "Purim", "🕍", "🕍")

def passover(now):
  first = holiday("passover", now, 8)
  firsteve = brico.events.lunar.sunset( first )
  lasteve = brico.events.lunar.sunset( first + datetime.timedelta(days=8) )

  unlev = brico.common.html.emoji("🍞🚫")
  if now < firsteve:
    (event, eve) = ("First Night of Passover " + unlev, firsteve)
  elif now < lasteve:
    (event, eve) = ("Passover Ends (≈⁂) " + unlev, lasteve)
  bound = { 'start': iso(eve), 'venue': "Holiday", 'event': event }

  if firsteve < now < lasteve:
    greet = "<em>Chag Kashruth Pesach</em> (Happy Kosher Passover) " + unlev
    happy = { 'start': now.date().isoformat(), 'venue': "Holiday",
              'event': greet }
    return [ bound, happy ]
  else: return [ bound ]

def passover(now):
  return multi_day(now, "Passover", 8, "🍞🚫",
                   "<em>Chag Kashruth Pesach</em> (Happy Kosher Passover)")

def hanukkah(now):
  first = holiday("hanukkah", now, 8)
  firsteve = brico.events.lunar.sunset( first )
  lasteve = brico.events.lunar.sunset( first + datetime.timedelta(days=8) )

  if now < firsteve:
    event = "First Night of Hanukkah " + brico.common.html.emoji("🕎");
    eve = firsteve
  elif now < lasteve:
    (event, eve) = menorah(first, now)

  return [{ 'start': iso(eve), 'venue': "Holiday", 'event': event }]

def rosh_hashanah(now):
  return multi_day(now, "Rosh Hashanah", 2, "🍎🍯",
                   "<em>Shanah tovah um’tukah</em> (Good and sweet new year)")

def yom_kippur(now):    return one_day(now, "Yom Kippur", "", "🍽️")

def sukkot(now):
  return multi_day(now, "Sukkot", 7, "🌿🌾🌿🍋",
                   "<em>Chag Sameach</em> (Joyous Festival)")

def one_day(now, hol, emobeg, emoend):
  first = holiday( hol.replace(" ", "_").lower(), now )
  firsteve = brico.events.lunar.sunset( first )
  lasteve = brico.events.lunar.sunset( first + datetime.timedelta(days=1) )

  emobeg = brico.common.html.emoji(emobeg)
  emoend = brico.common.html.emoji(emoend)

  if now < firsteve:
    (event, eve) = ("%s Begins %s" % (hol, emobeg), firsteve)
  elif now < lasteve:
    (event, eve) = ("%s Ends (≈⁂) %s" % (hol, emoend), lasteve)

  return [{ 'start': iso(eve), 'venue': "Holiday", 'event': event }]

def multi_day(now, hol, days, emoji, greet):
  first = holiday(hol.replace(" ", "_").lower(), now, days)
  firsteve = brico.events.lunar.sunset( first )
  lasteve = brico.events.lunar.sunset( first + datetime.timedelta(days=days) )

  emoji = brico.common.html.emoji(emoji)

  if now < firsteve:
    (event, eve) = ("First Night of %s %s" % (hol, emoji), firsteve)
  elif now < lasteve:
    (event, eve) = ("%s Ends (≈⁂) %s" % (hol, emoji), lasteve)
  bound = { 'start': iso(eve), 'venue': "Holiday", 'event': event }

  if firsteve < now < lasteve:
    happy = { 'start': now.date().isoformat(), 'venue': "Holiday",
              'event': "%s %s" % (greet, emoji) }
    return [ bound, happy ]
  else: return [ bound ]

def unlit():
  return brico.common.html.span().style("opacity: .15").inner("🕯").str()

def menorah(first, now):
  sunset = brico.events.lunar.sunset( now.date() )

  day = sunset.date() - first
  if sunset > now:
    sunset = brico.events.lunar.sunset( now - datetime.timedelta(days=1) )
    day = day.days
  else:
    day = day.days + 1

  shamash = brico.common.html.span().style("font-size:150%").inner("🕯").str()
  menorah = " " * (8-day) + "🕯" * day
  left = menorah[:4]
  right = menorah[4:]
  space = re.compile(r' ')
  left  = space.sub(unlit(), left)
  right = space.sub(unlit(), right)
  menorah = "%s%s%s" % (left, shamash, right)

  return (brico.common.html.emoji(menorah), sunset)

def holiday(name, now, days=1):
  last = holiday_eve(name, now) + datetime.timedelta(days=days)
  ends = brico.events.lunar.sunset( last )
  if ends <= now:
    then = now + datetime.timedelta(days=365)
    return holiday_eve(name, then)
  else:
    return holiday_eve(name, now)

def holiday_eve(name, now):
  method = getattr( convertdate.holidays, name )
  return datetime.date(*method(now.year)) - datetime.timedelta(days=1)
