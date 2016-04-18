import unittest

import os
import sys

script_path = '/home/alex/workspace/study'
sys.path.append(os.path.abspath(script_path))

from semester2.rna_structures.nussinov import getK, getBasePairedValue, sequence

class TestNussinov(unittest.TestCase):

    def testGetK(self):

        expected = []
        self.assertEqual(expected, getK(1, 1))

        expected = [2, 3, 4]
        self.assertEqual(expected, getK(1, 4))

    def testGetBasePairedValue(self):
        sequence = 'AGUC'
        expected = 1
        self.assertEqual(expected, getBasePairedValue(0, 2))

        expected = 0
        self.assertEqual(expected, getBasePairedValue(2, 3))


if __name__ == "__main__":
    unittest.main()