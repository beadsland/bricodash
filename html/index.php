<html>
  <head>
    <meta http-equiv="refresh" content="3600">
    <title>Hackerspace Dashboard - Hack Manhattan</title>

    <link rel="stylesheet" type="text/css" href="css/dash.css">
    <link rel="stylesheet" type="text/css" href="css/weather.css">
    <link rel="stylesheet" type="text/css" href="css/overlay.css">

    <meta charset="UTF-8">
    <link href="https://fonts.googleapis.com/css?family=Merriweather|Raleway:300,400" rel="stylesheet">

    <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.1.0/jquery.min.js"></script>
    <script src="js/launch.js"></script>
  </head>
<body>

<div style="height: 336px" id="upper_row">
  <table width="100%">
    <tr>
      <td>
        <div style="flex: 1; height: 336px; overflow: hidden;">
          <h1>Welcome to Hack Manhattan!</h1>
          <div id="event-schedule"><?php include "pull/events.html"?></div>
        </div>
      </td>
      <td width="448">
        <div style="width: 448px;"><?php include "pane/camera.html"?></div>
      </td>
    </tr>
  </table>
</div>

<div id="bottom_row">
    <div id="slack-chat"><?php include "pull/slack.html"?></div>
</div>

</body>
</html>

<!--
      <div class="slackhead" style="position: absolute; bottom: 0; margin: 0; z-index:5">
            Meanwhile, on the hackmanhattan.slack.com
           <img src="img/slack.png" height="20" style="vertical-align: middle">hackerspace channel...</div>
-->
