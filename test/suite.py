import sys
import os
import unittest

script_path = '/home/alex/workspace/study/test'
sys.path.append(os.path.abspath(script_path))
import test_semester2.test_rna_structures.nussinov_test

suite = unittest.TestLoader()
suite = suite.loadTestsFromModule(test_semester2.test_rna_structures.nussinov_test)

unittest.TextTestRunner().run(suite)