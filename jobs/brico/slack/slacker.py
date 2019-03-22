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

###
### Using legacy integrations. (deprecated)
###
### Replace with proper app.
###

from slacker import Slacker
from vend.memoize import memoized

class Slack:
  def __init__(self, app_token, bot_token=None):
    self.app = Slacker( app_token )
    self.bot = Slacker( bot_token )

    self.app_token = app_token
    self.bot_token = bot_token

  ###
  # Post a message to a channel
  ###
  def post(self, channel, str):
    self.app.chat.post_message("#%s" % channel, str)

  ###
  # Retrieve messages from a channel
  ###
  @memoized
  def messages(self, channel, count=10, oldest=0):
    history = self.history(channel = self.channels()[channel]['id'],
                           latest = None, oldest = oldest, count = count)
    return history.body['messages']

  ###
  # Queries against result
  ###
  @memoized
  def members(self):            return self.bot.users.list().body['members']

  # not memoized 'cause kwargs'
  def history(self, **kwargs):  return self.app.channels.history(**kwargs)

  ###
  # Generated lookup tables
  ###
  @memoized
  def channels(self):
    return { c['name']: c for c in self.app.channels.list().body['channels'] }

  @memoized
  def names(self, user=None):
    if not user:
      names = { u['id']: ( u['profile']['display_name'], u['name'] )
                                                    for u in self.members() }
      for id in names:
        names[id] = names[id][1] if names[id][0] == "" else names[id][0]
      return names
    else:
      return self.names()[user]

  @memoized
  def avatars(self, user=None, tag=None):
    if not user:
      return { u['id']: u['profile']['image_32'] for u in self.members() }
    else:
      return self.link( self.avatars()[user], tag )
