import os
import unittest

from numeric_slv.main import main

test_pddl_files_dir = os.path.join(os.path.dirname(__file__), 'test_pddl_files')

class BasicTestSuite(unittest.TestCase):
    """Basic test cases."""

    def test_absolute_truth_and_meaning(self):
        assert True

class TestMain(unittest.TestCase):

    def test_main(self):
        domain_file = os.path.join(test_pddl_files_dir, 'lunch_domain.pddl')
        problem_file = os.path.join(test_pddl_files_dir, 'lunch_pfile1.pddl')
        waitfor_file = os.path.join(test_pddl_files_dir, 'lunch_pfile1_waitfor.json')
        main(domain_file, problem_file, waitfor_file)

if __name__ == '__main__':
    unittest.main()
