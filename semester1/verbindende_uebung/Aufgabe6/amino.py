amino = {'ATC': 96989, 'TCC': 83086, 'CGC': 55703, 'CTG': 136596, 'CGA': 51532, 'TGG': 75549, 'CTC': 95194, 'GGG': 54485, 'GCA': 92652, 'GCT': 143776, 'TAT': 104149, 'CGG': 41121, 'TGA': 5215, 'ACG': 78731, 'TTT': 106240, 'GTC': 93666, 'TAC': 114100, 'TGT': 78620, 'GAG': 189373, 'GAC': 178859, 'ACC': 82078, 'ATT': 111703, 'GGT': 112491, 'ATG': 149910, 'AAA': 246496, 'CTA': 69576, 'GAT': 195060, 'CAT': 80020, 'CCG': 89537, 'CAA': 132723, 'CTT': 78594, 'ACA': 120207, 'TTG': 114734, 'ATA': 153118, 'AAT': 173216, 'TGC': 59841, 'AAC': 150609, 'TAA': 7163, 'CAG': 123144, 'TCG': 72613, 'GGC': 95827, 'TTC': 129037, 'GGA': 112550, 'GAA': 252369, 'GTA': 84846, 'AGA': 117190, 'CGT': 57755, 'TCA': 101479, 'GTT': 113917, 'GCG': 102957, 'AGC': 81843, 'AGT': 92411, 'TTA': 117269, 'GTG': 137366, 'NAG': 1, 'GCC': 114179, 'ACT': 101555, 'TCT': 93556, 'TAG': 3876, 'AGG': 73982, 'CCA': 105049, 'CCC': 76258, 'CCT': 89363, 'AAG': 178080, 'CAC': 88830, 'ATN': 1}
print(len(amino))
print(amino)

amino_sum = sum(amino.values())

file = open('/home/alexander/amino.csv', 'w')
seperator = ';'

# Kopfzeile schreiben
head_row = ['Aminosäure', 'abs. Häufigkeit', 'rel. Häufigkeit' + "\n"]
file.write(seperator.join(head_row))
# Sortierung bei der Ausgabe
for key in sorted(amino.keys()):
    rel_frequency = (amino[key]/amino_sum)*100
    output = [key, str(amino[key]), str('% .6f' % rel_frequency)]
    file.write(seperator.join(output) + "\n")