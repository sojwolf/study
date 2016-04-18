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
        self.assertEqual(expected_result_sequence_init, self.nussinov._result_sequence)

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

if __name__ == "__main__":
    unittest.main()