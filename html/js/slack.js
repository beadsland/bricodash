var oldOnLoad_sl=window.onload;

window.onload = function() {
 oldOnLoad_sl && oldOnLoad_sl();
 retrieveChat();
 setInterval(retrieveChat, 30000);
}

function retrieveChat() {
 var xhttp = new XMLHttpRequest();
 xhttp.responseType = "json";
 xhttp.onreadystatechange = function() {

     if (this.readyState == 4 && this.status == 200) {
       var scheduleDiv = document.querySelector("#slack-chat");
       var dateItems = xhttp.response
       scheduleDiv.innerHTML = "";

       dateItems.forEach(function(item) {
         scheduleDiv.innerHTML += item;
       });
     }
 };
xhttp.open("GET", "pull/slack.json", true);
xhttp.send();
}
