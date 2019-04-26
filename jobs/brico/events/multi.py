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

import brico.events.lunar.jewish
import brico.events.lunar.winter
import brico.events.lunar.chinese
import brico.events.lunar.christian
import brico.events.lunar.muslim
import brico.events.lunar.sciencey

import datetime
import dateutil

def main():
  now = datetime.datetime.now(dateutil.tz.tzlocal());
  hols =  brico.events.lunar.chinese.main(now) \
         + brico.events.lunar.jewish.main(now) \
         + brico.events.lunar.winter.main(now) \
         + brico.events.lunar.christian.main(now) \
         + brico.events.lunar.muslim.main(now) \
         + brico.events.lunar.sciencey.main(now)
  brico.common.write_json("multi.json", hols)
