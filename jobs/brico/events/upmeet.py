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

import re

import brico.common
import brico.common.meetup
import brico.common.html as html

def meetup(s):
  return "%s %s" % ( s, html.img().clss('logo').src("img/meetup.png").str() )

def main():
  events = brico.common.meetup.find("Offside Tavern", ".keys/meetup_upmeet")
  ratpark = []

  lstevt = ""
  lstday = ""
  for event in events:
    if "venue" in event and event['venue']['name'] == "Offside Tavern":
      name = event['name'].strip()
      date = event['local_date']
      if name != lstevt and date != lstday:
        lstevt = name.strip()
        lstday = date
        name = re.sub(' Wednesday! FREE!', ' Wed!', name)
        ratpark.append( { 'start': ' '.join( [date, event['local_time']] ),
                          'event': meetup(name), 'venue': "Offside Tavern" } )

  brico.common.write_json( "upmeet.json", brico.events.datesort(ratpark) )
