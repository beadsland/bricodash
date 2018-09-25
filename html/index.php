<html>
  <head>
    <!-- meta http-equiv="refresh" content="21600" -->
    <title>Hackerspace Dashboard - Hack Manhattan</title>

    <link rel="stylesheet" type="text/css" href="css/dash.css">
    <link rel="stylesheet" type="text/css" href="css/weather.css">
    <link rel="stylesheet" type="text/css" href="css/overlay.css">

    <meta charset="UTF-8">
    <link href="https://fonts.googleapis.com/css?family=Merriweather|Raleway:300,400" rel="stylesheet">
    <link href="https://fonts.googleapis.com/css?family=Lato" rel="stylesheet">

    <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.1.0/jquery.min.js"></script>
    <script src="js/launch.js"></script>
  </head>
<body>

<div class="container" id="random_photo"><?php include "pull/photo.html"?></div>

<div id="upper_row" class="container">

  <div class="top-left" style="z-index: 200;">
    <img id="eye" style="height:30%; opacity: 0;" src="img/eye.gif">
    <span id="sous"><?php include "pull/sous.html"?></span>
  </div>

  <table width="100%">
    <tr><td colspan=2><div id="outer_h1"></div></td></tr>
    <tr>
      <td><?php include "pane/events.html"?></td>
      <td id="upper_right_td"><div id="upper_right_column"><?php include "pane/upper_right.php"?></div>
      </td>
    </tr>
    <tr>
      <td colspan=2><?php include "pane/heads.html"?></td>
    </tr>
  </table>
</div>

<div id="mta-widget"><?php include "pane/mta.html"?></div>
<div id="wiki-edits"><?php include "pull/wiki.html"?></div>

<div id="bottom_row">
  <div id="slack-chat" class="container"><?php include "pull/slack.html"?></div></td>
</div>


</body>
</html>
