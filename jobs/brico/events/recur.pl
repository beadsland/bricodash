#!/usr/bin/env perl

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

require Date::Manip;

$str = $ARGV[0];
$str =~ s/Thurs?/Thur/;

$m = new Date::Manip::Date();
$m->parse($str);
if ($m->value < Date::Manip::Date->new("today")->value) {
  my ($sec,$min,$hour,$mday,$mon,$year,$wday,$yday,$isdst) = localtime(time);
  $year =1900 + $year + 1;
  $m->parse("$str $year");
}
if ((not $m->value) || $m->value < Date::Manip::Date->new("today")->value) {
  $m = recur($str);
}

print $m->printf("%Y/%m/%d %H:%M:%S");

sub recur(str) {
  $r = new Date::Manip::Recur;

  ($rec, $mod) = split(/\+/, $str);
  $mod =~ s/^\s+|\s+$//g;
  $mod = "FD0" unless $mod;

  $err = $r->parse( $rec, "$mod", "", "today", "2 years from now" );
  return ( $r->dates() )[0];
}
