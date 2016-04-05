from time import *
from resource import *
from os.path import expanduser

home = expanduser('~')

individuum = 'Danaus_plexippus'
cds_filename = '/Danaus_plexippus.DanPle_1.0.29.cds.all.fa'
pep_filename = '/Danaus_plexippus.DanPle_1.0.29.pep.all.fa'

#individuum = 'Dictyostelium_discoideum'
#cds_filename = '/Dictyostelium_discoideum.dictybase.01.29.cds.all.fa'
#pep_filename = '/Dictyostelium_discoideum.dictybase.01.29.pep.all.fa'

file_basename = home + ('/ownCloud/Studium/Extra/VerbindUe_Aufgabe6/%s' % (individuum))

output_path = file_basename
#print(output_path)
codons = {}
aminos = {}
amino_codons = {}
stop_codons = []

codon_list = []
amino_list = []

def fetchCdsData():
	global cds_gene_count
	cds_gene_count = 0
	cds_file = open(file_basename + cds_filename, 'r')
	i = -1
	gene_header = ''
	for line in cds_file:
		if str.find(line, ">") != -1:
			gene_header = line
			cds_gene_count += 1
			i += 1
			continue
		n_line = line.strip()
		
		if (len(n_line) % 3) != 0:
			print(gene_header)
		
		while n_line:
			codon = n_line[:3]
			
			if len(codon) != 3:
				print(codon)
				break
			
			if (i+1) == len(codon_list):
				codon_list[i].append(codon)
			else:
				codon_list.append([])
				codon_list[i].append(codon)
			
			if codon in codons:
				codons[codon] += 1;
			else:
				codons[codon] = 1;
			n_line = n_line[3:]

def writeCdsFile():
	new_filename = cds_filename.split('.')
	file = open(output_path + '/%s_%s.csv' % (new_filename[0], new_filename[4]), 'w')
	seperator = ';'
	
	# Kopfzeile schreiben
	head_row = ['Codon', 'abs. Häufigkeit', 'rel. Häufigkeit [%]' + "\n"]
	file.write(seperator.join(head_row))
	
	codon_sum = sum(codons.values())
	
	# Sortierung für die Ausgabe
	for key in sorted(codons.keys()):
		rel_frequency = (codons[key]/codon_sum)*100
		output = [key, str(codons[key]), str('% .6f' % rel_frequency)]
		file.write(seperator.join(output) + "\n")

def fetchPepData():
	global pep_gene_count
	pep_gene_count = 0
	pep_file = open(file_basename + pep_filename, 'r')
	i = -1
	for line in pep_file:
		if str.find(line, ">") != -1:
			pep_gene_count += 1
			i += 1
			continue
		n_line = line.strip()
		
		while n_line:
			amino = n_line[:1]
			
			if (i+1) == len(amino_list):
				amino_list[i].append(amino)
			else:
				amino_list.append([])
				amino_list[i].append(amino)
			
			if amino in aminos:
				aminos[amino] += 1;
			else:
				aminos[amino] = 1;
			n_line = n_line[1:]

def writePepData():
	new_filename = pep_filename.split('.')
	file = open(output_path + '/%s_%s.csv' % (new_filename[0], new_filename[4]), 'w')
	seperator = ';'
	
	# Kopfzeile schreiben
	head_row = ['Aminosäure', 'abs. Häufigkeit', 'rel. Häufigkeit [%]' + "\n"]
	file.write(seperator.join(head_row))
	
	amino_sum = sum(aminos.values())
	
	# Sortierung bei der Ausgabe
	for key in sorted(aminos.keys()):
		rel_frequency = (aminos[key]/amino_sum)*100
		output = [key, str(aminos[key]), str('% .6f' % rel_frequency)]
		file.write(seperator.join(output) + "\n")

def createMappingTable():
	global stop_codons

	for i in range(len(codon_list)):
		last_codon = codon_list[i].pop()
		if last_codon not in stop_codons:
			stop_codons.append(last_codon)
		
		for j in range(len(codon_list[i])):
			amino_acid = amino_list[i][j]
			current_codon = codon_list[i][j]
			if amino_acid not in amino_codons:
				amino_codons[amino_acid] = []
				amino_codons[amino_acid].append(current_codon)
			else:
				if current_codon not in amino_codons[amino_acid]:
					amino_codons[amino_acid].append(current_codon)

def writeMappingTable():
	new_filename = 'amino_codon_mapping'
	file = open(output_path + '/%s.csv' % (new_filename), 'w')
	seperator = ';'
	
	# Kopfzeile schreiben
	head_row = ['Aminosäure', 'Codonkombinationen', "\n"]
	file.write(seperator.join(head_row))
	
	# Sortierung bei der Ausgabe
	for key in sorted(amino_codons.keys()):
		file.write(seperator.join([key, ', '.join(amino_codons[key])]) + "\n")
	
	# Stopcodons anhängen
	file.write(seperator.join(['Stopcodons', ', '.join(stop_codons)]))

def prepare():
	print(codons)
	print(aminos)

fetchCdsData()
writeCdsFile()
fetchPepData()
writePepData()
createMappingTable()
writeMappingTable()
#prepare()

print("Anzahl Gene: " + str(pep_gene_count))

# Ausgabe Laufzeit und Speicherverbrauch
print('Laufzeit [s]: ' + str(clock()))
ru = getrusage(RUSAGE_SELF).ru_maxrss / 1024
print('Speicherverbrauch [kb]: ' + str('% .3f' % ru))