#!/usr/bin/env python3

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
import brico.common
import brico.weather.open
#import brico.weather.dark
#import brico.weather.accu
#import brico.weather.mashup

coord = (40.7383652,-73.9983442)
zipcd = 10011

min = datetime.datetime.now().minute

if 1:                 w = brico.weather.open.poll(zipcd)
#if min % 2:           brico.weather.dark.poll(coord)
#if min % 30:          brico.weather.accu.poll(coord)

#weather.mashup.update()

brico.common.write_json("weather.json", w)
