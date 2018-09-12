
/*
  Start polling for back-end content.
*/
window.onload = function() {
  scheduleDiv("#slack-chat", "pull/slack.html", 60000);
  scheduleDiv("#event-schedule", "pull/events.html", 60000);
  startTime()
  scheduleCam()
}

/*
 Reload camera feed if broken.
*/

function scheduleCam() {
  var params = new URLSearchParams(window.location.search);
  if ( params.has("timelapse") && $.isNumeric(params.get("timelapse")) ) {
    interval = parseInt(params.get("timelapse"))
  } else {
    interval = 60; // ~ 15 Hz
  }
  src = document.querySelector("#doorcam").src;

  fixCam(src)
  setInterval(function() { fixCam(src); }, interval)
}

function fixCam(src) {
  document.querySelector("#doorcam").src = src + "&action=snapshot&now=" + Date.now()
  console.log(Date.now())
}

/*
 Load a text file from server.
*/

function scheduleDiv(divID, pullPath, interval) {
  updateDiv(divID, pullPath);
  setInterval(function() { updateDiv(divID, pullPath); }, interval);
}

function updateDiv(divID, pullPath) {
  var xhttp = new XMLHttpRequest();
  xhttp.responseType = "text";
  xhttp.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
      document.querySelector(divID).innerHTML = xhttp.response;
    };
  }
  xhttp.open("GET", pullPath, true);
  xhttp.send();
}

/*
 Clock
*/

// https://stackoverflow.com/questions/18229022/how-to-show-current-time-in-java$
function checkTime(i) {
  return (i < 10) ? "0" + i : i;
}

function startTime() {
  var today = new Date(),
      h = checkTime(today.getHours()),
      m = checkTime(today.getMinutes()),
      s = checkTime(today.getSeconds());
  h = parseInt(h % 12, 10);
  if (h == 0) { h = 12 };
  str = "&thinsp;" + h + ":" + m + ":" + s + "&thinsp;";
  document.getElementById('clock').innerHTML = str;
  t = setTimeout(function () {
      startTime()
  }, 500);
}
