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

import brico.cloud
import brico.cloud.wiki
import brico.cloud.github
import brico.cloud.meetup
import brico.common

report = brico.cloud.wiki.main() + brico.cloud.github.main() \
         + brico.cloud.meetup.main()
report = sorted(report)
report = list(brico.cloud.line(s) for (t,s) in report)[-40:]

brico.common.write_pull("cloud.html", report)
