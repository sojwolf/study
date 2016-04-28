from copy import deepcopy

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


class Nussinov():

    # watson-crick and wobble base pairs
    _allowed_base_pairs = ['AU', 'UA', 'GC', 'CG', 'GU', 'UG']

    _sequence = ''
    _sequence_len = 0
    _result_sequence = None

    # minimal count of base between
    _min_count = 3

    # create empty matrix
    _matrix = None

    def __init__(self, sequence):
        self._sequence = sequence
        self._sequence_len = len(sequence)
        self._result_sequence = [''] * self._sequence_len
        self._matrix = [[''] * self._sequence_len
                        for i in range(self._sequence_len)]

    # initialization
    def initiate(self):

        # diagonal initialization, initialization of i<j<=i+3
        i = 0
        for row in self._matrix:
            for n in range(self._min_count+1):
                if (i+n) < self._sequence_len:
                    row[i+n] = 0
            i += 1

        # additional initialization of N(i+1,j)
        for i in range(0, self._sequence_len):
            if i < (self._sequence_len-1):
                self._matrix[i+1][i] = 0

    def _getK(self, i, j):
        return list(range(i+1, j+1))

    def _getBasePairedValue(self, i, k):
        base_pair = self._sequence[i] + self._sequence[k]
        return 1 if base_pair in self._allowed_base_pairs else 0

    def calculate(self):
        j_start = self._min_count + 1

        s = 0
        t = j_start
        while t <= self._sequence_len:
            i = 0
            jn = j_start + s
            for j in range(jn, self._sequence_len):
                k_values = self._getK(i + self._min_count, j)
                results = []
                for k in k_values:
                    trivial = self._matrix[i + 1][j]
                    results.append(trivial)

                    k_value = k + 1

                    base_paired_value = self._getBasePairedValue(i, k)
                    if k_value < self._sequence_len:
                        calc = self._matrix[i+1][k-1] + self._matrix[k+1][j] +\
                            base_paired_value
                    else:
                        calc = self._matrix[i+1][k-1] + 0 + base_paired_value
                    results.append(calc)
                self._matrix[i][j] = max(results)
                i += 1
            s += 1
            t += 1

    def output(self):

        # copy matrix for output
        output_matrix = deepcopy(self._matrix)

        # insert sequence as headline and headcolumn for view
        output_matrix.insert(0, list(self._sequence))

        for i, row in enumerate(output_matrix):
            if i == 0:
                row.append('')
            else:
                row.append(self._sequence[i-1])
            i += 1

        # insert index numbers as headline and headcolumn for view
        sequence_index = list(range(1, self._sequence_len + 1))
        output_matrix.insert(0, sequence_index)

        for i, row in enumerate(output_matrix):
            if i < 2:
                row.append('')
            else:
                row.append(i-1)
            i += 1

        return output_matrix

    def printOutput(self):   # pragma: no cover (excluded from coverage)
        output = self.output()
        for row in output:
            print("\t".join(map(str, row)) + "\n")

    def backtracking(self):
        backtracking = []
        for i in self._sequence:
            backtracking.append('-')

        stack = [[0, self._sequence_len-1]]

        while stack != []:
            current = stack.pop()
            i = current[0]
            j = current[1]

            if i > j:
                continue

            if i == j:
                backtracking[j] = "."
                continue

            if self._matrix[i][j] == self._matrix[i+1][j]:
                backtracking[i] = "."
                stack.append([i+1, j])
                continue

            for k in range(i + 1 + self._min_count, j+1):
                base_paired_value = self._getBasePairedValue(i, k)
                if base_paired_value:
                    exprTwo = 0
                    if j - (k + 1) > -1:
                        exprTwo = self._matrix[k+1][j]

                    if self._matrix[i][j] == self._matrix[i+1][k-1]\
                            + exprTwo + base_paired_value:
                        backtracking[i] = '('
                        backtracking[k] = ')'
                        stack.append([i+1, k-1])
                        stack.append([k+1, j])

        return backtracking

    def printBacktracking(self):   # pragma: no cover (excluded from coverage)
        backtracking = self.backtracking()
        print(self._sequence)
        print(''.join(backtracking))

if __name__ == "__main__":
    sequence = 'CCAAAGGGGAAACC'
    nussinov = Nussinov(sequence)
    nussinov.initiate()
    nussinov.calculate()
    nussinov.printOutput()
    nussinov.printBacktracking()
