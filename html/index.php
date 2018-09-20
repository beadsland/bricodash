<html>
  <head>
    <meta http-equiv="refresh" content="21600">
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

<div id="upper_row">
  <table width="100%">
    <tr><td colspan=2><div id="outer_h1"></div></td></tr>
    <tr>
      <td>
        <div id="upper_left_column">
          <div id="inner_h1"><h1>Welcome to Hack Manhattan!</h1></div>
          <div id="space-events"><?php include "pull/space_events.html"?></div>
        </div>
        <div id="upper_left_column_alt" style="display: none;">
          <div id="building-events"><?php include "pull/building_events.html"?></div>
        </div>
      </td>
      <td id="upper_right_td">
        <div id="upper_right_column"><?php include "pane/upper_right.php"?></div>
      </td>
    </tr>
    <tr>
      <td colspan=2>
        <div id="slack_head">Meanwhile, on
            <img src="img/slack.png" height="20"
                 style="vertical-align: baseline">hackerspace at
                 hackmanhattan.slack.com…</div>
      </td>
    <tr>
  </table>
</div>

<div id="mta-widget"><?php include "pane/mta.html"?></div>

<div id="bottom_row">
  <div id="slack-chat" class="container"><?php include "pull/slack.php"?></div>
</div>


</body>
</html>
