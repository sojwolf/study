#!/usr/bin/perl

use strict;
#use warnings;
#use diagnostics;

# @see Beispiel Vorlesung
my $sequenz1 = "CGCUA";
my $sequenz2 = "CGCGCUGU";

# @see https://de.wikipedia.org/wiki/Smith-Waterman-Algorithmus (match=2)
#my $sequenz1 = "TCCG";
#my $sequenz2 = "ACGA";

# @see https://en.wikipedia.org/wiki/Smith%E2%80%93Waterman_algorithm (match=2)
#my $sequenz1 = "AGCACACA";
#my $sequenz2 = "ACACACTA";

# Alignmentmatrix
my @A;

# Hilfsmatrix für Backtracking
my @B;

my @sequenz1 = split( //, $sequenz1 );
my @sequenz2 = split( //, $sequenz2 );

my $gap      = -1;
my $match    = 1;
my $mismatch = -1;

my %max_value = ("value" => 0, "row" => 0, "column" => 0);

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
		$A[1][ $i + 1 ] = 0;
	}

	for ( my $i = 1 ; $i <= length($sequenz1) ; $i++ ) {
		$A[ $i + 1 ][1] = 0;
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
		$B[1][ $i + 1 ] = 0;
	}

	for ( my $i = 1 ; $i <= length($sequenz1) ; $i++ ) {
		$B[ $i + 1 ][1] = 0;
	}
}

# Matrix füllen
sub setValues {
	
	my $result = 0;
	
	for ( my $row = 2 ; $row < length($sequenz1) + 2 ; $row++ ) {
		my $s1_char = $sequenz1[ $row - 2 ];
		for ( my $column = 2 ; $column < length($sequenz2) + 2 ; $column++ ) {
			my $s2_char = $sequenz2[ $column - 2 ];

			if ( $s1_char eq $s2_char ) {
				$result = $A[ $row - 1 ][ $column - 1 ] + $match;
				$A[$row][$column] = ($result > 0) ? $result : 0;
				$B[$row][$column] = "lu";
			} else {
				$result = $A[ $row - 1 ][ $column - 1 ] + $mismatch;
				$A[$row][$column] = ($result > 0) ? $result : 0;
				$B[$row][$column] = "lu";
			}

			if ( $A[ $row - 1 ][$column] + $gap > $A[$row][$column] ) {
				$result = $A[ $row - 1 ][$column] + $gap;
				$A[$row][$column] = ($result > 0) ? $result : 0;
				$B[$row][$column] = "u";
			}

			if ( $A[$row][ $column - 1 ] + $gap > $A[$row][$column] ) {
				$result = $A[$row][ $column - 1 ] + $gap;
				$A[$row][$column] = ($result > 0) ? $result : 0;
				$B[$row][$column] = "l";
			}
			
			# Daten zum Maximum speichern
			if ($max_value{"value"} < $result) {
				$max_value{"value"} = $result;
				$max_value{"row"} = $row;
				$max_value{"column"} = $column;
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
	
	print("MAX: Wert: " . $max_value{"value"} . ", Zeile: " . $max_value{"row"} . ", Spalte: ". $max_value{"column"} . "\n\n");
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
	my $row_count     = $max_value{"row"};
	my $column_count  = $max_value{"column"};
	my $current_score = $A[$row_count][$column_count];

	while ( $current_score > 0 && ($row_count >= 2 || $column_count >= 2) ) {
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
		
		$current_score = $A[$row_count][$column_count];
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