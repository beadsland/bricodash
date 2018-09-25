'use strict';

/*
 Start polling for back-end content.
 */
window.onload = function() {
  position_header();

  setInterval(renewCam, 1000);     /*  renewCam(); */
  setInterval(updateTime, 400);

  scheduleDiv("#slack-chat", "pull/slack.html", 30 * 1000);

  scheduleDiv("#space-events", "pull/space_events.html", 10 * 60 * 1000);
  scheduleDiv("#building-events", "pull/building_events.html", 10 * 60 * 1000);
  buildingCal()

  scheduleDiv("#mta-widget", "pane/mta.html", 60 * 1000);
  scheduleDiv("#wiki-edits", "pull/wiki.html", 30 * 60 * 1000);

  scheduleDiv("#random_photo", "pull/photo.html", 10 * 60 * 1000);
  peekawait();

  var urlParams = new URLSearchParams(window.location.search);
  if (urlParams.has("whoami") && urlParams.get("whoami") === "chromecast") {
    setInterval(rebootCast, 6 * 60 * 60 * 1000);

    scheduleDiv("#sous", "pull/sous.html", 250);
    setInterval(sousveil, 500)
  }
}

function rebootCast() {
  var oReq = new XMLHttpRequest();
  oReq.onload = function() { console.log("Rebooting self."); }
  oReq.open("get", "util/recast.php", true);
  oReq.send();
}

/*
 Sous veil ance
 */
function sousveil() {
  var veil = document.querySelector("#veil");
  var eye = document.querySelector("#eye");
  var vop = veil.getAttribute("value");
  var eop = eye.style.opacity;
  if (vop === localStorage.eye_opacity) {
    if (eop > 0) {
      eye.style.opacity = eop * .9;
    }
  } else {
    eye.style.opacity = vop;
  }
  localStorage.eye_opacity = vop;
}

/*
 Alternate between building and space calendars.
 */

function buildingCal() {
  $("#upper_left_column").hide()
  $("#upper_left_column_alt").show()
  setTimeout(spaceCal, 1*60000)
}

function spaceCal() {
  $("#upper_left_column_alt").hide()
  $("#upper_left_column").show()
  setTimeout(buildingCal, 4*60000)
}

/*
 Show random photo
 */

function peekawait() { setTimeout(peekaboo, 300000 + Math.random(600000)); }

function peekaboo() {  $("#peekaboo").show(3000, peekabout); }

function peekabout() { setTimeout(unpeekaboo, 2000); }

function unpeekaboo() { $('#peekaboo').hide(7000, peekawait); }

/*
 Position the H1
*/

function position_header() {
  console.log($(window).width())

  var h1 = "<h1>Welcome to Hack Manhattan!</h1>";
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
  var cam = document.querySelector("#door-cam");
  cam.src = cam.src;
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

  var mydiv = document.querySelector(divID);
  var e
  try {
    e = mydiv.querySelector("#timestamp").getAttribute("epoch");
  } catch (err) {
    e = 0;
  }

  var elapsed = new Date() / 1000 - e;

  if (elapsed > (interval / 1000 * 2)) {
    var err = document.createElement("div");
    err.className = "centered";
    var ico = document.createElement("span");
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

function updateTime() {
  var today = new Date();
  var h = checkTime(today.getHours());
  var m = checkTime(today.getMinutes());
  var s = checkTime(today.getSeconds());
  h = parseInt(h % 12, 10);
  if (h == 0) { h = 12 };
  var str = "&thinsp;" + h + ":" + m + ":" + s + "&thinsp;";
  document.getElementById('clock').innerHTML = str;
}
