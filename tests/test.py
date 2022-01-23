import os
import unittest

from .context import numeric_slv
import numeric_slv.utils as utils
test_pddl_files_dir = os.path.join(os.path.dirname(__file__), 'test_pddl_files')

class BasicTestSuite(unittest.TestCase):
    """Basic test cases."""

    def test_absolute_truth_and_meaning(self):
        assert True

class TestUTILS(unittest.TestCase):
    """Basic test cases."""

    def test_get_sas_translation(self):
        domain_file = os.path.join(test_pddl_files_dir, 'domain.pddl')
        problem_file = os.path.join(test_pddl_files_dir, 'pfile1.pddl')
        sas_as_list = utils.get_sas_translation(domain_file, problem_file)
        self.assertTrue(len(sas_as_list) > 100)

class TestSocialPlanningProblem(unittest.TestCase):

    def test_init(self):
        domain_file = os.path.join(test_pddl_files_dir, 'domain.pddl')
        problem_file = os.path.join(test_pddl_files_dir, 'pfile1.pddl')
        spp = numeric_slv.SocialPlanningProblem(domain_file, problem_file)





if __name__ == '__main__':
    unittest.main()
