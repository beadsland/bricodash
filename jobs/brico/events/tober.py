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

import dateutil.parser
import re

import brico.common
import brico.common.meetup
import brico.common.html as html

def main():
  events = brico.common.meetup.find("Hacktoberfest",
                                    ".keys/meetup_hacktoberfest")
  events += brico.common.meetup.find("Hacktober", ".keys/meetup_hacktober")

  def logoit(l): return html.img().clss('logo').src( l ).str()
  def dateit(e): return ' '.join([ e['local_date'], e['local_time'] ])
  def meetit(e): return '(%s)' % ' '.join([ e['group']['name'].strip(),
                                            logoit("img/meetup.png") ])
  def nameit(e): return u' '.join([ e['name'].strip(),
                                    logoit("img/tober.png"),
                                    meetit(e) ])

  events = [ { 'start': dateit(e), 'event': nameit(e), 'venue': "Holiday" }
             for e in events ]

  brico.common.write_json("tober.json", brico.events.datesort(events))
