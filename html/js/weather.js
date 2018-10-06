/*
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
*/

'use strict';

// v3.1.0
//Docs at http://simpleweatherjs.com

function launch_weather() {
  toggleTemp();
  setInterval(toggleTemp, 5000)
  pollWeather();
  setInterval(pollWeather, 30 * 1000);
}

function pollWeather() {
  var xhttp = new XMLHttpRequest();
  xhttp.responseType = "json";
  xhttp.onreadystatechange = function() {
    removeStale("#weather");
    if (this.readyState == 4 && this.status == 200
                                            && 'tempf' in xhttp.response) {
      var w = xhttp.response;
      var div = document.querySelector("#weather");

      for (var key in xhttp.response) {
        div.querySelector("#"+key).innerHTML = w[key]
      };
      div.querySelector("#winds").innerHTML = Math.round(w.winds);
      div.querySelector("#winoji").innerHTML = feeloji("🍃", w.winds/15*100);
      div.querySelector("#humoji").innerHTML = feeloji("💦", w.humid);
      div.querySelector("#timestamp").setAttribute("epoch", w.epoch);
    };
    checkStale("#weather", 30 * 1000);
  }
  xhttp.open("GET", "pull/weather.json", true);
  xhttp.send();
}

function feeloji(str, percent) {
  return '<span style="font-size: ' + percent + '%;">' + str + '</span>'
}

function toggleTemp() {
  var div = document.querySelector("#weather");

  if ( $("#weather-ftemp").is(":visible") ) {
    $("#weather-ftemp").hide();
    $("#weather-ctemp").show();

    $("#weather-index").hide();
    if (div.querySelector("#tempf").innerHTML > 70) {
      $("#weather-humid").show();
    };

    $("#weather-chill").hide();
    if (div.querySelector("#tempf").innerHTML <= 70) {
      $("#weather-winds").show();
    };
  } else {
    $("#weather-ctemp").hide();
    $("#weather-ftemp").show();

    var tempf = parseInt(div.querySelector("#tempf").innerHTML, 10);

    if (tempf < parseInt(div.querySelector("#index").innerHTML, 10)) {
      $("#weather-humid").hide();
      $("#weather-index").show();
    } else if (tempf > parseInt(div.querySelector("#chill").innerHTML, 10)) {
      $("#weather-winds").hide();
      $("#weather-chill").show();
    };
  }
}
