input = '/home/alexander/ownCloud/Studium/2. Semester/RNA und Proteinstrukturen/uebung/2/trna4.eps'
output = '/home/alexander/ownCloud/Studium/2. Semester/RNA und Proteinstrukturen/uebung/2/output.txt'
output2 = '/home/alexander/ownCloud/Studium/2. Semester/RNA und Proteinstrukturen/uebung/2/output2.txt'

data = []
sequence = ''
prop_data = []

f = open(input, 'r')

sequence_header = "/sequence { ("

for line in f:
    data.append(line)

for i, row in enumerate(data):
    if row[:-2] == sequence_header:
        sequence = data[i+1][:-2]

    if row[0] != '%' and row[-5:-1] == 'ubox':
        row_data = row.split(' ')
        prop_data.append([
            row_data[0],
            sequence[int(row_data[0])],
            row_data[1],
            sequence[int(row_data[1])],
            float(row_data[2])**2,
        ])

        base = row_data[0]


write_handle = open(output, '+w')
for row in prop_data:
    write_handle.write(",".join(map(str, row)) + '\n')

write_handle.close()