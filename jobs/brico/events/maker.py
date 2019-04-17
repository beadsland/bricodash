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

events = []

for item in brico.common.meetup.events("fat-cat-fab-lab")[:8]:
  evt = item['name']
  dt = dateparser.parse(item['local_date'] + " " + item['local_time'])
  venue = "Fat Cat FAB LAB"
  events = { 'event': evt, 'start': dt, 'venue': venue }


# refactor eventbrite for generic venues at a generic address
