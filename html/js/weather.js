// v3.1.0
//Docs at http://simpleweatherjs.com
$(document).ready(function() {
  getWeather(); //Get the initial weather.
  setInterval(getWeather, 600000); //Update the weather every 10 minutes.
});

function getWeather() {
  $.simpleWeather({
    location: '10011',
    woeid: '',
    unit: 'f',
    success: function(weather) {
      html = '<h2>&thinsp;<i class="icon-'+weather.code+'"></i>';
      html += weather.temp+'&deg;F '+weather.humidity + '%';
      html += '<span style="vertical-align: text-top; font-size:70%;">💦 </span>';
      html += '&thinsp;</h2>';
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
