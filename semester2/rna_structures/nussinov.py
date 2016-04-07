###
#   initialization:
#       N(i,i) = 0
#       N(i,j) = 0 ... i<j<=i+3
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

sequence = 'GGGAAAUCC'
sequence_len = len(sequence)

# minimal count of base between
min_count = 3

# create empty matrix
matrix = [['']*sequence_len for i in range(sequence_len)]

# initialization
def init():

    i = 0
    for row in matrix:
        for n in range(min_count+1):
            if (i+n) < sequence_len:
                row[i+n] = '0'
        i += 1

def calculate():
    pass

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

    for row in matrix:
        print("\t".join(row) + "\n")
        pass

init()
output()
