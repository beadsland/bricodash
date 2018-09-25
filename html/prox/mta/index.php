<?php
  if ($_SERVER['QUERY_STRING'] == "widgetImages/mta_widget_logo.png") {
    header("Content-Type: image/png");
    header("Content-Length: " . filesize("logo.png"));
    fpassthru(fopen("logo.png", 'r'));
  } else {
    $path = "http://service.mta.info/ServiceStatus/" . $_SERVER['QUERY_STRING'];
    $temp = tmpfile();
    $metaDatas = stream_get_meta_data($temp);
    $tmpFilename = $metaDatas['uri'];
    file_put_contents($tmpFilename, fopen($path, 'r'));

    exec("convert " . $tmpFilename . " -fuzz 40% -fill black -floodfill +0+0 white " . $tmpFilename);

    header("Content-Type: image/gif");
    header("Content-Length: " . filesize($tmpFilename));
    fpassthru($temp);
  }
  exit;
?>

<!--
?>

-->
