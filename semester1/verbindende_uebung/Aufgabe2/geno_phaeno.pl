#!/usr/bin/perl

use strict;
#use warnings;
#use diagnostics;

# Konfiguration des Genotyp-Phaenotyp-Mappping
# Form
my %form = (
	"A" => {"valence" => "3","value" => "Raute"},
	"a" => {"valence" => "2","value" => "Balken"},
	"alpha" => {"valence" => "1","value" => "Welle"},
);

# Farbe
my %color = (
	"B" => {"valence" => "3","value" => "rot"},
	"b" => {"valence" => "2","value" => "grün"},
	"beta" => {"valence" => "1","value" => "violett"},
);

# Füllung
my %filling = (
	"C1" => {"valence" => "3","value" => "leer"},
	"C2" => {"valence" => "2","value" => "voll"},
	"C1C2" => {"valence" => "1","value" => "halb"},
	"C2C1" => {"valence" => "0","value" => "halb"},
);

# Ergebnismatrizen
our @result;
our %phaenotype_result;

# Anzahl der Chromosomen, wird vom Script gesetzt
# durch Formalismus bei der Angabe der Chromatide als Abfrage überflüssig
our $chromosomen_count = 0;

# Arbeitsvariablen
our @merged_genotype_data;

# Array mit aufbereiteten Daten
our @prepared_data = ();

# letzte Fehlermeldung
our $error_message = "";

# Inputdata Abfragen und speichern
sub fetchInputData {
	print("Beispiele für die Angabe der Chromatide\n");
	print("Chromosomenanzahl=1: (A,B,C2)\n");
	print("Chromosomenanzahl=2: (A,B);(C2)\n");
	print("Chromosomenanzahl=3: (A);(B);(C2)\n\n");
	
	for (my $i = 1; $i < 3; $i++) {
		for (my $c = 1; $c < 3; $c++) {
			my $p = 1;
			do {
				if ($error_message ne "") {
					print($error_message);
				}
				print("Individuum " . $i . ", Chromatid " . $c . ":");
				my $tmp = <STDIN>;
				$p = splitInput($tmp);
			} while($p == 0);
			
			$error_message = "";
		}
		$error_message = "";
	}
}

# Inputdata auftrennen
sub splitInput {
	
	# übergebenen Input holen
	my $input = $_[0];
	
	# Chromosomen trennen und Anzahl prüfen
	my $current_count = 0;
	my @test = split(/\);\(/, $input);
	if ($chromosomen_count == 0) {
		$chromosomen_count = scalar (keys @test);
		$current_count = $chromosomen_count;
	} else {
		$current_count = scalar (keys @test);
	}
	
	if ($chromosomen_count != $current_count) {
		$error_message = "Fehler: Falsche Anzahl der Chromosomen. Angegeben: " . $current_count . ", Benötigt: " . $chromosomen_count . "\n";
		return 0;
	}

	# Genotypen trennen
	my @genotypes = ();
	
	if ($chromosomen_count == 1) {
		# ^\((\w{1,5}),(\w{1,5}),(\w{1,5})\)$ für (A,beta,C2)
		@genotypes = ($input =~ m/^\((\w{1,5},\w{1,5},\w{1,5})\)$/g);
	} elsif ($chromosomen_count == 2) {
		# ^\((\w{1,5}),(\w{1,5})\);\((\w{1,5})\)$ für (A,b);(C1)
		# oder mit ^\((\w{1,5});(\w{1,5})\),\((\w{1,5})\)$ für (A);(b,C1)
		@genotypes = ($input =~ m/^\((\w{1,5},\w{1,5})\);\((\w{1,5})\)$/g);
	} elsif ($chromosomen_count == 3) {
		# ^\((\w{1,5})\),\((\w{1,5})\),\((\w{1,5})\)$ für (alpha),(B),(C2)
		@genotypes = ($input =~ m/^\((\w{1,5})\);\((\w{1,5})\);\((\w{1,5})\)$/g);
	} else {
		$error_message = "Fehler bei der Trennung der Genotypen: " . chomp($input) . ". (Falsches Format?)\n";
		return 0;
	}

	push(@merged_genotype_data, @genotypes);
	return 1;
}

# Mischung der Allele für zwei Chromosomen
sub merge_chromosomes_2 {
	my @data = @_;
	my @res = ();
	for (my $i=0; $i <= 3; $i += 2) {
		for (my $j=1; $j <= 3; $j += 2) {
			push(@res, $data[$i] . "," . $data[$j]);
		}
	}
	
	return @res;
}

# Mischung der Allele für drei Chromosomen
sub merge_chromosomes_3 {
	my @data = @_;
	my @res = ();
	for (my $i=0; $i <= 5; $i += 3) {
		for (my $j=1; $j <= 5; $j += 3) {
			for (my $k=2; $k <= 5; $k += 3) {
				push(@res, $data[$i] . "," . $data[$j] . "," . $data[$k]);
			}
		}
	}
	
	return @res;
}

# Aufbereitung der Inputdata
sub prepareData {

	if ($chromosomen_count == 1) {
		$prepared_data[0][0] = $merged_genotype_data[0];
		$prepared_data[0][1] = $merged_genotype_data[1];
		$prepared_data[1][0] = $merged_genotype_data[2];
		$prepared_data[1][1] = $merged_genotype_data[3];
	} elsif ($chromosomen_count == 2) {
		# Paarungen erzeugen
		my @test1 = merge_chromosomes_2(@merged_genotype_data[0,1,2,3]);
		my @test2 = merge_chromosomes_2(@merged_genotype_data[4,5,6,7]);
		
		# Paarungen zuordnen
		for (my $i = 0; $i <= ($#test1); $i++) {
			$prepared_data[0][$i] = $test1[$i];
			$prepared_data[1][$i] = $test2[$i];
		}
	} elsif ($chromosomen_count == 3) {
		# Paarungen erzeugen
		my @test1 = merge_chromosomes_3(@merged_genotype_data[0,1,2,3,4,5]);
		my @test2 = merge_chromosomes_3(@merged_genotype_data[6,7,8,9,10,11]);
		
		# Paarungen zuordnen
		for (my $i = 0; $i <= ($#test1); $i++) {
			$prepared_data[0][$i] = $test1[$i];
			$prepared_data[1][$i] = $test2[$i];
		}
	}
}

# Erzeugen der Kopfzeilen der Tabelle
sub createTableHeader {

	# erste Zeile: Individuum1
	for (my $j = 0; $j <= (scalar (keys $prepared_data[0]))-1; $j++) {
		$result[0][$j+1] = $prepared_data[0][$j];
	}
	
	# erste Spalte: Indivduum2
	for (my $j = 0; $j <= (scalar (keys $prepared_data[1]))-1; $j++) {
		$result[$j+1][0] = $prepared_data[1][$j];
	}
}

# Zusammenstellen eines Genotyps
sub prepareGenotyp {
	my ($x, $y) = @_;
	my $result = "";
	my @genotyp1 = split(",", $x);
	my @genotyp2 = split(",", $y);

	if ($form{$genotyp1[0]}{"valence"} > $form{$genotyp2[0]}{"valence"}) {
		$result .= $genotyp1[0] . "/" . $genotyp2[0] . " ";
	} else {
		$result .= $genotyp2[0] . "/" . $genotyp1[0] . " ";
	}
	
	if ($color{$genotyp1[1]}{"valence"} > $color{$genotyp2[1]}{"valence"}) {
		$result .= $genotyp1[1] . "/" . $genotyp2[1] . " ";
	} else {
		$result .= $genotyp2[1] . "/" . $genotyp1[1] . " ";
	}
	
	if ($filling{$genotyp1[2]}{"valence"} > $filling{$genotyp2[2]}{"valence"}) {
		$result .= $genotyp1[2] . "/" . $genotyp2[2];
	} else {
		$result .= $genotyp2[2] . "/" . $genotyp1[2];
	}

	return $result;
}

# Phaenotyp anhand des Genotyps erzeugen
sub setPhaenotype {
	my $genotypes = $_[0];
	my @dom_genotypes = ($genotypes =~ m/^(\w)\/\w{1,5}\s(\w)\/\w{1,5}\s(\w{2})\/(\w{2})$/g);
	
	my $form1 = $form{$dom_genotypes[0]}{"value"}; # Form
	my $color1 = $color{$dom_genotypes[1]}{"value"}; # Farbe
	
	# Füllung
	my $filling1 = ($dom_genotypes[2] eq $dom_genotypes[3])
				 ? $filling{$dom_genotypes[2]}{"value"}
				 : $filling{$dom_genotypes[2].$dom_genotypes[3]}{"value"};
	
	my $phaenotype = $form1 . " " . $color1 . " " . $filling1;
	if (!defined($phaenotype_result{$phaenotype})) {
		$phaenotype_result{$phaenotype} = 1;
	} else {
		$phaenotype_result{$phaenotype}++;
	}
}

# Tabellenelemente erzeugen
sub createTableValues {
	my $column_count = (scalar(keys $result[0] )-1);
	for ( my $row = 1 ; $row <= $#result ; $row++ ) {
		for ( my $column = 1 ; $column <= $column_count; $column++ ) {
			my $genotype = prepareGenotyp($result[0][$column], $result[$row][0]);
			$result[$row][$column] = $genotype;
			setPhaenotype($genotype);
		}
	}
}

# Ausgabe der Tabelle auf der Konsole
sub output {
	print("Matrix:\n");
	for ( my $row = 0 ; $row <= $#result ; $row++ ) {
		for ( my $column = 0 ; $column < length( $result[$row] ) ; $column++ ) {
			print $result[$row][$column] . "\t";
		}
		print "\n";
	}
}

# vollständige Ausgabe (Tabelle + Häufigkeiten) als CSV-Datei
sub writeOutputFile {
	my $seperator = ";";

	my $file_path = $ENV{"HOME"} . "/demo.csv";
	open(FILE, "> " . $file_path) or die "Fehler beim Öffnen der Datei: $!\n";

	# Genotyp-Tabelle
	for (my $row = 0; $row <= $#result; $row++) {
		my @line_data = ();
		for (my $column = 0; $column <= length($result[$row]); $column++) {
			push(@line_data, $result[$row][$column]);
		}
		print FILE join($seperator, @line_data) . "\n\l";
	}
	
	print FILE "\n";
	
	# Phaenotyp-Tabelle
	print FILE join($seperator, keys %phaenotype_result) . "\n\l";
	print FILE join($seperator, values %phaenotype_result);
	
	close(FILE);
	
	print "Die Ergebnisse wurde in die Datei " . $file_path . " geschrieben.\n";
}

fetchInputData();
prepareData();
createTableHeader();
createTableValues();
#output();
writeOutputFile();