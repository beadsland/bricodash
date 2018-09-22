#!/usr/bin/env perl

require Date::Manip;

$str = $ARGV[0];
$str =~ s/Thurs?/Thur/;

$m = new Date::Manip::Date();
$m->parse($str);
if ($m->value < Date::Manip::Date->new("today")->value) {
  $m = $m->calc(Date::Manip::Delta->new("1 year"));
}
$m = recur(str) unless $m->value;

print $m->printf("%Y/%m/%d %H:%M:%S");

# print recur(str)->printf("%Y/%m/%d %H:%M:%S");


sub recur(str) {
  $r = new Date::Manip::Recur;

  ($rec, $mod) = split(/\+/, $str);
  $mod =~ s/^\s+|\s+$//g;

  $r->parse( $rec );
  $r->modifiers( $mod ) if $mod;
  $r->start("today");
  $r->end("next year");

  return ( $r->dates() )[0];
}
