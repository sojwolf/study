#!/usr/bin/perl

use strict;

# @see metacpan.org/pod/Class::CSV
#use Class::CSV;

my @zeile1 = ("1", "Test", "3");
my @zeile2 = ("2", "Test1", "6");
my @zeile3 = ("3", "Test2", "9");
my @zeile4 = ("4", "Test3", "12");

our @data = (\@zeile1,\@zeile3,\@zeile3,\@zeile4);

# oder durch ein anonymes Array
our @data2 = (
	["1", "Test0", "3"],
	["2", "Test1", "6"],
	["3", "Test2", "9"],
	["4", "Test3", "8"]
);

for (my $i = 0; $i <= $#data2; $i++) {
	for (my $j = 0; $j < length($data2[$i]); $j++) {
		print($data[$i][$j]);
	}
	print("\n");
}

sub writeFile {
	my $seperator = ",";
	# dynamischen Pfad?
	my $file_path = "/home/alexander/demo.csv";
	open(FILE, "> " . $file_path) or die "Fehler beim Öffnen der Datei: $!\n";

	for (my $row = 0; $row <= $#data; $row++) {
		my @line_data = ();
		for (my $column = 0; $column <= 3; $column++) {
			push(@line_data, $data[$row][$column]);
		}
		print FILE join($seperator, @line_data) . "\n\l";
	}

	close(FILE);
}

#writeFile();