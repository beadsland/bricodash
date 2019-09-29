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

import datetime

def main(now):
  return programmer(now) + skeptic(now)

def skeptic(now):
  firsts = (datetime.date(now.year, m, 1) for m in range(1, 13))
  then = now + datetime.timedelta(days=365)
  secnds = (datetime.date(then.year, m, 1) for m in range(1, 13))
  thirts = (list(day for day in firsts if day.weekday() == 6)[0],
            list(day for day in secnds if day.weekday() == 6)[0])
  skeptc = thirts[1] if thirts[0] < now.date() else thirts[0]
  skeptc = skeptc + datetime.timedelta(days=12)
  return [ { 'start': skeptc.isoformat(), 'venue': 'Holiday',
             'event': "International Skeptics Day "
                      + brico.common.html.emoji("🤔") } ]

def programmer(now):
  days = programmer_byyear(now.year) + programmer_byyear(now.year + 1)
  return [{'start': d['start'].isoformat(), 'venue': 'Holiday', 'event': d['event']}
          for d in days if d['start'] >= now.date()]

def programmer_byyear(year):
  return [ {'start': datetime.date(year, 1, 7), 'venue': 'Holiday',
            'event': "Day of the Programmer (Historical) "
                     + brico.common.html.emoji("⌨")},
           {'start': datetime.date(year, 1, 1) + datetime.timedelta(days = 255),
            'venue': 'Holiday',
            'event': "Day of the Programmer (Canonical) "
                     + brico.common.html.emoji("⌨")} ]
