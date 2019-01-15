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
import vend.easter

import datetime

def main(now):
  cal = calendar(now.year) + calendar(now.year + 1);
  while cal[0]['start'] < (now - datetime.timedelta(days=1)).isoformat():
    pop(cal);
  return cal;

def calendar(year):
  easter = vend.easter.calc_easter(year)
  return [
          { 'start': (easter - datetime.timedelta(days = 47)).isoformat(),
            'venue': "Holiday",
            'event': "Mardis Gras " + brico.common.html.emoji("🎭⚜") },
          { 'start': (easter - datetime.timedelta(days = 46)).isoformat(),
            'venue': "Holiday",
            'event': "Ash Wednesday " + brico.common.html.emoji("⛪") },
          { 'start': (easter - datetime.timedelta(days = 7)).isoformat(),
            'venue': "Holiday",
            'event': "Palm Sunday " + brico.common.html.emoji("🌴") },
          { 'start': (easter - datetime.timedelta(days = 2)).isoformat(),
            'venue': "Holiday",
            'event': "Good Friday " + brico.common.html.emoji("⛪") },
          { 'start': easter.isoformat(),
            'venue': "Holiday",
            'event': "Easter Sunday " + brico.common.html.emoji("🐰") },
        ]
