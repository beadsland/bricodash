
/*
  Start polling for back-end content.
*/
window.onload = function() {
  scheduleDiv("#slack-chat", "pull/slack.html", 60000);
  scheduleDiv("#event-schedule", "pull/events.html", 60000);
  scheduleCam(1000);
  startTime()
}

/*
 Reload camera feed if broken.
*/

function scheduleCam(interval) {
  fixCam()
  setInterval(function() { fixCam(); }, interval)
}

function fixCam() {
  cam = document.querySelector("#doorcam");
  cam.src = cam.src;
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
  str = "&thinsp;" + h + ":" + m + ":" + s + "&thinsp;";
  document.getElementById('clock').innerHTML = str;
  t = setTimeout(function () {
      startTime()
  }, 500);
}
