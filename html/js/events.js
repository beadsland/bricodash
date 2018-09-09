var oldOnLoad=window.onload;
window.onload = function() {
 oldOnLoad && oldOnLoad();
 retrieveData();
 setInterval(retrieveData, 300000);
}

function retrieveData() {
 var xhttp = new XMLHttpRequest();
 xhttp.responseType = "json";
 xhttp.onreadystatechange = function() {
     if (this.readyState == 4 && this.status == 200) {
       var scheduleDiv = document.querySelector("#event-schedule");
       var dateItems = xhttp.response
       scheduleDiv.innerHTML = "";

       dateItems.forEach(function(item){
         scheduleDiv.innerHTML += formatItem(item)
       });
     }
 };
xhttp.open("GET", "pull/events.json", true);
xhttp.send();
}

function formatItem(item) {
  var dt = "<dt>" + item.dt;
  var dd = "<dd>" + item.name;
  if (item.rsvp > 4) {
    dd += " (" + item.rsvp + ")";
  }
  return dt + dd
}
