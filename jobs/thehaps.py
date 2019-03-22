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

import brico.slack

channel = "thehaps"
user = "Bricodash" # API does not provide for discovery of bot's own name or ID

bot_token = brico.common.get_token("slack_bot_token")
app_token = brico.common.get_token("slack_app_token")
slack = brico.slack.Slack( app_token, bot_token )

epoch = datetime.datetime(1970,1,1)
i = datetime.datetime.now()
delta_time = (i - epoch - datetime.timedelta(days = 3)).total_seconds()
recent = slack.messages(channel, 100, delta_time)
recent = (m for m in recent if 'username' in m.keys() and m['username'] == user)

cid = slack.channels()[channel]["id"]
for r in recent: slack.api.chat.delete(cid, r['ts'])
slack.post(channel, brico.common.slurp("threeday_events.slack"))
