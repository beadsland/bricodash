<?php

/*
####
## Copyright © 2018 Beads Land-Trujillo.
##
## This program is free software: you can redistribute it and/or modify
## it under the terms of the GNU Affero General Public License as published
## by the Free Software Foundation, either version 3 of the License, or
## (at your option) any later version.
##
## This program is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU Affero General Public License for more details.
##
## You should have received a copy of the GNU Affero General Public License
## along with this program.  If not, see <https://www.gnu.org/licenses/>.
####
*/

  if ($_SERVER['QUERY_STRING'] == "widgetImages/mta_widget_logo.png") {
    header('Pragma: public');
    header('Cache-Control: max-age=86400');
    header("Content-Type: image/png");
    header("Content-Length: " . filesize("logo.png"));
    fpassthru(fopen("logo.png", 'r'));
  } else {
    $path = "http://service.mta.info/ServiceStatus/" . $_SERVER['QUERY_STRING'];
    $temp = tmpfile();
    $metaDatas = stream_get_meta_data($temp);
    $tmpFilename = $metaDatas['uri'];
    file_put_contents($tmpFilename, fopen($path, 'r'));

    exec("convert " . $tmpFilename . " -fuzz 40% -fill '#101010' -floodfill +0+0 white " . $tmpFilename);

    header('Pragma: public');
    header('Cache-Control: max-age=86400');
    header("Content-Type: image/gif");
    header("Content-Length: " . filesize($tmpFilename));
    fpassthru($temp);
  }
  exit;
?>
