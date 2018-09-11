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

  <div style="width: 100%; z-index: 10; position:absolute; margin-bottom: 30px; top: 0; background-image: url('img/black1x1.png');">
    <div style="float: left; flex: 1; height: 400px;overflow: hidden;">
      <h1>Welcome to Hack Manhattan!</h1>           <!-- welcome -->
      <div id="event-schedule"></div> <!-- events -->


      <div class="slackhead" style="position: absolute; bottom: 0; margin: 0; z-index:5">
            Meanwhile, on the hackmanhattan.slack.com
           <img src="img/slack.png" height="20" style="vertical-align: middle">hackerspace channel...</div>
    </div>

    <div style="float: right; width: 448px;"> <!-- right column -->
      <div class="container">
        <!-- doorcam: 640 x 480 -->
        <img id="doorcam" width="448" height="336"
             src="http://hackmanhattan.duckdns.org:8888/hm/dash/util/camera.php?view=door">
        <div class="bottom-right" style="not-bottom:55">
          <span id="clock"></span>
        </div>

        <div class="top-right"><span id="weather"></span></div>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/jquery.simpleWeather/3.1.0/jquery.simpleWeather.min.js"></script>
        <script src="js/weather.js"></script>
      </div>

    </div>
  </div>

  <div style="position: absolute; bottom: 0; width: 100%;">



       <div style="word-wrap: break-word;"
             id="slack-chat"></div>
           </div>
</body>
</html>
