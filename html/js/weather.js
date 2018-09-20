'use strict';

// v3.1.0
//Docs at http://simpleweatherjs.com
$(document).ready(function() {
  getWeather(); //Get the initial weather.
  setInterval(getWeather, 600000); //Update the weather every 10 minutes.
  toggleTemp();
  setInterval(toggleTemp, 5000);
});

function toggleTemp() {
  if ( $("#weather-ftemp").is(":visible") ) {
    $("#weather-ftemp").hide();
    $("#weather-ctemp").show();

    $("#weather-hindx").hide();
    $("#weather-humid").show();
  } else {
    $("#weather-ctemp").hide();
    $("#weather-ftemp").show();

    if (localStorage.tempF < localStorage.feelsF) {
      $("#weather-humid").hide();
      $("#weather-hindx").show();
    }
  }
}

function span(str, cls, id) {
  if (id !== undefined) {
    return '<span class="' + cls + '" id="' + id + '">' + str + '</span>'
  } else {
    return '<span class="' + cls + '">' + str + '</span>'
  }
}

function hspan(str, percent) {
  return '<span style="font-size: ' + percent + '%;">' + str + '</span>'
}

function getWeather() {
  var hotmoji = '<img src="img/ggl-hot-face.png" style="height: .8em;">';

  $.simpleWeather({
    location: '10011',
    woeid: '',
    unit: 'f',
    success: function(weather) {
      document.querySelector("#weather-condn").innerHTML =
                            span("", "emoji", "moon-" + weather.code) +
                            span("", "emoji", "icon-" + weather.code);

      localStorage.tempF = weather.temp + span("℉", "degrees");
      localStorage.tempC = weather.alt.temp + span("℃", "degrees");
      document.querySelector("#weather-ftemp").innerHTML = localStorage.tempF;
      document.querySelector("#weather-ctemp").innerHTML = localStorage.tempC;

      localStorage.humid = weather.humidity + span("%", "degrees") +
                            hspan(span("💦", "emoji"), weather.humidity);
      document.querySelector("#weather-humid").innerHTML = localStorage.humid;

      localStorage.feelsF = weather.heatindex + span("℉", "degrees");
      document.querySelector("#weather-hindx").innerHTML = hotmoji +
                                                           localStorage.feelsF;

      toggleTemp()
    },
    error: function(error) {
      $("#weather").html('<p>'+error+'</p>');
    }
  });
}
