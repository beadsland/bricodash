// v3.1.0
//Docs at http://simpleweatherjs.com
$(document).ready(function() {
  getWeather(); //Get the initial weather.
  setInterval(getWeather, 600000); //Update the weather every 10 minutes.
  setInterval(toggleTemp, 5000);
});

function toggleTemp() {
  if ( $("#weather_temp").html() === localStorage.getItem("tempF") ) {
    $("#weather_temp").html(localStorage.getItem("tempC"))
  } else {
    $("#weather_temp").html(localStorage.getItem("tempF"))
  }
}

function newtoggleTemp() {
  console.log("toggle");
  if ( $("#weather_ftemp").is(":visible") ) {
    $("#weather_ftemp").hide();
    $("#weather_ctemp").show();
    console.log("yes")
  } else {
    $("#weather_ctemp").hide();
    $("#weather_ftemp").show();
    console.log("no")
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

      html  = span("", "emoji", "moon-" + weather.code);
      html += span("", "emoji", "icon-" + weather.code);
      html += span(localStorage.tempF, "", "weather_temp")
      html += " " + localStorage.humid;

      $("#weather").html('&thinsp;' + html + '&thinsp;');
      toggleTemp()
    },
    error: function(error) {
      $("#weather").html('<p>'+error+'</p>');
    }
  });
}
