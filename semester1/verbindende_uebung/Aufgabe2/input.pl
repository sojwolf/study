#!/usr/local/bin/perl -w
use strict;
print "Name : ";
my $name = <STDIN>;
chomp($name);
printf("Hallo, %s !\n",$name);