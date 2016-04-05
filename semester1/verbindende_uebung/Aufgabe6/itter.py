codons = {'TGC':2,'TGT':3,'ATA':9,'ATC':7,'ATT':4}
aminos = {'C':5, 'I':20}

codons = {'TGG': 75549, 'ATG': 149910,'TGC': 59841, 'TGT': 78620,'ATA': 153118, 'ATC': 96989, 'ATT': 111703,'CCA':105049,'CCC':76258,'CCG':89537,'CCT':89363,}
aminos = {'W': 75549, 'M': 149910,'C': 138461,'I': 361810,'P':360207,}

codons = {'ATA': 153118, 'ATC': 96989, 'ATT': 111703,'CCA':105049,'CCC':76258,'CCG':89537,'CCT':89363,}
aminos = {'I': 361810,'P':360207,}

#codons = {'TAG': 3876, 'AAG': 178080, 'TCC': 83086, 'GTC': 93666, 'GAT': 195060, 'GCC': 114179, 'CGC': 55703, 'CCA': 105049, 'ATN': 1, 'CTT': 78594, 'GCA': 92652, 'AGG': 73982, 'GCT': 143776, 'CCC': 76258, 'AGT': 92411, 'GGT': 112491, 'NAG': 1, 'AAA': 246496, 'GGC': 95827, 'AAC': 150609, 'CAG': 123144, 'CAT': 80020, 'CTA': 69576, 'ACA': 120207, 'GGG': 54485, 'ACC': 82078, 'TTC': 129037, 'CAC': 88830, 'AAT': 173216, 'GAC': 178859, 'TGT': 78620, 'TTT': 106240, 'CCT': 89363, 'GTG': 137366, 'GTA': 84846, 'CGG': 41121, 'ACG': 78731, 'ATA': 153118, 'AGA': 117190, 'GCG': 102957, 'CCG': 89537, 'TGG': 75549, 'ATC': 96989, 'ACT': 101555, 'GGA': 112550, 'TGC': 59841, 'CAA': 132723, 'GAA': 252369, 'AGC': 81843, 'TTG': 114734, 'TAT': 104149, 'TCT': 93556, 'TTA': 117269, 'ATT': 111703, 'GTT': 113917, 'CGA': 51532, 'CTG': 136596, 'ATG': 149910, 'CGT': 57755, 'TCA': 101479, 'TAC': 114100, 'TGA': 5215, 'CTC': 95194, 'TAA': 7163, 'GAG': 189373, 'TCG': 72613}
#aminos = {'W': 75549, 'X': 2, 'S': 524988, 'N': 323825, 'C': 138461, 'I': 361810, 'Y': 218249, 'H': 168850, 'E': 441742, 'K': 424576, 'D': 373919, 'F': 235277, 'P': 360207, 'M': 149910, 'G': 375353, 'R': 397283, 'Q': 255867, 'T': 382571, 'V': 429795, 'A': 453564, 'L': 611963}

def getKeyByValue(dict={}, value=''):
    for i in dict:
        if dict[i]==value:
            return i;

res = {}

for a_value in sorted(aminos.values()):
    current_codons = codons.copy()
    amino_key = getKeyByValue(aminos, a_value)
    res[amino_key] = []
    while True:
        tmp = []
        current_amino_value = a_value
        print("aktuelles Amino: " + str(current_amino_value))
        sorted_codon_values = sorted(current_codons.values(), reverse=True)
        
        for codon_value in sorted_codon_values:
            substitution_list = sorted_codon_values.copy()
            if codon_value > current_amino_value:
                print(str(codon_value) + " zu groß")
                # zu hohe Werte aus Liste für innere Schleife entfernen
                substitution_list.remove(codon_value)
                continue
            for codon_subvalue in substitution_list:
                print("Abziehen: " + str(codon_subvalue))
                result = current_amino_value - codon_subvalue
                print("Ergebnis: " + str(result))
                if result == 0:
                    print("raus")
                    test = True
                    key = getKeyByValue(current_codons, codon_subvalue)
                    tmp.append(key)
                    break
                
                if result > 0:
                    print("weiter abziehen")
                    current_amino_value = result
                    test = False
                    key = getKeyByValue(current_codons, codon_subvalue)
                    current_codons.pop(key)
                    # Zahl merken
                    tmp.append(key)
        # Schleife ohne Ergebnis durchlaufen, alle Ergebnisse bis
        # auf das erste aus der sortierten Liste zurücklegen
        for v in range(len(sorted_codon_values)):
            if v == 0:
                continue
            value_to_put_back = sorted_codon_values[v]
            key = getKeyByValue(codons, value_to_put_back)
            current_codons[key] = value_to_put_back
        if test == True:
            res[amino_key] = tmp
            # zugewiesene Codons aus Liste entfernen
            for used_codon in tmp:
                codons.pop(used_codon)
            break

print(res)
print(codons)