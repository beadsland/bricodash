
/*
 Start polling for back-end content.
 */
window.onload = function() {
  position_header()
  scheduleDiv("#slack-chat", "pull/slack.html", 60000);
  scheduleDiv("#event-schedule", "pull/events.html", 300000);
  updateMTA("#mta-widget", "#mta-loader", "pane/mta.html", 30000);
  startTime();
  renewCam();
}

/*
 Reload the MTA widget
*/

function scheduleMTA(divID, loadID, pullPath, interval) {
  updateMTA(divID, loadID, pullPath, interval);
  setInterval(function() { updateMTA(divID, loadID, pullPath, interval); }, interval);
}

function updateMTA(divID, loadID, pullPath, interval) {
  console.log(divID + loadID + new Date().toLocaleTimeString());
  $(divID).show();
  $(loadID).hide();
  updateDiv(loadID, pullPath, interval);
  setTimeout(function () { updateMTA(loadID, divID, pullPath, interval); }, interval);
}

/*
 Position the H1
*/

function position_header() {
  console.log($(window).width())

  h1 = "<h1>Welcome to Hack Manhattan!</h1>";
  if ($(window).width() < 1150) {
    document.querySelector("#inner_h1").innerHTML = "";
    document.querySelector("#outer_h1").innerHTML = h1;
  } else {
    document.querySelector("#outer_h1").innerHTML = "";
    document.querySelector("#inner_h1").innerHTML = h1;
  }
}

/*
 Reload camera feed if broken.
*/

function renewCam() {
  src = document.querySelector("#door-cam").src;
  lFunc = function() { return src; };
  fixCam(lFunc);
  setInterval(function() { fixCam(lFunc); }, 60000);
}

function fixCam(lFunc) {
  document.querySelector("#door-cam").src = lFunc();
}

/*
 Timelapse camera rather than live MJPG feed.
 Stalls on chromecast, so not used, but retained for possible future use.
 */

function lapseCam() {
  var params = new URLSearchParams(window.location.search);
  if ( params.has("timelapse") && $.isNumeric(params.get("timelapse")) ) {
    interval = parseInt(params.get("timelapse"))
  } else {
    interval = 60; // ~ 15 Hz
  }

  src = document.querySelector("#doorcam").src;
  lapseFunc = function () { return src + "&action=snapshot&now=" + Date.now() };

  fixCam(lapseFunc)
  setInterval(function() { fixCam(lapseFunc); }, interval)
}

/*
 Load a text file from server.
*/

function scheduleDiv(divID, pullPath, interval) {
  updateDiv(divID, pullPath, interval);
  setInterval(function() { updateDiv(divID, pullPath, interval); }, interval);
}

function updateDiv(divID, pullPath, interval) {
  var xhttp = new XMLHttpRequest();
  xhttp.responseType = "text";
  xhttp.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200 && xhttp.response.length > 0) {
      document.querySelector(divID).innerHTML = xhttp.response;
      checkStale(divID, interval);
    };
  }
  xhttp.open("GET", pullPath, true);
  xhttp.send();
}

/*
 Test if pull data is stale since last successful poll.
 */

function checkStale(divID, interval) {
  if (divID === "#mta-widget") { return; }; // short circuit
  if (divID === "#mta-loader") { return; }; // short circuit

  mydiv = document.querySelector(divID);
  try {
    e = mydiv.querySelector("#timestamp").getAttribute("epoch");
  } catch (err) {
    e = 0;
  }

  elapsed = new Date() / 1000 - e;

  if (elapsed > (interval / 1000 * 2)) {
    err = document.createElement("div");
    err.className = "centered";
    ico = document.createElement("span");
    ico.className = "timeout-error";
    err.appendChild(ico);
    mydiv.appendChild(err);
  }
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
