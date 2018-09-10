
/*
  Start polling for back-end content.
*/
window.onload = function() {
  scheduleDiv("#slack-chat", "pull/slack.html", 60000);
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
