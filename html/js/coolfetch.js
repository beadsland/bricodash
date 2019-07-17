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
/*

'use strict';

/*
  Wrapper for axios get to give us cleaner, fetch-like response as result.
*/
async function fetchlike(url, opt) {
  try {
    var response = await axios.get(url, opt);
    response['ok'] = true;
    return response;
  } catch (error) {
    if (error.response) {
      error.response['ok'] = false;
      return error.response;
    } else {
      return { ok: false }
    }
  }
}

/*
  Wrapper to carry over cooldown time since last bad fetch.
*/
async function coolfetch(snap, opt, cooldown, cool = null) {
  var response = await fetchlike(snap, opt);
  if (!response.ok) {
    response['cool'] = (new Date() / 1000) + cooldown;
  } else {
    if (cool > new Date() / 1000) {
      response['cool'] = cool
    }
  }
  return response
}
