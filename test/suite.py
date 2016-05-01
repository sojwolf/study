'''
install coverage:
sudo pip install coverage

run tests to collect data:
coverage run suite.py

show data from tests in terminal:
coverage report

generate html output:
coverage html -d test_report
'''

import unittest
import test_semester2.test_rna_structures.nussinov_test

suite = unittest.TestLoader()
suite = suite.loadTestsFromModule(
    test_semester2.test_rna_structures.nussinov_test)

unittest.TextTestRunner().run(suite)
