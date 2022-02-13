from copy import deepcopy

import sympy as sym

from translate.pddl import FunctionComparison, Task, Action, Conjunction, Literal, ArithmeticExpression, \
    PrimitiveNumericExpression, NumericConstant, Effect, FunctionAssignment, Sum, Product


def arithmetic_expression_to_sym(exp, pne_dict=dict()):
    """
    gets an ArithmeticExpression and translate it to sympy expression
    """
    if isinstance(exp, ArithmeticExpression):
        if exp.op == '+':
            return arithmetic_expression_to_sym(exp.parts[0], pne_dict) + arithmetic_expression_to_sym(exp.parts[1],
                                                                                                       pne_dict)
        elif exp.op == '-':
            return arithmetic_expression_to_sym(exp.parts[0], pne_dict) - arithmetic_expression_to_sym(exp.parts[1],
                                                                                                       pne_dict)
        elif exp.op == '*':
            return arithmetic_expression_to_sym(exp.parts[0], pne_dict) * arithmetic_expression_to_sym(exp.parts[1],
                                                                                                       pne_dict)
        elif exp.op == '/':
            return arithmetic_expression_to_sym(exp.parts[0], pne_dict) / arithmetic_expression_to_sym(exp.parts[1],
                                                                                                       pne_dict)
        else:
            raise NotImplemented
    elif isinstance(exp, PrimitiveNumericExpression):
        symbol_name = str(exp)
        pne_dict[symbol_name] = deepcopy(exp)
        return sym.Symbol(symbol_name)
    elif isinstance(exp, NumericConstant):
        return exp.value
    else:
        raise NotImplemented


def convert_numerical_expressions_to_normal_form_of_function_comparison(obj):
    """
    gets FunctionComparison object and modify it to have a normal form:
    - constants on the right
    - variables on the left
    - greater than operator
    e.g.
    w1 * v1 <= w2 * v2 -5 =>
    \sum w_vi * vi >= v0
    """
    assert isinstance(obj, FunctionComparison), f'expected a function comparison, got: {obj}'
    pne_dict = dict()
    left = arithmetic_expression_to_sym(obj.parts[0], pne_dict)
    right = arithmetic_expression_to_sym(obj.parts[1], pne_dict)
    comparitor = obj.comparator
    eq = eval('left' + comparitor + 'right')
    eq = convert_sympy_expressions_to_normal_form(eq.simplify())
    return sym_expression_to_pddl_numerical_expression(eq, pne_dict)


def convert_numerical_expressions_to_normal_form(obj):
    """
    gets FunctionComparison object and modify it to have a normal form:
    - constants on the right
    - variables on the left
    - greater than operator
    e.g.
    w1 * v1 <= w2 * v2 -5 =>
    \sum w_vi * vi >= v0
    """

    def binary_tree_to_list(tree):
        if tree.parts:
            left = tree.parts[0]
            right = tree.parts[1]
            op = tree.comparator if isinstance(tree, FunctionComparison) else tree.op
            return binary_tree_to_list(left) + [op] + binary_tree_to_list(right)
        else:
            return [tree]

    if isinstance(obj, Task):
        modified_task = deepcopy(obj)
        modified_task.actions = [convert_numerical_expressions_to_normal_form(a) for a in modified_task.actions]
        return modified_task
    elif isinstance(obj, Action):
        modified_action = deepcopy(obj)
        modified_action.precondition = convert_numerical_expressions_to_normal_form(modified_action.precondition)
        modified_action.effects = [convert_numerical_expressions_to_normal_form(eff) for eff in modified_action.effects]
        return modified_action
    elif isinstance(obj, Conjunction):
        modified_conjunction = deepcopy(obj)
        modified_conjunction.parts = [convert_numerical_expressions_to_normal_form(p) for p in
                                      modified_conjunction.parts]
        return modified_conjunction
    elif isinstance(obj, Literal):
        return deepcopy(obj)
    elif isinstance(obj, FunctionComparison):
        modified_comparison = deepcopy(obj)
        modified_comparison = convert_numerical_expressions_to_normal_form_of_function_comparison(modified_comparison)
        return modified_comparison
    elif isinstance(obj, Effect):
        modified_eff = deepcopy(obj)
        modified_eff.peffect = convert_numerical_expressions_to_normal_form(modified_eff.peffect)
        return modified_eff
    elif isinstance(obj, FunctionAssignment):
        f_assignment = deepcopy(obj)
        assert isinstance(f_assignment.fluent,
                          PrimitiveNumericExpression), f'expected a PNE, got: {f_assignment.fluent}'
        f_assignment.expression = convert_numerical_expressions_to_normal_form(f_assignment.expression)
        return f_assignment
    elif isinstance(obj, NumericConstant):
        return deepcopy(obj)
    elif isinstance(obj, PrimitiveNumericExpression):
        return deepcopy(obj)
    else:
        raise NotImplemented


def convert_sympy_expressions_to_normal_form(eq):
    """
    gets a sympy expressions and converts them to normal form:
    - constants on the right
    - variables on the left
    - greater than operator
    e.g.
    w1 * v1 <= w2 * v2 -5 =>
    \sum w_vi * vi >= v0
    """
    if isinstance(eq, sym.GreaterThan):
        # move all to the right
        l = eq.lhs
        r = eq.rhs
        new_l = l - r
        new_r = sym.simplify(0)
        coeff_dict = new_l.as_coefficients_dict()
        for key in coeff_dict.keys():
            if key == 1:
                new_l = new_l - coeff_dict[key]
                new_r = new_r - coeff_dict[key]
        return sym.GreaterThan(new_l, new_r)
    elif isinstance(eq, sym.LessThan):
        modified_eq = sym.GreaterThan(-1 * eq.lhs, -1 * eq.rhs)
        return convert_sympy_expressions_to_normal_form(modified_eq)
    else:
        raise NotImplemented


def sym_expression_to_pddl_numerical_expression(sym_exp, pne_dict):
    """
    gets a sympy numeric expression and translate it to ArithmeticExpression
    """
    from sympy.core.relational import Relational
    if isinstance(sym_exp, Relational):
        comparator = sym_exp.rel_op
        left = sym_expression_to_pddl_numerical_expression(sym_exp.args[0], pne_dict)
        right = sym_expression_to_pddl_numerical_expression(sym_exp.args[1], pne_dict)
        return FunctionComparison(comparator, [left, right])
    elif isinstance(sym_exp, sym.Symbol):
        return pne_dict[str(sym_exp)]
    elif isinstance(sym_exp, sym.Float):
        return NumericConstant(float(sym_exp))
    elif isinstance(sym_exp, sym.Add):
        left = sym_expression_to_pddl_numerical_expression(sym_exp.args[0], pne_dict)
        right = sym_expression_to_pddl_numerical_expression(sym_exp - sym_exp.args[0], pne_dict)
        return Sum([left, right])
    elif isinstance(sym_exp, sym.Mul):
        assert len(sym_exp.args) == 2, f'expected maximum argument length mul. of 2, received: {sym_exp}'
        left = sym_expression_to_pddl_numerical_expression(sym_exp.args[0], pne_dict)
        right = sym_expression_to_pddl_numerical_expression(sym_exp.args[1], pne_dict)
        return Product([left, right])
    elif isinstance(sym_exp, sym.Number):
        return NumericConstant(float(sym_exp))
    else:
        raise NotImplemented
