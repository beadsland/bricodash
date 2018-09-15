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

function getWeather() {
  $.simpleWeather({
    location: '10011',
    woeid: '',
    unit: 'f',
    success: function(weather) {
      localStorage.tempF = weather.temp + '<span class="degrees">℉</span>';
      localStorage.tempC = weather.alt.temp + '<span class="degrees">℃</span>';

      html = '&thinsp;<span class="emoji" id="moon-'+weather.code+'"></span>';
      html += '<span class="emoji" id="icon-'+weather.code+'"></span>';
      html += '<span id="weather_temp">' + localStorage.tempF + '</span> '
      html += weather.humidity + '<span class="degrees">%</span>';
      html += '<span class="emoji">💦</span>';
      html += '&thinsp;';
//      html += '<ul><li>'+weather.city+', '+weather.region+'</li>';
//      html += '<li class="currently">'+weather.currently+'</li>';
//      html += '<li>'+weather.wind.direction+' '+weather.wind.speed+' '+weather.units.speed+'</li></ul>';

      $("#weather").html(html);
    },
    error: function(error) {
      $("#weather").html('<p>'+error+'</p>');
    }
  });
}
