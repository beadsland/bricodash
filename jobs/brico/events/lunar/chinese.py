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

import datetime
import lunarcalendar.festival

import brico.common.html
import brico.events.lunar

animals = ["🐉", "🐍", "🐎", "🐑", "🐒", "🐓", "🐕", "🐖", "🐀", "🐂", "🐅", "🐇"]

def main(now):
  event = "Chinese New Year"
  dates = [holiday(now.year, event), holiday(now.year + 1, event)]
  date = dates[1] \
     if dates[0] < datetime.date(now.year, now.month, now.day) else dates[0]
  event = "%s %s" % (event, animals[ (date.year - 2000) % 12 ])

  return [{ 'start': date.isoformat(), 'venue': 'Holiday', 'event': event }]

def holiday(year, event):
  for fest in lunarcalendar.festival.festivals:
    if fest.get_lang('en') == event:
      return fest(year)
