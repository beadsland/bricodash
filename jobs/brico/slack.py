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

from brico.common.memoize import memoized
from slacker import Slacker

class Slack:
  def __init__(self, token):
    self.api = Slacker( token )

  @memoized
  def members(self):            return self.api.users.list().body['members']

  @memoized
  def emoji(self):              return self.api.emoji.list().body['emoji'];

  # not memoized 'cause kwargs'
  def history(self, **kwargs):  return self.api.channels.history(**kwargs)


  @memoized
  def channels(self):
    return { c['name']: c for c in self.api.channels.list().body['channels'] }

  @memoized
  def names(self):
    names = { u['id']: ( u['profile']['display_name'], u['name'] )
                                                    for u in self.members() }
    for id in names:
      names[id] = names[id][1] if names[id][0] == "" else names[id][0]
    return names

  @memoized
  def avatars(self):
    return { u['id']: u['profile']['image_32'] for u in self.members() }
