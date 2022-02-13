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
        domain_file = os.path.join(test_pddl_files_dir, 'depot_domain.pddl')
        problem_file = os.path.join(test_pddl_files_dir, 'depot_pfile1.pddl')
        sas_as_list = utils.get_sas_translation(domain_file, problem_file)
        self.assertTrue(len(sas_as_list) > 100)


class TestSocialPlanningProblem(unittest.TestCase):

    def test_arithmetic_expression_to_sym(self):
        from numeric_slv.zeta_compilation import arithmetic_expression_to_sym
        from translate.pddl import Difference, PrimitiveNumericExpression, NumericConstant, Sum, Product, \
            FunctionComparison
        # load_limit(truck0) - 5
        exp = Difference([PrimitiveNumericExpression(symbol='load_limit', args=('truck0',)), NumericConstant(value=5.)])
        sym_exp = arithmetic_expression_to_sym(exp)
        self.assertEqual('PNE load_limit(truck0) - 5.0', str(sym_exp))
        # load_limit(truck0) - 5 + 5
        exp_2 = Sum([NumericConstant(value=5.), exp])
        sym_exp_2 = arithmetic_expression_to_sym(exp_2)
        self.assertEqual('PNE load_limit(truck0)', str(sym_exp_2))
        # 2 * (load_limit(truck0) - 5)
        exp_3 = Product([NumericConstant(value=2.), exp])
        sym_exp_3 = arithmetic_expression_to_sym(exp_3)
        self.assertEqual('2.0*PNE load_limit(truck0) - 10.0', str(sym_exp_3))

    def test_convert_numerical_expressions_to_normal_form_of_function_comparison(self):
        from numeric_slv.zeta_compilation import convert_numerical_expressions_to_normal_form_of_function_comparison
        from translate.pddl import FunctionComparison, Difference, PrimitiveNumericExpression, NumericConstant, Product, \
            Sum
        # load_limit(truck0) - 5 >= 10
        pne = PrimitiveNumericExpression(symbol='load_limit', args=('truck0',))
        exp = Difference([pne, NumericConstant(value=5.)])
        eq = FunctionComparison('>=', [exp, NumericConstant(10)])
        simplified_eq = convert_numerical_expressions_to_normal_form_of_function_comparison(eq)
        expected_eq = FunctionComparison('>=', [pne, NumericConstant(15)])
        self.assertEqual(simplified_eq, expected_eq)
        # 2*(load_limit(truck0) - 5) >= 10
        exp_2 = Product([NumericConstant(2), exp])
        eq_2 = FunctionComparison('>=', [exp_2, NumericConstant(10)])
        simplified_eq = convert_numerical_expressions_to_normal_form_of_function_comparison(eq_2)
        expected_eq = FunctionComparison('>=', [pne, NumericConstant(10)])
        self.assertEqual(simplified_eq, expected_eq)
        # load_limit(truck0) - 5 >= load_limit(truck1)
        pne_0 = PrimitiveNumericExpression(symbol='load_limit', args=('truck0',))
        pne_1 = PrimitiveNumericExpression(symbol='load_limit', args=('truck1',))
        exp_left = Difference([pne_0, NumericConstant(value=5.)])
        exp_right = pne_1
        eq_3 = FunctionComparison('>=', [exp_left, exp_right])
        simplified_eq = convert_numerical_expressions_to_normal_form_of_function_comparison(eq_3)
        expected_eq = FunctionComparison('>=',
                                         [Sum([pne_0, Product([NumericConstant(-1.), pne_1])]), NumericConstant(5)])
        self.assertEqual(simplified_eq, expected_eq)
        # x >= y + z
        x, y, z = PrimitiveNumericExpression(symbol='x', args=tuple()), \
                  PrimitiveNumericExpression(symbol='y',args=tuple()), \
                  PrimitiveNumericExpression(symbol='z', args=tuple())
        left = x
        right = Sum([y, z])
        eq_4 = FunctionComparison('>=', [left, right])
        simplified_eq_4 = convert_numerical_expressions_to_normal_form_of_function_comparison(eq_4)
        expected_eq_4 = FunctionComparison('>=', [Sum([x, Sum([Product([NumericConstant(-1.), y]), Product([NumericConstant(-1.), z])])]), NumericConstant(0.)])
        self.assertEqual(simplified_eq_4, expected_eq_4)
        # x <= y + z => -x + y + z >= 0
        x, y, z = PrimitiveNumericExpression(symbol='x', args=tuple()), \
                  PrimitiveNumericExpression(symbol='y',args=tuple()), \
                  PrimitiveNumericExpression(symbol='z', args=tuple())
        left = x
        right = Sum([y, z])
        eq_4 = FunctionComparison('<=', [left, right])
        simplified_eq_4 = convert_numerical_expressions_to_normal_form_of_function_comparison(eq_4)
        expected_eq_4 = FunctionComparison('>=', [Sum([y, Sum([z, Product([NumericConstant(-1.), x])])]), NumericConstant(0.)])
        self.assertEqual(simplified_eq_4, expected_eq_4)

    def test_init(self):
        domain_file = os.path.join(test_pddl_files_dir, 'lunch_domain.pddl')
        problem_file = os.path.join(test_pddl_files_dir, 'lunch_pfile1.pddl')
        spp = numeric_slv.SocialPlanningProblem(domain_file, problem_file)


if __name__ == '__main__':
    unittest.main()
