#!/usr/bin/perl

use strict;
#use warnings;
#use diagnostics;

#my $sequenz1 = "GCATGCT";
#my $sequenz2 = "GATTACA";

#my $sequenz1 ="ACGTC";
#my $sequenz2 = "AGTC";

# @see: http://www.avatar.se/molbioinfo2001/dynprog/dynamic.html
my $sequenz1 = "JAETHE";
my $sequenz2 = "AEHREN";

# Alignmentmatrix
my @A;

# Hilfsmatrix für Backtracking
my @B;

my @sequenz1 = split( //, $sequenz1 );
my @sequenz2 = split( //, $sequenz2 );
my $gap      = -1;
my $match    = 3;
my $mismatch = 0;

# Beschriftung für A
sub setHeadersA {

	# erste Zeile (Sequenz2)
	for ( my $i = 0 ; $i <= ( length($sequenz2) - 1 ) ; $i++ ) {
		if ( $i == 0 ) { }
		elsif ( $i == 1 ) {
			$A[0][$i] = "_";
		}
		$A[0][ $i + 2 ] = $sequenz2[$i];
	}

	# erste Spalte (Sequenz1)
	for ( my $i = 0 ; $i <= ( length($sequenz1) - 1 ) ; $i++ ) {
		if ( $i == 0 ) { }
		elsif ( $i == 1 ) {
			$A[$i][0] = "_";
		}

		$A[ $i + 2 ][0] = $sequenz1[$i];
	}
}

# Initialisierung für A
sub initA {

	# erste Zeile
	for ( my $i = 0 ; $i <= length($sequenz2) ; $i++ ) {
		$A[1][ $i + 1 ] = $i * $gap;
	}

	for ( my $i = 1 ; $i <= length($sequenz1) ; $i++ ) {
		$A[ $i + 1 ][1] = $i * $gap;
	}
}

# Beschriftung für B
sub setHeadersB {

	# erste Zeile (Sequenz2)
	for ( my $i = 0 ; $i <= ( length($sequenz2) - 1 ) ; $i++ ) {
		if ( $i == 0 ) { }
		elsif ( $i == 1 ) {
			$B[0][$i] = "_";
		}
		$B[0][ $i + 2 ] = $sequenz2[$i];
	}

	# erste Spalte (Sequenz1)
	for ( my $i = 0 ; $i <= ( length($sequenz1) - 1 ) ; $i++ ) {
		if ( $i == 0 ) { }
		elsif ( $i == 1 ) {
			$B[$i][0] = "_";
		}
		$B[ $i + 2 ][0] = $sequenz1[$i];
	}
}

# Initialisierung für B
sub initB {

	# erste Zeile
	for ( my $i = 0 ; $i <= length($sequenz2) ; $i++ ) {
		$B[1][ $i + 1 ] = $i * $gap;
	}

	for ( my $i = 1 ; $i <= length($sequenz1) ; $i++ ) {
		$B[ $i + 1 ][1] = $i * $gap;
	}
}

# Matrix füllen
sub setValues {
	for ( my $row = 2 ; $row < length($sequenz1) + 2 ; $row++ ) {
		my $s1_char = $sequenz1[ $row - 2 ];
		for ( my $column = 2 ; $column < length($sequenz2) + 2 ; $column++ ) {
			my $s2_char = $sequenz2[ $column - 2 ];

			if ( $s1_char eq $s2_char ) {
				$A[$row][$column] = $A[ $row - 1 ][ $column - 1 ] + $match;
				$B[$row][$column] = "lu";
			}
			else {
				$A[$row][$column] = $A[ $row - 1 ][ $column - 1 ] + $mismatch;
				$B[$row][$column] = "lu";
			}

			if ( $A[ $row - 1 ][$column] + $gap > $A[$row][$column] ) {
				$A[$row][$column] = $A[ $row - 1 ][$column] + $gap;
				$B[$row][$column] = "u";
			}

			if ( $A[$row][ $column - 1 ] + $gap > $A[$row][$column] ) {
				$A[$row][$column] = $A[$row][ $column - 1 ] + $gap;
				$B[$row][$column] = "l";
			}
		}
	}
}

sub outputA {
	print("A:\n");
	for ( my $row = 0 ; $row <= $#A ; $row++ ) {
		for ( my $column = 0 ; $column < length( $A[$row] ) ; $column++ ) {
			print "\t". $A[$row][$column];
		}
		print "\n";
	}

	print "\n";
	print "\n";
}

sub outputB {
	print("B:\n");
	for ( my $row = 0 ; $row <= $#B ; $row++ ) {
		for ( my $column = 0 ; $column < length( $B[$row] ) ; $column++ ) {
			print "\t$B[$row][$column]";
		}
		print "\n";
	}

	print "\n";
	print "\n";
}

# Backtracking ausführen und Ergebnisse speichern/ausgeben
sub displayBacktrackingResult {

	my $seq_a = "";
	my $seq_b = "";

	my $current_value = 0;
	my $row_count     = $#B;
	my $column_count  = ( scalar( keys $B[1] ) ) - 1;

	while ( $row_count >= 2 || $column_count >= 2 ) {
		$current_value = $B[$row_count][$column_count];

		if ( $current_value eq "lu" ) {
			$seq_a = $B[$row_count][0] . $seq_a;
			$seq_b = $B[0][$column_count] . $seq_b;
			$row_count--;
			$column_count--;
		}
		elsif ( $current_value eq "u" ) {
			$seq_a = $B[$row_count][0] . $seq_a;
			$seq_b = "_" . $seq_b;
			$row_count--;
		}
		else {
			$seq_b = $B[0][$column_count] . $seq_b;
			$seq_a = "_" . $seq_a;
			$column_count--;
		}
	}

	print( "Sequenz 1: " . $seq_a );
	print "\n";
	print( "Sequenz 2: " . $seq_b );
	print "\n";
	print "\n";
}

setHeadersA();
setHeadersB();
initA();
initB();
setValues();
outputA();
outputB();
displayBacktrackingResult();
