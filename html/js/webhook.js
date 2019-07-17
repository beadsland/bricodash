/*
<!--
####
## Copyright © 2019 Beads Land-Trujillo.
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

incoming-webhooks App API was made by a member of the Slack team to help
connect Slack with a third-party service; these apps may not be tested,
documented, or supported by Slack in the way we support our core offerings,
like Slack Enterprise Grid and Slack for Teams. You may provide feedback
about these apps at <mailto:feedback@slack.com>.

It only uses data Slack already has access to (view our Privacy Policy to
learn more). By enabling and/or using this app, you may be connecting with
a service that is not part of Slack.

Getting started: https://api.slack.com/incoming-webhooks
*/

'use strict';

async function gethook(hook_url) {
  var response = await fetch(hook_url)
  var hook = await response.text()
  return hook
}

async function throwhook(hook, msg) {
  await fetch(hook, { method: 'POST', body: JSON.stringify( { text: msg } ) });
  console.log(msg)
}
