<?php
// Modified: https://github.com/simonwalz/php-mjpeg-proxy

/* MIT License

Copyright (c) 2017 Simon Walz

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE. */

/*
 Multiple feeds, snapshot, and live pid functionality added by Beads Land-Trujillo
 at Hack Manhattan, 2018
 */

 // NOTE: www-data needs to be in a group with write access to pid/
 if ( (!isset($_GET["view"])) or $_GET["view"] == "space" ) {
   $pid = exec("/opt/defaultcast/jobs/sous/live.sh > /dev/null 2>&1 & echo $!;");
   function shutdown($pid) { exec("kill -9 " . $pid); }
   register_shutdown_function('shutdown', $pid);
 }


// config:

/*
$mjpg = array(
          'space' => "http://192.168.42.22:8080/",
          'door2' => "http://192.168.42.21:8080/",
          'cr10' => "http://192.168.42.19:8080/",
          'hydro' => "http://192.168.42.18:8081/"
        );
*/
$mjpg = array(
          'space' => "http://wrtnode-webcam.lan:8080/",
          'door' => "http://rfid-access-building.lan:8080/",
          'cr10' => "http://octoprint-main.lan:8080/",
          'hydro' => "http://hydrocontroller.lan:8081/",
          'bind' => "http://bricolage.hackmanhattan.com:2020/test/stream"
        );

if ( !isset($_GET["view"]) ) {
  $mjpeg_url = $mjpg["space"];
} else {
  $mjpeg_url = $mjpg[$_GET["view"]];
};

if ( !isset($_GET["action"]) ) {
  do_stream($mjpeg_url);
} elseif ( $_GET["action"] == "stream" ) {
  do_stream($mjpeg_url);
} elseif ( $_GET["action"] == "snapshot" ) {
  do_snap($mjpeg_url);
}

function do_snap($url) { // https://gist.github.com/nicoptere/a23ffae9ed51a5ca9766
  $url .= "?action=snapshot";
  $imginfo = getimagesize( $url );
  header("Content-type: ".$imginfo['mime']);
  readfile( $url );
}

function do_stream($mjpeg_url) {
  $mjpeg_url .=  "?action=stream";
  // preparing http options:
  $opts = array(
  	'http'=>array(
  		'method'=>"GET",
  		'header'=>"Accept-language: en\r\n" .
  		"Cookie: foo=bar\r\n"
  	  )
  );
  $context = stream_context_create($opts);
  // set no time limit and disable compression:
  set_time_limit(0);
//  @apache_setenv('no-gzip', 1);
  @ini_set('zlib.output_compression', 0);
  /* Sends an http request
   *    with additional headers shown above */
  $fp = fopen($mjpeg_url, 'r', false, $context);
  if ($fp) {
  	// send mjpeg header:
  	header("Cache-Control: no-cache");
  	header("Cache-Control: private");
  	header("Pragma: no-cache");
  	header("Content-type: multipart/x-mixed-replace; boundary=boundarydonotcross");
  	// pass data
  	fpassthru($fp);
  	fclose($fp);
  } else {
  	// error: webcam probably offline
  	// send alternative picture:
  	$d = file_get_contents("../img/ceilingcat.jpg");
  	Header("Content-Type: image/jpeg");
  	Header("Content-Length: ".strlen($d));
  	header("Cache-Control: no-cache");
  	header("Cache-Control: private");
  	header("Pragma: no-cache");
  	echo $d;
  }
}
