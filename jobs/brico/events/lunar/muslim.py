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
import brico.common.html as html

from ummalqura.hijri_date import HijriDate
import datetime
import ephem

astromoji = "".join([ "(", html.emoji("🔭🌑"), " / ", html.emoji("🇺🇸"), ")" ])
nakedmoji = "".join([ "(", html.emoji("👁️🌒"), " / ", html.em("varies"), ")" ])
ramadmoji = " ".join([ "First Night of Ramaḍān", html.emoji("☪️") ])
shawwmoji = " ".join([ "Eid al-Fitr (End of Ramaḍān)", html.emoji("🍽🛐️") ])
ramgreet = " ".join([ html.em("Ramaḍān Kareem"), "(Noble Ramadan)",
                      html.emoji("🌅🌇") ])
fitgreet = " ".join([ html.em("Eid Mubarak"), "(Blessed Eid)", html.emoji("🍽🛐️")])
endfmoji = " ".join([ "End of Eid al-Fitr", html.emoji("🍽🛐️") ])

def iso(dt): return dt.isoformat()

def main(now): return ramadan(now);

def ramadan(now):
  now = now.replace(tzinfo=None)
  then = now - datetime.timedelta(days = 31)
  um = HijriDate(then.year, then.month, then.day, gr=True)
  if (um.month < 10):
    um = HijriDate.get_georing_date('%d-08-28' % um.year)
  else:
    um = HijriDate.get_georing_date('%d-08-28' % (um.year + 1))

  events = []

  # Start of Ramadan
  (astroR, nakedR) = new_month(um)
  if astroR != nakedR:
    events.append(( astroR, "%s %s" % (ramadmoji, astromoji) ))
  events.append(( nakedR, "%s %s" % (ramadmoji, nakedmoji) ))

  # Current day in Ramadan
  (astroS, nakedS) = new_month(um + datetime.timedelta(days = 28))
  if astroR < now < nakedS:
    events.append(( datetime.datetime.combine(now.date(),
                                              datetime.datetime.min.time()),
                    ramgreet ))

  # Start of Eid
  if now < nakedS:
    if astroS != nakedS and now < astroS:
      events.append(( astroS, "%s %s" % (shawwmoji, astromoji) ))
    events.append(( nakedS, "%s %s" % (shawwmoji, nakedmoji) ))

  # Current day in Eid
  astroE = brico.events.lunar.sunset(astroS.date() + datetime.timedelta(days=3))
  astroE = astroE.replace(tzinfo=None)
  nakedE = brico.events.lunar.sunset(nakedS.date() + datetime.timedelta(days=3))
  nakedE = nakedE.replace(tzinfo=None)

  if nakedS < now < nakedE:
    events.append(( datetime.datetime.combine(now.date(),
                                              datetime.datetime.min.time()),
                    fitgreet ))
  elif astroS < now < nakedE:
    events.append(( datetime.datetime.combine(now.date(),
                                              datetime.datetime.min.time()),
                    ' '.join([fitgreet, astromoji]) ))


  # End of Eid
  if now < nakedE:
    if astroE != nakedE and now < astroE:
      events.append(( astroE, "%s %s" % (endfmoji, astromoji) ))
    events.append(( nakedE, "%s %s" % (endfmoji, nakedmoji) ))

  # Strip off events that have already happened
  while events and events[0][0].date() < now.date():  events.pop(0)

  events = [ {'start': iso(t[0]), 'venue': "Holiday",
              'event': t[1]} for t in events ]

  return events

# Estimating astronomical siting per:\
# http://www.arabnews.com/node/1302826/saudi-arabia
def new_month(date):
  newmn = ephem.next_new_moon(date).datetime()
  sight = newmn + datetime.timedelta(seconds = 15*60*60)

  astro = None
  first = None
  day = date
  while first is None:
    day = day + datetime.timedelta(days = 1)
    sunset = brico.events.lunar.sunset(day).replace(tzinfo=None)

    if sunset > newmn and astro is None:
      astro = sunset

    if sunset > sight:
      moonrise = brico.events.lunar.moonrise(sunset).datetime()
      moonset = brico.events.lunar.moonset(moonrise).datetime()
      if moonset > sight:
        diff = min([moonset, sunset]) - max([moonrise, sight])
        if diff >= datetime.timedelta(seconds = 30*60):
          first = sunset

  return (astro, first)

# https://pypi.org/project/ummalqura/
