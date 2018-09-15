<html>
  <head>
    <!--meta http-equiv="refresh" content="3600" -->
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

<div id="upper_row">
  <table width="100%">
    <tr><div id="outer_h1"></div></tr>
    <tr>
      <td>
        <div id="upper_left_column">
          <div id="inner_h1"><h1>Welcome to Hack Manhattan!</h1></div>
          <div id="event-schedule"><?php include "pull/events.html"?></div>
        </div>
      </td>
      <td>
        <div id="upper_right_column"><?php include "pane/camera.html"?></div>
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

<div id="mta-widget">
  <script type="text/javascript"
          src="http://www.mta.info/sites/all/libraries/mta_WidgetScripts/serviceStatusWidget.js"></script>
</div>

<div id="bottom_row">
  <div id="slack-chat"><?php include "pull/slack.html"?></div>
</div>


</body>
</html>
