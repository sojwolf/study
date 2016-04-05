#! /usr/bin/perl

use warnings;
use strict;
use LWP;
my $ua = LWP::UserAgent->new;

my $filename=$ARGV[0];

open INPUT, "<IEP_".$filename."_fastacut.txt";
my @input=<INPUT>;
chomp @input;
close INPUT;

my $name;
unlink $filename."_canadierseite.txt";
open OUTPUT, ">".$filename."_canadierseite.txt";
foreach (@input) {
	
	if ($_ =~ /\>/) {
		$name=$_;
	} else {

		my $response = $ua->post( "http://webapps2.ucalgary.ca/~groupii/cgi-bin/primes.cgi", ['sequence'=>$_] );
		
		print $name."\n";
		print OUTPUT $name."\n";
		print ($response->content);
		print OUTPUT ($response->content);

	}
}
close OUTPUT;
