from copy import deepcopy

import sympy as sym

from translate.pddl import FunctionComparison, Task, Action, Conjunction, Literal, ArithmeticExpression, \
    PrimitiveNumericExpression, NumericConstant, Effect, FunctionAssignment, Sum, Product, Atom, Function, Assign, \
    conditions, NegatedAtom, Increase, Decrease
from translate.pddl.conditions import ConstantCondition


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
        modified_task.goal = convert_numerical_expressions_to_normal_form(modified_task.goal)
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
        assert isinstance(f_assignment.fluent, PrimitiveNumericExpression), \
            f'expected a PNE, got: {f_assignment.fluent}'
        f_assignment.expression = convert_numerical_expressions_to_normal_form(f_assignment.expression)
        return f_assignment
    elif isinstance(obj, NumericConstant):
        return deepcopy(obj)
    elif isinstance(obj, PrimitiveNumericExpression):
        return deepcopy(obj)
    elif isinstance(obj, ConstantCondition):
        return obj
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


def is_function_comparison_simple(f: FunctionComparison):
    """
    gets a FunctionComparison object and returns true if the left side is a single numeric expression and the right
    side is a numeric constant
    """
    left, right = f.parts
    return isinstance(left, PrimitiveNumericExpression) and isinstance(right, NumericConstant)


def replace_complex_numerical_expressions_with_zeta_variables(obj, zeta_dict_list=[], num_init_list=[]):
    """
    gets an object (e.g. FunctionComparison, Task) and replaces complex numerical expressions with simple ones
    by adding zeta variables
    """

    def get_zeta_dict(f: FunctionComparison):
        assert isinstance(f, FunctionComparison), f'expected FunctionComparison, got:{f}'
        zeta_dict = dict()
        left, right = f.parts
        assert isinstance(right, NumericConstant), f'expected right side to be numeric constant, got:{right}'
        pne_dict = dict()
        sym_expr = arithmetic_expression_to_sym(left, pne_dict)
        coeff_dict = sym_expr.as_coefficients_dict()
        zeta_as_vector = [0] * len(num_init_list)
        for key, value in coeff_dict.items():
            idx = num_init_list.index(key.name)
            zeta_as_vector[idx] = float(value)
        zeta_dict['f'] = f
        zeta_dict['left'] = left
        zeta_dict['as_vector'] = tuple(zeta_as_vector)
        zeta_dict['coeff_dict'] = dict((key.name, float(value)) for key, value in coeff_dict.items())
        return zeta_dict

    def get_zeta_dict_list(task):
        # compute zeta_dict_list: a list of dictionaries with data on needed zeta variables
        zeta_cnt = 0
        zeta_dict_list = []
        for action in task.actions:
            if isinstance(action.precondition, Conjunction):
                for pre in action.precondition.parts:
                    if isinstance(pre, Atom) or isinstance(pre, NegatedAtom):
                        continue
                    elif isinstance(pre, FunctionComparison):
                        if is_function_comparison_simple(pre):
                            continue
                        else:
                            zeta_dict = get_zeta_dict(pre)
                            if zeta_dict['as_vector'] in [z['as_vector'] for z in zeta_dict_list]:
                                continue
                            else:
                                zeta_dict['name'] = f'zeta_{zeta_cnt}'
                                zeta_dict_list.append(zeta_dict)
                                zeta_cnt += 1
                    else:
                        raise NotImplemented
            elif isinstance(action.precondition, Atom):
                continue
            elif isinstance(action.precondition, ConstantCondition):
                continue
            else:
                raise NotImplemented
        return zeta_dict_list

    if isinstance(obj, Task):
        assert zeta_dict_list == [], f'expected empty list, got: {zeta_dict_list}'
        assert num_init_list == [], f'expected empty list, got: {zeta_dict_list}'
        modified_task = deepcopy(obj)
        num_init_list = [str(v.fluent) for v in obj.num_init]
        zeta_dict_list = get_zeta_dict_list(modified_task)
        # add zeta variables to domain variables
        for z_dict in zeta_dict_list:
            function = Function(z_dict['name'], [], 'number')
            modified_task.functions.append(function)
        # modify actions
        modified_actions = []
        for action in obj.actions:
            mod_action = replace_complex_numerical_expressions_with_zeta_variables(action, zeta_dict_list,
                                                                                   num_init_list)
            modified_actions.append(mod_action)
        modified_task.actions = modified_actions
        # modify initial state
        zeta_num_init = []
        str_num_init_list = [str(a.fluent) for a in obj.num_init]
        for z_dict in zeta_dict_list:
            zeta_fluent = PrimitiveNumericExpression(symbol=z_dict['name'], args=tuple())
            zeta_initial_value = .0
            coeff_dict = z_dict['coeff_dict']
            for coeff in coeff_dict.keys():
                idx = str_num_init_list.index(coeff)
                k = obj.num_init[idx].expression.value
                zeta_initial_value += coeff_dict[coeff] * k
            zeta_assign = Assign(fluent=zeta_fluent, expression=NumericConstant(zeta_initial_value))
            zeta_num_init.append(zeta_assign)
        modified_task.num_init.extend(zeta_num_init)
        # modify goal
        modified_task.goal = \
            replace_complex_numerical_expressions_with_zeta_variables(modified_task.goal, zeta_dict_list, num_init_list)
        return modified_task
    elif isinstance(obj, Action):
        modified_precondition = replace_complex_numerical_expressions_with_zeta_variables(obj.precondition,
                                                                                          zeta_dict_list, num_init_list)
        modified_effects = replace_complex_numerical_expressions_with_zeta_variables(obj.effects,
                                                                                     zeta_dict_list, num_init_list)
        modified_action = deepcopy(obj)
        modified_action.precondition = modified_precondition
        modified_action.effects = modified_effects
        return modified_action
    elif isinstance(obj, Conjunction):
        # modify preconditions
        modified_precondition_parts = []
        for p in obj.parts:
            modified_p = replace_complex_numerical_expressions_with_zeta_variables(p, zeta_dict_list, num_init_list)
            modified_precondition_parts.append(modified_p)
        new_conj = deepcopy(obj)
        new_conj.parts = modified_precondition_parts
        return new_conj
    elif isinstance(obj, Atom) or isinstance(obj, NegatedAtom):
        return deepcopy(obj)
    elif isinstance(obj, FunctionComparison):
        if is_function_comparison_simple(obj):
            # is complex?
            return deepcopy(obj)
        else:
            # find the corresponding zeta
            obj_zeta_dict = get_zeta_dict(obj)
            zeta_vector_list = [z['as_vector'] for z in zeta_dict_list]
            assert obj_zeta_dict['as_vector'] in zeta_vector_list, f'expected formula in the dict list, formula: {obj}'
            idx = zeta_vector_list.index(obj_zeta_dict['as_vector'])
            zeta_dict = zeta_dict_list[idx]
            # build new pre with zeta
            zeta_name = zeta_dict['name']
            modified_left = PrimitiveNumericExpression(zeta_name, [])
            new_function_comparison = deepcopy(obj)
            new_function_comparison.parts = modified_left, new_function_comparison.parts[1]
            return new_function_comparison
    elif isinstance(obj, list) and obj and isinstance(obj[0], Effect):
        modified_effects = []
        for o in obj:
            eff = replace_complex_numerical_expressions_with_zeta_variables(o, zeta_dict_list, num_init_list)
            if isinstance(eff, list):
                modified_effects.extend(eff)
            else:
                modified_effects.append(eff)
        # find and collate zeta effects
        collated_zeta_effects = []
        for zeta_dict in zeta_dict_list:
            zeta_effects = [eff for eff in modified_effects
                            if (isinstance(eff.peffect, Increase) or isinstance(eff.peffect, Decrease))
                            and (eff.peffect.fluent.symbol == zeta_dict['name'])]
            if len(zeta_effects) == 0:
                continue
            elif len(zeta_effects) == 1:
                collated_zeta_effects.append(zeta_effects[0])
            else:
                # need to merge multiple zeta effect
                zeta_k = 0
                for z_eff in zeta_effects:
                    assert (isinstance(z_eff.peffect, Increase) or isinstance(z_eff.peffect,
                                                                              Decrease)), f"expected Increase or Decrease, got {z_eff.peffect}"
                    if isinstance(z_eff.peffect, Increase):
                        zeta_k += z_eff.peffect.expression.value
                    else:
                        zeta_k -= z_eff.peffect.expression.value
                if zeta_k == 0:
                    continue
                zeta_fluent = zeta_effects[0].peffect.fluent
                zeta_expression = NumericConstant(abs(zeta_k))
                if zeta_k > 0:
                    zeta_peffect = Increase(zeta_fluent, zeta_expression)
                else:
                    zeta_peffect = Decrease(zeta_fluent, zeta_expression)
                collated_zeta_effects.append(Effect(parameters=[], condition=conditions.Truth(), peffect=zeta_peffect))
        # build the final effect list = non-numerical-effects + numerical-non-zeta-effects + collated zeta effects
        non_numerical_effects = [eff for eff in modified_effects if
                                 not (isinstance(eff.peffect, Increase) or isinstance(eff.peffect, Decrease))]
        numerical_non_zeta_effects = [eff for eff in modified_effects
                                      if ((isinstance(eff.peffect, Increase) or isinstance(eff.peffect, Decrease))
                                          and not(eff.peffect.fluent.symbol.startswith('zeta')))]
        return non_numerical_effects + numerical_non_zeta_effects + collated_zeta_effects
    elif isinstance(obj, Effect):
        assert obj.condition == conditions.Truth() and obj.parameters == [], f'expected regular effect, got: {obj}'
        original_eff = deepcopy(obj)
        if isinstance(obj.peffect, Atom) or isinstance(obj.peffect, NegatedAtom):
            return original_eff
        elif isinstance(obj.peffect, Increase) or isinstance(obj.peffect, Decrease):
            assert isinstance(obj.peffect.expression, NumericConstant), \
                f"expected expression to be a constant, got: {obj.peffect.expression}"
            zeta_effects = []
            for zeta_dict in zeta_dict_list:
                coeff_dict = zeta_dict['coeff_dict']
                coeff = coeff_dict.get(str(obj.peffect.fluent), 0.)
                k = obj.peffect.expression.value
                if coeff != 0.:
                    new_fluent = PrimitiveNumericExpression(symbol=zeta_dict['name'], args=tuple())
                    new_expression_value = coeff * k * (1. if isinstance(obj.peffect, Increase) else -1.)
                    new_expression = NumericConstant(abs(new_expression_value))
                    if new_expression_value > 0.:
                        new_peffect = Increase(new_fluent, new_expression)
                    else:
                        new_peffect = Decrease(new_fluent, new_expression)
                    zeta_effect = Effect(parameters=[], condition=conditions.Truth(), peffect=new_peffect)
                    zeta_effects.append(zeta_effect)
                else:
                    continue
            return [original_eff] + zeta_effects
        else:
            raise NotImplemented
    elif isinstance(obj, ConstantCondition):
        return obj
    else:
        raise NotImplemented
