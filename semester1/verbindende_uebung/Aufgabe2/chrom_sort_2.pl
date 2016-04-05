my @chrom_data = ('A,B', 'C1', 'a,Beta', 'C2', 'A,B', 'C2', 'Alpha,b', 'C2');

my @_result_1 = ();
my @_result_2 = ();

sub merge_chromosoms {
	my @data = @_;
	my @result = ();
	for (my $i=0; $i <= 3; $i += 2) {
		for (my $j=1; $j <= 3; $j += 2) {
			push(@result, $data[$i] . "," . $data[$j]);
		}
	}
	
	return @result;
}

@_result_1 = merge_chromosoms(@chrom_data[0,1,2,3]);
@_result_2 = merge_chromosoms(@chrom_data[4,5,6,7]);
print(join(";", @_result_1) . "\n");
print(join(";", @_result_2) . "\n");