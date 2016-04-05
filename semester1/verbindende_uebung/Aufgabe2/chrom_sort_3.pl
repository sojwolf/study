my @chrom_data = ('A','B', 'C1', 'a','Beta', 'C2', 'A','B', 'C2', 'Alpha','b', 'C2');

my @_result_1 = ();
my @_result_2 = ();

sub merge_chromosoms {
	my @data = @_;
	my @result = ();
	for (my $i=0; $i <= 5; $i += 3) {
		for (my $j=1; $j <= 5; $j += 3) {
			for (my $k=2; $k <= 5; $k += 3) {
				push(@result, $data[$i] . "," . $data[$j] . "," . $data[$k]);
			}
		}
	}
	
	return @result;
}

@_result_1 = merge_chromosoms(@chrom_data[0,1,2,3,4,5]);
@_result_2 = merge_chromosoms(@chrom_data[6,7,8,9,10,11]);
print(join(";", @_result_1) . "\n");
print(join(";", @_result_2) . "\n");