###
#   initialization:
#       N(i,i) = 0
#       N(i,j) = 0 ... i<j<=i+3
#       N(i+1,j) = 0
#
#   calculation:
#                     ---
#                     | N(i+1,j) ...   i=unpaired
#       N(i,j) = max <
#                     |   max   N(i+1,k-1) + N(k+1,j) + F(i,k)
#                     | i+3<k<=j
#                     ---
#
#                 ---
#                 | 1 if i,k in (AU,GC,GU)
#   with F(i,k) = <
#                 | 0 else
#                 ---
###

# watson-crick and wobble base pairs
allowed_base_pairs = ['AU', 'UA', 'GC', 'CG', 'GU', 'UG']

sequence = 'AGGCAAUGCC'
sequence_len = len(sequence)

# minimal count of base between
min_count = 3

# create empty matrix
matrix = [['']*sequence_len for i in range(sequence_len)]


# initialization
def init():

    # diagonal initialization
    # initialization of i<j<=i+3
    i = 0
    for row in matrix:
        for n in range(min_count+1):
            if (i+n) < sequence_len:
                row[i+n] = 0
        i += 1

    # additional initialization of N(i+1,j)
    for i in range(0, sequence_len):
        if i < (sequence_len-1):
            matrix[i+1][i] = 0


def getK(i, j):
    k = list()

    for s in range(i, j+1):
        if (s > i) & (s <= j):
            k.append(s)

    return k


def getBasePairedValue(i, k):
    base_pair = sequence[i] + sequence[k]
    return 1 if base_pair in allowed_base_pairs else 0


def calculate():
    j_start = min_count + 1

    s = 0
    t = j_start
    while t <= sequence_len:
        i = 0
        jn = j_start + s
        for j in range(jn, sequence_len):
            # todo: über Liste der k-values itterieren
            k = getK(i+min_count, j)
            if len(k) == 1:
                print(i, j, k)
                trivial = matrix[i+1][j]
                k_value = k[0]+1

                base_paired_value = getBasePairedValue(i, k[0])
                if k_value < sequence_len:
                    calc = matrix[i+1][k[0]-1] + matrix[k[0]+1][j] +\
                        base_paired_value
                else:
                    calc = matrix[i+1][k[0]-1] + 0 + base_paired_value
                result = max(trivial, calc)
                matrix[i][j] = result
                i += 1
        s += 1
        t += 1


def output():

    # insert sequence as headline and headcolumn for view
    matrix.insert(0, list(sequence))

    i = 0
    for row in matrix:
        if i == 0:
            row.append('')
        else:
            row.append(sequence[i-1])
        i += 1

    # insert index numbers as headline and headcolumn for view
    sequence_index = list(range(1, sequence_len+1))
    matrix.insert(0, sequence_index)

    i = 0
    for row in matrix:
        if i < 2:
            row.append('')
        else:
            row.append(i-1)
        i += 1

    # matrix output
    for row in matrix:
        print("\t".join(map(str, row)) + "\n")
        pass

init()
calculate()
output()
