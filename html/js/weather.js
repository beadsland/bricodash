// v3.1.0
//Docs at http://simpleweatherjs.com
$(document).ready(function() {
  getWeather(); //Get the initial weather.
  setInterval(getWeather, 600000); //Update the weather every 10 minutes.
  setInterval(toggleTemp, 5000);
});

function toggleTemp() {
  if ( $("#weather-ftemp").is(":visible") ) {
    $("#weather-ftemp").hide();
    $("#weather-ctemp").show();
  } else {
    $("#weather-ctemp").hide();
    $("#weather-ftemp").show();
  }
}

function span(str, cls, id) {
  if (id !== undefined) {
    return '<span class="' + cls + '" id="' + id + '">' + str + '</span>'
  } else {
    return '<span class="' + cls + '">' + str + '</span>'
  }
}

function getWeather() {
  $.simpleWeather({
    location: '10011',
    woeid: '',
    unit: 'f',
    success: function(weather) {
      localStorage.tempF = weather.temp + span("℉", "degrees");
      localStorage.tempC = weather.alt.temp + span("℃", "degrees");

      localStorage.humid = weather.humidity
                          + span("%", "degrees") + span("💦", "emoji");

      document.querySelector("#weather-condn").innerHTML =
                            span("", "emoji", "moon-" + weather.code) +
                            span("", "emoji", "icon-" + weather.code);
      document.querySelector("#weather-ftemp").innerHTML = localStorage.tempF;
      document.querySelector("#weather-ctemp").innerHTML = localStorage.tempC;
      document.querySelector("#weather-humid").innerHTML = localStorage.humid;

      toggleTemp()
    },
    error: function(error) {
      $("#weather").html('<p>'+error+'</p>');
    }
  });
}
