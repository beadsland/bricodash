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

import brico.common
import brico.slack

import os
import time
import pathlib

bot_token = brico.common.get_token("slack_bot_token")
app_token = brico.common.get_token("slack_app_token")
slack = brico.slack.Slack( app_token, bot_token )
channel = "netops"

def pull_path(f): return os.path.join(brico.common.pwd(), "../html/pull", f)

dir = os.listdir(pull_path("."))
dir = [f for f in dir if f.startswith("doorcam")]
dir = [f for f in dir if time.time() - os.path.getmtime(pull_path(f)) < 60 * 60]
touch = [f for f in dir if f.endswith(".touch")]
alert = [f for f in dir if f.endswith(".alert")]

down = [f for f in touch if time.time() - os.path.getmtime(pull_path(f)) > 30]

for f in down:
  alert = f.replace(".touch", ".alert")
  device = f.replace(".touch", "").replace("doorcam_", "")
  if (not os.path.exists(pull_path(alert))) \
      or os.path.getmtime(pull_path(alert)) < os.path.getmtime(pull_path(f)):
    slack.post(channel, "Bricodash on %s has stopped polling 🚪🎥 :'(" % device)
    pathlib.Path(pull_path(alert)).touch()

for f in alert:
  touch = f.replace(".alert", ".touch")
  device = f.replace(".alert", "").replace("doorcam_", "")
  if os.path.exists(pull_path(touch)) \
      and os.path.getmtime(pull_path(touch)) > os.path.getmtime(pull_path(f)):
    slack.post(channel, "Bricodash on %s has resumed polling 🚪🎥 :)" % device)
    os.remove(pull_path(f))
