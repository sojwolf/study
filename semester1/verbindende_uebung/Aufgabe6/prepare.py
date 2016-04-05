codons = {'TAG': 3876, 'AAG': 178080, 'TCC': 83086, 'GTC': 93666, 'GAT': 195060, 'GCC': 114179, 'CGC': 55703, 'CCA': 105049, 'ATN': 1, 'CTT': 78594, 'GCA': 92652, 'AGG': 73982, 'GCT': 143776, 'CCC': 76258, 'AGT': 92411, 'GGT': 112491, 'NAG': 1, 'AAA': 246496, 'GGC': 95827, 'AAC': 150609, 'CAG': 123144, 'CAT': 80020, 'CTA': 69576, 'ACA': 120207, 'GGG': 54485, 'ACC': 82078, 'TTC': 129037, 'CAC': 88830, 'AAT': 173216, 'GAC': 178859, 'TGT': 78620, 'TTT': 106240, 'CCT': 89363, 'GTG': 137366, 'GTA': 84846, 'CGG': 41121, 'ACG': 78731, 'ATA': 153118, 'AGA': 117190, 'GCG': 102957, 'CCG': 89537, 'TGG': 75549, 'ATC': 96989, 'ACT': 101555, 'GGA': 112550, 'TGC': 59841, 'CAA': 132723, 'GAA': 252369, 'AGC': 81843, 'TTG': 114734, 'TAT': 104149, 'TCT': 93556, 'TTA': 117269, 'ATT': 111703, 'GTT': 113917, 'CGA': 51532, 'CTG': 136596, 'ATG': 149910, 'CGT': 57755, 'TCA': 101479, 'TAC': 114100, 'TGA': 5215, 'CTC': 95194, 'TAA': 7163, 'GAG': 189373, 'TCG': 72613}
aminos = {'W': 75549, 'X': 2, 'S': 524988, 'N': 323825, 'C': 138461, 'I': 361810, 'Y': 218249, 'H': 168850, 'E': 441742, 'K': 424576, 'D': 373919, 'F': 235277, 'P': 360207, 'M': 149910, 'G': 375353, 'R': 397283, 'Q': 255867, 'T': 382571, 'V': 429795, 'A': 453564, 'L': 611963}

codons = {
    'TGG': 75549, 'ATG': 149910,
    'TGC': 59841, 'TGT': 78620,
    'ATA': 153118, 'ATC': 96989, 'ATT': 111703,
}
aminos = {
    'W': 75549, 'M': 149910,
    'C': 138461,
    'I': 361810,
}

codon_amino_map = {}

def infos():
    print(codon_amino_map)
    print(len(codons))
    print(len(aminos))

#infos()

# 1:1-Verknüpfungen ermitteln
for i in codons:
    for j in aminos:
        if codons[i] == aminos[j]:
            #print(str(i) + ":" + str(codons[i]) + "/" + str(j) + ":" + str(aminos[j]))
            codon_amino_map[j] = [i]

# und aus den Basisdaten löschen
for k in codon_amino_map:
    if k in aminos:
        aminos.pop(k)
    for l in codon_amino_map[k]:
        if l in codons:
            codons.pop(l)

#infos()

for i in sorted(aminos.values()):
    amino_value = i
    for j in sorted(codons.values(), reverse=True):
        if j > amino_value:
            continue
        print(j, amino_value)
    break