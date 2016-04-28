import unittest

import os
import sys

script_path = os.path.abspath(__file__) + '/../../../..'
sys.path.append(os.path.abspath(script_path))
from semester2.rna_structures.nussinov import Nussinov


class TestNussinov(unittest.TestCase):

    def testInit(self):
        sequence = 'AGUC'
        self.nussinov = Nussinov(sequence)
        self.assertEqual(sequence, self.nussinov._sequence)
        self.assertEqual(len(sequence), self.nussinov._sequence_len)

        expected_result_sequence_init = [''] * len(sequence)
        self.assertEqual(expected_result_sequence_init,
                         self.nussinov._result_sequence)

        matrix = [[''] * len(sequence) for i in range(len(sequence))]
        self.assertEqual(matrix, self.nussinov._matrix)

    def testInitiate(self):
        sequence = 'AGUCGAUC'
        self.nussinov = Nussinov(sequence)
        self.nussinov.initiate()

        expected = [
            [0, 0, 0, 0, '', '', '', ''],
            [0, 0, 0, 0, 0, '', '', ''],
            ['', 0, 0, 0, 0, 0, '', ''],
            ['', '', 0, 0, 0, 0, 0, ''],
            ['', '', '', 0, 0, 0, 0, 0],
            ['', '', '', '', 0, 0, 0, 0],
            ['', '', '', '', '', 0, 0, 0],
            ['', '', '', '', '', '', 0, 0]
        ]
        self.assertEqual(expected, self.nussinov._matrix)

    def testGetK(self):

        self.nussinov = Nussinov('AGUC')

        expected = []
        self.assertEqual(expected, self.nussinov._getK(1, 1))

        expected = [2, 3, 4]
        self.assertEqual(expected, self.nussinov._getK(1, 4))

    def testGetBasePairedValue(self):

        self.nussinov = Nussinov('AGUC')

        expected = 1
        self.assertEqual(expected, self.nussinov._getBasePairedValue(0, 2))

        expected = 0
        self.assertEqual(expected, self.nussinov._getBasePairedValue(2, 3))

    def testCalculate(self):
        sequence = 'GGCAGACUAU'
        self.nussinov = Nussinov(sequence)
        self.nussinov.initiate()
        self.nussinov.calculate()

        expected = [
            [0, 0, 0, 0, 0, 0, 1, 2, 2, 2],
            [0, 0, 0, 0, 0, 0, 1, 1, 1, 2],
            ['', 0, 0, 0, 0, 0, 0, 1, 1, 1],
            ['', '', 0, 0, 0, 0, 0, 1, 1, 1],
            ['', '', '', 0, 0, 0, 0, 0, 0, 1],
            ['', '', '', '', 0, 0, 0, 0, 0, 1],
            ['', '', '', '', '', 0, 0, 0, 0, 0],
            ['', '', '', '', '', '', 0, 0, 0, 0],
            ['', '', '', '', '', '', '', 0, 0, 0],
            ['', '', '', '', '', '', '', '', 0, 0]
        ]
        self.assertEqual(expected, self.nussinov._matrix)

    def testOutput(self):
        sequence = 'CCAAAGGGGAAACC'
        self.nussinov = Nussinov(sequence)
        self.nussinov.initiate()
        self.nussinov.calculate()

        expected = [
            [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, ''],
            ['C', 'C', 'A', 'A', 'A', 'G', 'G', 'G', 'G', 'A', 'A', 'A', 'C', 'C', '', ''],
            [0, 0, 0, 0, 0, 1, 2, 2, 2, 2, 2, 2, 3, 4, 'C', 1],
            [0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 2, 3, 'C', 2],
            ['', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 2, 'A', 3],
            ['', '', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 2, 'A', 4],
            ['', '', '', 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 2, 'A', 5],
            ['', '', '', '', 0, 0, 0, 0, 0, 0, 0, 0, 1, 2, 'G', 6],
            ['', '', '', '', '', 0, 0, 0, 0, 0, 0, 0, 1, 2, 'G', 7],
            ['', '', '', '', '', '', 0, 0, 0, 0, 0, 0, 1, 2, 'G', 8],
            ['', '', '', '', '', '', '', 0, 0, 0, 0, 0, 1, 1, 'G', 9],
            ['', '', '', '', '', '', '', '', 0, 0, 0, 0, 0, 0, 'A', 10],
            ['', '', '', '', '', '', '', '', '', 0, 0, 0, 0, 0, 'A', 11],
            ['', '', '', '', '', '', '', '', '', '', 0, 0, 0, 0, 'A', 12],
            ['', '', '', '', '', '', '', '', '', '', '', 0, 0, 0, 'C', 13],
            ['', '', '', '', '', '', '', '', '', '', '', '', 0, 0, 'C', 14]
        ]

        result = self.nussinov.output()
        self.assertEqual(expected, result)

    def testBacktracking(self):
        sequence = 'CCAAAGGGGAAACC'
        self.nussinov = Nussinov(sequence)
        self.nussinov.initiate()
        self.nussinov.calculate()

        expected = ['(', '(', '.', '.', '.', ')', ')', '(', '(', '.', '.', '.', ')', ')']

        result = self.nussinov.backtracking()
        self.assertEqual(expected, result)


if __name__ == "__main__":
    unittest.main()
