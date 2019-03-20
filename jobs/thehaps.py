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

import brico.slack

token = brico.common.get_token("slacker_token")
slack = brico.slack.Slack( token )

#if min == 0 and hr % 12 == 0 or 'holiday' in sys.argv:
channel = "bottest"
slack.post(channel, brico.common.slurp("threeday_events.slack"))
print(slack.messages(channel)[0])
