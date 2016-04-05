import glob
import os.path
import subprocess
import re

def blast():
	path = '/scr/genomes/Bacteria/Bacteria_NCBI/*/'
	file_pattern = '*.fna'
	target_path = '/u/home/praktikum/PRAK12/Blast-results/'
	intron_file = '/scratch/u/home/praktikum/PRAK12/new_sequenze_data1.txt'
	i = 0
	for filename in glob.glob(path + file_pattern):
		dir_name = os.path.basename(os.path.dirname(filename))
		new_file_path = target_path + 'blast_result.txt'
		content = '#FILE: ' + target_path + dir_name + '__' + os.path.basename(filename)
		command = "echo '%s' >> %s" % (content, new_file_path)
		subprocess.check_output(['bash','-c', command])
		
		command = "blastall -p blastn -m8 -e0.1 -d %s -i %s >> %s" % (filename, intron_file, new_file_path)

		try:
			subprocess.check_output(['bash','-c', command])
			print(dir_name)
		except Exception:
			print('Fehler')
		i+=1
		if i==4:
			break

#blast()

def countIntronLenght():
	results = {}
	intron_file = '/scratch/u/home/praktikum/PRAK12/data.csv'
	with open(intron_file) as f:
		for line in f:
			data = line.split(',')
			intron_lenght = int(data[3]) - int(data[2])
			new_data = data
			new_data.append(intron_lenght)
			results[data[0]] = new_data
	
	print(results)

#countIntronLenght()

def writeIntronPositionData(strand, filename):

	directory = '/scratch/u/home/praktikum/PRAK12/final/'
	target_file = directory + filename
	file_handle = open(target_file, 'a')
	
	for genome_titel, data in strand.iteritems():
		for subset in data:
			line = ','.join(map(str, subset))
			data_line = genome_titel + ',' + line + '\n'
			file_handle.write(data_line)
	
	file_handle.close()

def mappIntronOnGenome():
	
	intron_data = {}
	intron_summary = '/scratch/u/home/praktikum/PRAK12/data.csv'
	with open(intron_summary) as f:
		for line in f:
			data = line.split('\t')
			intron_data[data[0]] = data[7]
	
	blast_file = '/scratch/u/home/praktikum/PRAK12/Blast-results/complete_fin'
	pos_strand = {}
	neg_strand = {}
	
	with open(blast_file) as f:
		for line in f:
			if line[0]!='#':
				data = line.split('\t')
				intron_title = data[0]
				tmp_title = data[1].split('|')
				genome_title = tmp_title[3]
				q_start = data[6]
				q_end = data[7]
				s_start = data[8]
				s_end = data[9]
				
				if (int(s_end)-int(s_start)) > 0:
					#positivstrang
					g_start = int(s_start) - (int(q_start) +100)
					g_end = int(s_end) + (int(intron_data[intron_title]) - int(q_end)) + 100
					
					if g_start<0:
						g_start=0
					
					if g_end<0:
						g_end=0
					
					if genome_title not in pos_strand:
						pos_strand[genome_title] = []
						pos_strand[genome_title].append([g_start, g_end, intron_title])
					else:
						pos_strand[genome_title].append([g_start, g_end, intron_title])
				else:
					#negativstrang
					g_start = int(s_start) + (int(q_start) +100)
					g_end = int(s_end) - (int(intron_data[intron_title]) - int(q_end)) - 100
					
					if g_start<0:
						g_start=0
					
					if g_end<0:
						g_end=0
					
					if genome_title not in neg_strand:
						neg_strand[genome_title] = []
						neg_strand[genome_title].append([g_start, g_end, intron_title])
					else:
						neg_strand[genome_title].append([g_start, g_end, intron_title])
		
		#Daten vom Positivstrang in Datei schreiben
		writeIntronPositionData(pos_strand, 'pos_strand.csv')
		
		#Daten vom Negativstrang in Datei schreiben
		writeIntronPositionData(neg_strand, 'neg_strand.csv')

#mappIntronOnGenome()

def mergeStrandIntronData():
	intron_file = '/u/home/praktikum/PRAK12/tmp/pos_strand_sorted.csv'
	
	# Beispiel: {'Genome1' : [[start,ende][start,ende]...], 'Genome2' : [[]...]}
	result = {}
	
	with open(intron_file) as f:
		for line in f:
			data = line.split('\t')
			title = data[0]
			start = int(data[1])
			end = int(data[2])
			
			if title not in result:
				#Genomedaten mit erstem Datensatz initialisieren
				result[title] = []
				result[title].append([start, end])
			else:
				# Genomdaten erweitern mit aktuellem Datensatz erweitern, alle bisherigen Daten muessen verglichen werden
				existing_data = result[title]
				last_dataset = existing_data[-1]
				last_start = int(last_dataset[0])
				last_end = int(last_dataset[1])

				if (start >= last_start) and (end <= last_end):
					#Start und Ende bei beiden gleich
					#schon bestehendes behalten, neues Intron ueberspringen
					#print('schon bestehendes behalten, neues Intron ueberspringen')
					continue
				elif (start >= last_start and start < last_end) and (end > last_end):
					#ueberlappung
					#neues Ende berechnen und bestehenden Datensatz entsprechend bearbeiten
					#print('ueberlappung')
					# ueberlappung ergibt neue Grenzen, daher letztes Element entfernen
					result[title].pop()
					# und neues schreiben
					result[title].append([last_start, end])
					
				elif start > last_end:
					#Introns liegen komplett hintereinander
					#beide behalten
					#print('beide behalten')
					result[title].append([start, end])
				else:
					print('Fehler?')
					print(title, start, end)
	#print(result)
	writeIntronPositionData(result, 'pos_strand_sorted_merged_test.csv')

#mergeStrandIntronData()

def createGenomeLengthList():
	db_dir = '/scr/genomes/Bacteria/Bacteria_NCBI/*/'
	file_pattern = '*.fna'
	target_file = '/u/home/praktikum/PRAK12/tmp/genome_length.csv'
	file_handle = open(target_file, 'a')
	
	for filename in glob.glob(db_dir + file_pattern):
		
		command = 'fastalength %s' % (filename)
		try:
			result = subprocess.check_output(['bash', '-c', command])
			print(result)
			length = result.split(' ')[0]
			title = result.split(' ')[1].split('|')[3]
			file_handle.write(title + ',' + length + '\n')
		except Exception:
			print('Fehler')
	
	file_handle.close()

#createGenomeLengthList()

def fetchGenomeLength():
	filename = '/u/home/praktikum/PRAK12/tmp/genome_length.csv'
	result = {}
	with open(filename) as f:
		for line in f:
			data = line.split(',')
			title = data[0].split('.')[0]
			length = data[1].rstrip('\n')
			
			if title in result:
				print(line)
			else:
				result[title] = []
				result[title].append(length)
	
	return result

def fetchSequenzData():
	# command
	# fastacmd -d /scr/genomes/Bacteria/Bacteria_NCBI/Salinibacter_ruber_DSM_13855/NC_007677.fna -L 671851,673962 -s NC_007677
	
	merged_file = '/u/home/praktikum/PRAK12/tmp/testfile_joerg'
	db_dir = '/scr/genomes/Bacteria/Bacteria_NCBI/*/'
	target_file = '/u/home/praktikum/PRAK12/tmp/joerg_test'
	
	genome_length = fetchGenomeLength()
	
	i = 0
	with open(merged_file) as f:
		for line in f:
			line = line.rstrip('\n')
			data = line.split(',')
			file_name = data[0].split('.')[0] + '.fna'
			db_file_path = glob.glob(db_dir + file_name)[0]

			species = data[0].split('.')[0]
			max_length = genome_length[species][-1]
			start_pos = data[1]
			end_pos = data[2]
			if int(end_pos) > int(max_length):
				end_pos = max_length
				print('Test')
			seq_part = start_pos + ',' + end_pos
			
			command = "fastacmd -d %s -L %s -S2 -s %s >> %s" % (str(db_file_path), str(seq_part), str(species), str(target_file))

			try:
				subprocess.check_output(['bash','-c', command])
				print(command)
				print(i)
			except Exception:
				print('Fehler')
			i+=1
	
	f.close()

#fetchSequenzData()

def getPreparedSequenzData():
    sequ_data_file = '/home/alexander/Schreibtisch/tmp/sequ_data/merged'
    result = {}
    
    with open(sequ_data_file) as f:
        headline = ''
        data = ''
        for line in f:
            line = line.rstrip('\n')
            if line[0] == '>':
                title = line.split(' ')[0].split('|')[1]
                result[title] = {'headrow' : line, 'data' : ''}
                continue
            
            result[title]['data'] += line

    return result

def writeCandidateSequenzData():
    candidate_intron_file = '/home/alexander/Schreibtisch/tmp/sequ_data/intron_candidates.csv'
    
    target_file = '/home/alexander/Schreibtisch/tmp/sequ_data/candidates_sequenz_result'
    
    prepared_sequenz_data = getPreparedSequenzData()
    
    file_handle = open(target_file, 'w+')
    
    with open(candidate_intron_file) as f:
        for line in f:
            title = line.split(',')[0].split('|')[1]
            if title in prepared_sequenz_data:
                file_handle.write(prepared_sequenz_data[title]['headrow'] + '\n')
                file_handle.write(prepared_sequenz_data[title]['data'] + '\n')
                file_handle.write('\n')

    file_handle.close()

#writeCandidateSequenzData()

def createIndividuumListFile():
    result_list = []
	
	# Liste aus all_introns.txt
    intron_file = '/u/home/praktikum/PRAK12/final/all_introns.txt'
	
    with open(intron_file) as f:
		# Example-Line: >A.pt.I1/AF369871/2878..4803/Acinetobacter pittii/Bacterial C/Intron Sequence
        for line in f:
            if line[0] == '>':
                individuum = line.split('/')[3]
                individuum = individuum.replace(' sp', '')
                individuum = individuum.rstrip('.')
                if individuum not in result_list:
                    result_list.append(individuum)

	# Liste des Verzeichnisses /scr/genomes/Bacteria/Bacteria_NCBI/ anhaengen
    #path = '/scr/genomes/Bacteria/Bacteria_NCBI/*/'
    #individuum_pathes = glob.glob(path)
    #for path in individuum_pathes:
    #    individuum_title = path.rstrip('/').split('/')[-1]
    #    if individuum_title not in result_list:
    #        result_list.append(individuum_title)
    
    #file = '/home/alex/Studium/eclipse_workspace/Semester1/Sequenzanalyse/Praktikum/NCBI-Tree/directory_list'
    #with open(file) as f:
    #    for line in f:
    #        tmp_result = re.findall('^[A-Z][a-z]*_[a-z]*', line)
    #        if len(tmp_result) > 0:
    #            individuum = tmp_result[0].rstrip('_')
    #            individuum = individuum.replace('_', ' ')
    #            individuum = individuum.replace(' sp', '')
    #            if individuum not in result_list:
    #                result_list.append(individuum)
    
	# Zieldatei
    target_file = '/u/home/praktikum/PRAK12/tmp/individuum_list'
    file_handle = open(target_file, 'w+')
    for individuum_title in result_list:
        file_handle.write(individuum_title + '\n')
	
    file_handle.close()

#createIndividuumListFile()

def convertIndividuumTitels():
	#Alle Introns einlesen und relevante Daten speichern
	intron_file = '/u/home/praktikum/PRAK12/final/all_introns.txt'
	#>E.c.I5/AF074613/58241..60646/Escherichia coli/CL1/Intron Sequence
	intron_data = {}
	with open(intron_file) as f:
		for line in f:
			if line[0] == '>':
				data = line.split('/')
				ind_key = data[0].lstrip('>') + '/' + data[1]
				value = data[4]
				if ind_key not in intron_data:
					intron_data[ind_key] = []
					intron_data[ind_key].append(value)
	#Baum-Datei einlesen
	tree_result = []
	tree_file = '/u/home/praktikum/PRAK12/tmp/all_canditates.dnd'

	with open(tree_file) as f:
		for line in f:
			re_result = re.findall('^[A-Z]', line)
			if len(re_result) > 0:
				data = line.split(':')
				value = data[1]
				tmp_title = data[0].split('/')
				tmp_title = tmp_title[0] + '/' + tmp_title[1]
				title = intron_data[tmp_title][-1]
				insert_value = title + ':' + value
				line = insert_value
			tree_result.append(line)
	print(tree_result)
	target_file = '/u/home/praktikum/PRAK12/tmp/new.dnd'
	file_handle = open(target_file, 'w+')
	for line in tree_result:
		file_handle.write(line)
	file_handle.close()

#convertIndividuumTitels()

def createCandidatesSequenzFile():
	candidates_file = '/u/home/praktikum/PRAK12/tmp/canditates_list'
	candidates_result = []
	with open(candidates_file) as f:
		for line in f:
			candidates_result.append(line.rstrip('\n').replace('_', ':'))
	
	# Sequenzdatei aller Intronkandidaten
	candidates_intron_file = '/u/home/praktikum/PRAK12/tmp/candidates_sequenz_result'
	result = {}

	with open(candidates_intron_file) as f:
		for line in f:
			if len(line) > 1:
				line = line.rstrip('\n')
				if line[0] == '>':
					title = line.split(' ')[0].lstrip('>')
					result[title] = {'headrow' : line.replace(', complete genome', ''), 'data' : ''}
					continue
				result[title]['data'] += line
	
	target_file = '/u/home/praktikum/PRAK12/tmp/E1_candidates_sequenzes'
	file_handle = open(target_file, 'w+')
	for ind in candidates_result:
		file_handle.write(result[ind]['headrow'] + '\n')
		file_handle.write(result[ind]['data'] + '\n')
		file_handle.write('\n')
	file_handle.close()

#createCandidatesSequenzFile()

def extractDataFromIntronFile():
	file = '/home/alex/Studium/eclipse_workspace/Semester1/Sequenzanalyse/Praktikum/intron_candidate_data'
	tmp = {}
	i = 0
	tmp[i] = []
	
	with open(file) as f:
		for line in f:
			line = line.rstrip('\n')
			if len(line) <= 1:
				i+=1
				tmp[i] = []
				continue
			tmp[i].append(line)
	
	result = {}
	
	for key,dataset in tmp.items():
		if len(dataset) == 10:
			tmp_title = dataset[0].split(' ')[-1].split(':')[0].lstrip('(')
			tmp_start = dataset[3].lstrip('Position ')
			tmp_stop = dataset[7].lstrip('Position ')
			
			if tmp_title not in result:
				result[tmp_title] = []
				result[tmp_title].append([dataset[0], tmp_start, tmp_stop])
			else:
				test = False
				for subset in result[tmp_title]:
					if (int(subset[1]) == int(tmp_start)) and (int(subset[2]) == int(tmp_stop)):
						test = False
					else:
						test = True
				if test:
					result[tmp_title].append([dataset[0], tmp_start, tmp_stop])
	
	#for key,line in result.items():
	#	print(key)
	#	for set in line:
	#		print(set)
	
	target_file = '/home/alex/Studium/eclipse_workspace/Semester1/Sequenzanalyse/Praktikum/unique_intron_candidate_data.csv'
	file_handle = open(target_file, 'w+')
	
	for key,line in result.items():
		for subset in line:
			file_handle.write(','.join(subset) + '\n')
	file_handle.close()

extractDataFromIntronFile()
