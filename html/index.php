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

  <div class="right" style="float: right; width: 448px;">
    <div class="container" style="z-index: 5; position: absolute; top: 0;">
      <!-- doorcam: 640 x 480 -->
      <img id="doorcam" width="448" height="336"
           src="http://hackmanhattan.duckdns.org:8888/hm/dash/util/camera.php?view=door">
      <div class="bottom-right" style="bottom:55">
        <span id="time"></span>
      </div>
      <script src="js/time.js"></script>

      <div class="top-right""><span id="weather"></span></div>
      <script src="https://cdnjs.cloudflare.com/ajax/libs/jquery.simpleWeather/3.1.0/jquery.simpleWeather.min.js"></script>
      <script src="js/weather.js"></script>
      <div class="slackhead" style="z-index:5">
         Recently on the
         <img src="img/slack.png" height="20"
                  style="vertical-align:middle">hackerspace channel...</div>
    </div>

  </div>

  <div style="width:35%;z-index:1;position:absolute;bottom:0;right:0"
      id="slack-chat"></div>


    <div style="float: left; width: 60%">

    <h1>Welcome to Hack Manhattan!</h1>
    <div id="event-schedule"></div>

    </div>

    <center>
    <div style="float: left; width:60%;">
    <em style="font-size: 120%;">Dashboard under construction.
                                Expect components and layout to change.</em>
    </center>

    </div>

</body>
</html>
