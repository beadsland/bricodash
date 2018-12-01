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

import brico.events
import brico.events.brite
import brico.events.upmeet
import brico.events.multi
import brico.events.holiday
import brico.events.tober
import brico.events.space
import brico.events.castles

import brico.common.html as html
import datetime
import os
import sys

###
# Update event source files
###

min = datetime.datetime.now().minute
hr  = datetime.datetime.now().hour

sunset = brico.common.sunset(datetime.datetime.now().date())
sunset = sunset + datetime.timedelta(minutes=1)
if min == sunset.minute and hr == sunset.hour:
                                              brico.events.holiday.main()
                                              brico.events.multi.main()

if min == 0 and hr % 12 == 0 or 'holiday' in sys.argv:
                                              brico.events.holiday.main()
if min == 0 and hr % 12 == 0 or 'multi' in sys.argv:
                                              brico.events.multi.main()

if min % 60 == 0 or 'brite' in sys.argv:      brico.events.brite.main()
if min % 60 == 0 or 'tober' in sys.argv:      brico.events.tober.main()
if min % 60 == 0 or 'castles' in sys.argv:    brico.events.castles.main()
if min % 30 == 0 or 'upmeet' in sys.argv:     brico.events.upmeet.main()
if min % 10 == 0 or 'space' in sys.argv:       brico.events.space.main()

###
# Build events component divs
###
evtSpce = []
for item in brico.events.community()[:10]:
  evtSpce.append( brico.events.line(brico.events.format(item)) )

evtBldg = []
header = html.span().id('ratparkHdr').inner("Rat Park Building Calendar")
evtBldg.append( html.span().clss('event').inner(header.str()).str() )
for item in brico.events.building()[:10]:
  venue = brico.events.venue(item['venue'])
  event = brico.events.format(item)
  evtBldg.append( brico.events.line("%s %s" % (venue, event)) )

brico.common.write_pull("space_events.html", evtSpce)
brico.common.write_pull("building_events.html", evtBldg)
