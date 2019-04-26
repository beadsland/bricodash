// https://stackoverflow.com/a/18229123

// Copyright (c) 2013 Tushar Gupta.
//
// Used under Attribution-ShareAlike 3.0 Unported (CC BY-SA 3.0)
// https://creativecommons.org/licenses/by-sa/3.0/

function checkTime(i) { return (i < 10) ? "0" + i : i; }

function updateTime() {
  var today = new Date();
  var h = checkTime(today.getHours());
  var m = checkTime(today.getMinutes());
  var s = checkTime(today.getSeconds());
  h = parseInt(h % 12, 10);
  if (h == 0) { h = 12 };
  var str = "&thinsp;" + h + ":" + m + ":" + s + "&thinsp;";
  node = document.getElementById('clock')
  node.innerHTML = str;

  if (document.getElementById('testing').innerHTML.startsWith("true")) {
    pass = document.getElementById('testpass')
    half = (parseInt( pass.innerHTML ) + 1) % 2
    pass.innerHTML = half

    if (half == 0) {
      var audio = document.getElementById("clock_tick");
      audio.loop = false;
      var promise = audio.play();
      if (promise) {
          promise.catch(function(error) { console.error("play error: ", error); });
          node.insertAdjacentHTML('afterbegin',
                                  '<span class="emoji">&thinsp;🕰️</span>')
      }
    }
  }
}
