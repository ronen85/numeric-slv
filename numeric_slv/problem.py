import re
import string
from copy import deepcopy

from sympy.core.numbers import NegativeOne

from translate import pddl_parser
import sympy as sym
from numeric_slv import utils
from translate.pddl import Action, Atom, FunctionComparison, Effect, NegatedAtom, Increase, Decrease, \
    Conjunction, PrimitiveNumericExpression, NumericConstant, Task, FunctionAssignment, NumericEffect, Literal, \
    ArithmeticExpression, Sum, Product, Predicate, Function, conditions, TypedObject, Assign


def as_pddl(obj):
    """
    gets and obj and returns pddl as string
    """
    if isinstance(obj, Atom):
        return f'({obj.predicate} ' + ' '.join(obj.args) + ')'
    elif isinstance(obj, NegatedAtom):
        return f'(not ({obj.predicate} ' + ' '.join(obj.args) + '))'
    elif isinstance(obj, TypedObject):
        return f'{obj.name} - {obj.type_name}'
    elif isinstance(obj, Predicate):
        return '(' + obj.name + ' ' + ' '.join([f'{a.name} - {a.type_name}' for a in obj.arguments]) + ')'
    elif isinstance(obj, Function):
        return '(' + obj.name + ' ' + ' '.join([f'{a.name} - {a.type_name}' for a in obj.arguments]) + ')'
    elif isinstance(obj, Action):
        action_str = f'(:action {obj.name}\n'
        parameters_typed_objects = ' '.join([f'{as_pddl(p)}' for p in obj.parameters])
        action_str += f':parameters ({parameters_typed_objects})\n'
        action_str += f':precondition {as_pddl(obj.precondition)}\n'
        action_str += f':effects (and\n'
        for eff in obj.effects:
            action_str += f'\t{as_pddl(eff)}\n'
        action_str += '))'
        return action_str
    elif isinstance(obj, Conjunction):
        return f'(and\n\t' + '\n\t'.join([as_pddl(p) for p in obj.parts]) + ')'
    elif isinstance(obj, Effect):
        if obj.condition == conditions.Truth() and obj.parameters == []:
            return as_pddl(obj.peffect)
        else:
            raise NotImplemented
    elif isinstance(obj, Increase):
        return '(increase ' + ' '.join([as_pddl(obj.fluent), as_pddl(obj.expression)]) + ')'
    elif isinstance(obj, Decrease):
        return '(decrease ' + ' '.join([as_pddl(obj.fluent), as_pddl(obj.expression)]) + ')'
    elif isinstance(obj, PrimitiveNumericExpression):
        return f'({obj.symbol} ' + ' '.join(obj.args) + ')'
    elif isinstance(obj, NumericConstant):
        return f'{obj.value}'
    elif isinstance(obj, FunctionComparison):
        return f'({obj.comparator} ' + as_pddl(obj.parts[0]) + as_pddl(obj.parts[1]) + ')'
    elif isinstance(obj, Assign):
        return f'(= {as_pddl(obj.fluent)} {as_pddl(obj.expression)})'
    elif isinstance(obj, ArithmeticExpression):
        return f'({obj.op} ' + ' '.join([as_pddl(obj.parts[0]), as_pddl(obj.parts[0])]) + ')'
    else:
        raise NotImplemented


def get_pddl_domain(task):
    """
    gets a task and returns the pddl domain as string
    """

    def get_types_lines(types):
        type_dict = dict()
        for t in types:
            if t.basetype_name in type_dict:
                type_dict[t.basetype_name].append(t.name)
            else:
                type_dict[t.basetype_name] = [t.name]
        types_lines = []
        for key, value in type_dict.items():
            if key is None:
                continue
            types_lines.append(' '.join(value) + f' - {key}')
        return types_lines

    domain = '(define (domain ' + task.domain_name + ')\n\n'
    domain += '(:requirements  ' + ' '.join(task.requirements.requirements) + ')\n\n'
    # parse and print types
    types_lines = get_types_lines(task.types)
    domain += '(:types\n'
    for l in types_lines:
        domain += f'\t{l}\n'
    domain += ')\n\n'
    # parse and print predicates
    domain += '(:predicates\n'
    for p in task.predicates:
        if p.name == '=':
            continue
        domain += f'\t{as_pddl(p)}\n'
    domain += ')\n\n'
    # parse and print functions
    domain += '(:functions\n'
    for f in task.functions:
        domain += f'\t{as_pddl(f)}\n'
    domain += ')\n\n'
    # parse and print actions
    for a in task.actions:
        domain += f'\n{as_pddl(a)}\n'
    domain += ')'
    # print(domain)
    return domain


def get_constants_from_grounded_task(grounded_task):
    """
    gets a grounded task (with grounded actions (no parameters)) and returns a dictionary with constants
    (functions, i.e. numerical variables, that the agents' actions do not change)
    """
    assign_dict = dict([(assign.fluent, assign.expression) for assign in grounded_task.num_init])
    variables_from_init = set([a.fluent for a in grounded_task.num_init])
    variables_from_action_effects = set()
    for action in grounded_task.actions:
        for eff in action.effects:
            if isinstance(eff.peffect, Literal):
                continue
            elif isinstance(eff.peffect, FunctionAssignment):
                assert isinstance(eff.peffect.fluent, PrimitiveNumericExpression), 'expected PNE object'
                variables_from_action_effects.add(eff.peffect.fluent)
            else:
                raise NotImplemented
    constants = variables_from_init - variables_from_action_effects
    constants_dict = deepcopy(dict([(pne, assign_dict[pne]) for pne in constants]))
    return constants_dict


def get_numerical_preconditions_from_action(action: Action):
    """
    gets and action and returns a list with its numerical precondition
    """
    if isinstance(action.precondition, Atom):
        return []
    elif isinstance(action.precondition, Conjunction):
        numerical_preconditions = []
        for pre in action.precondition.parts:
            if isinstance(pre, Atom):
                continue
            elif isinstance(pre, FunctionComparison):
                numerical_preconditions.append(pre)
            else:
                raise NotImplemented
    return numerical_preconditions


def replace_punctuation(s, replace=' '):
    """
    replaces punctuation (/*-+...) with 'replace'
    """
    chars = re.escape(string.punctuation)
    return re.sub(r'[' + chars + ']', replace, s)


def get_grounded_action_signatures_from_sas_list(sas_as_list: list):
    """
    gets a sas file as list and returns action signature
    e.g. move truck0 loc1 loc2
    """
    sas_list = deepcopy(sas_as_list)
    action_signatures = []
    for idx, l in enumerate(sas_list):
        if l.strip() == 'begin_operator':
            action_signatures.append(sas_list[idx + 1].strip())
    return action_signatures


def ground_obj_with_dict(obj, type_dict):
    """
    gets an object (e.g. FunctionAssignment) and replaces its arguments with the info in the type dictionary
    """
    grounded_obj = deepcopy(obj)
    if hasattr(grounded_obj, 'parts') and (len(grounded_obj.parts) > 0) and (not hasattr(grounded_obj, 'args')):
        grounded_obj.parts = [ground_obj_with_dict(p, type_dict) for p in grounded_obj.parts]
        return grounded_obj
    elif hasattr(grounded_obj, 'args') and ((not hasattr(grounded_obj, 'parts')) or (len(grounded_obj.parts) == 0)):
        grounded_obj.args = tuple(type_dict[a] for a in grounded_obj.args)
        return grounded_obj
    elif isinstance(grounded_obj, NumericConstant):
        return grounded_obj
    elif isinstance(grounded_obj, Effect):
        if grounded_obj.parameters:
            raise NotImplemented
        grounded_obj.peffect = ground_obj_with_dict(grounded_obj.peffect, type_dict)
        return grounded_obj
    elif isinstance(grounded_obj, FunctionAssignment):
        grounded_obj.fluent = ground_obj_with_dict(grounded_obj.fluent, type_dict)
        grounded_obj.expression = ground_obj_with_dict(grounded_obj.expression, type_dict)
        return grounded_obj
    elif isinstance(grounded_obj, PrimitiveNumericExpression):
        grounded_obj.args = tuple(type_dict[a] for a in grounded_obj.args)
        return grounded_obj
    elif isinstance(grounded_obj, NumericEffect):
        grounded_obj.effect = ground_obj_with_dict(grounded_obj.effect, type_dict)
        return grounded_obj
    else:
        raise NotImplemented


def get_grounded_task(domain_filename, prob_filename):
    """
    gets a path to pddl file and prob
    gets its action signatures from sas translation (using fast downward)
    replaces lifted actions with grounded ones
    returns Task
    """

    def get_rel_action_from_task(action_name, task):
        alist = [a for a in task.actions if a.name == action_name]
        assert len(alist) == 1
        return deepcopy(alist[0])

    task = pddl_parser.open_pddl(domain_filename, prob_filename)
    sas_as_list = utils.get_sas_translation(domain_filename, prob_filename)

    grounded_task = deepcopy(task)
    grounded_task.domain_name = '_'.join([task.domain_name, task.task_name, 'grounded'])
    grounded_task.task_name = '_'.join([task.task_name, 'grounded'])
    # ground actions
    action_signatures = get_grounded_action_signatures_from_sas_list(sas_as_list)
    grounded_actions = []
    for signature in action_signatures:
        signature_as_list = signature.split()
        action_name = signature_as_list[0]
        lifted_action = get_rel_action_from_task(action_name, task)
        type_dict = dict([(x.name, value) for x, value in zip(lifted_action.parameters, signature_as_list[1:])])
        name = '_'.join(signature_as_list)
        parameters = []
        num_external_parameters = 0
        precondition = ground_obj_with_dict(lifted_action.precondition, type_dict)
        effects = [ground_obj_with_dict(e, type_dict) for e in lifted_action.effects]
        cost = ground_obj_with_dict(lifted_action.cost, type_dict)
        grounded_action = Action(name, parameters, num_external_parameters, precondition, effects, cost)
        grounded_actions.append(grounded_action)
    grounded_task.actions = grounded_actions
    return grounded_task


def replace_pne_with_numeric_constants(obj, constants_dict):
    """
    gets an object (e.g. Action, Conjunction) and a dictionary with constants information
    and returns the same object with constants (instead of numeric expressions)
    """
    if isinstance(obj, Task):
        modified_task = deepcopy(obj)
        modified_task.actions = [replace_pne_with_numeric_constants(a, constants_dict) for a in modified_task.actions]
        return modified_task
    elif isinstance(obj, Action):
        modified_action = deepcopy(obj)
        modified_action.precondition = replace_pne_with_numeric_constants(modified_action.precondition, constants_dict)
        modified_action.effects = [replace_pne_with_numeric_constants(eff, constants_dict) for eff in
                                   modified_action.effects]
        return modified_action
    elif isinstance(obj, Conjunction):
        modified_conjunction = deepcopy(obj)
        modified_conjunction.parts = [replace_pne_with_numeric_constants(p, constants_dict) for p in
                                      modified_conjunction.parts]
        return modified_conjunction
    elif isinstance(obj, Literal):
        return deepcopy(obj)
    elif isinstance(obj, FunctionComparison):
        modified_comparison = deepcopy(obj)
        modified_comparison.parts = [replace_pne_with_numeric_constants(p, constants_dict) for p in
                                     modified_comparison.parts]
        return modified_comparison
    elif isinstance(obj, ArithmeticExpression):
        modified_expression = deepcopy(obj)
        modified_expression.parts = [replace_pne_with_numeric_constants(p, constants_dict) for p in
                                     modified_expression.parts]
        return modified_expression
    elif isinstance(obj, Effect):
        modified_eff = deepcopy(obj)
        modified_eff.peffect = replace_pne_with_numeric_constants(modified_eff.peffect, constants_dict)
        return modified_eff
    elif isinstance(obj, FunctionAssignment):
        f_assignment = deepcopy(obj)
        assert isinstance(f_assignment.fluent,
                          PrimitiveNumericExpression), f'expected a PNE, got: {f_assignment.fluent}'
        f_assignment.expression = replace_pne_with_numeric_constants(f_assignment.expression, constants_dict)
        return f_assignment
    elif isinstance(obj, PrimitiveNumericExpression):
        return constants_dict[obj] if obj in constants_dict.keys() else deepcopy(obj)
    elif isinstance(obj, NumericConstant):
        return deepcopy(obj)
    else:
        raise NotImplemented


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


def get_pddl_prob(task):
    """
    gets a task and returns the pddl problem as a string
    """
    prob = f'(define (problem {task.task_name}) (domain {task.domain_name})\n\n'
    prob += '(:objects\n' + '\n\t'.join([as_pddl(o) for o in task.objects]) + ')\n\n'
    prob += '(:init\n'
    for i in task.init:
        if i.predicate == '=':
            continue
        prob += '\t' + as_pddl(i) + '\n'
    for i in task.num_init:
        prob += '\t' + as_pddl(i) + '\n'
    prob += ')\n\n'
    prob += '(:goal ' + as_pddl(task.goal) + ')\n\n'
    if len(task.metric) == 2 and task.metric[0] in '<>':
        prob += f'(:metric '
        prob += 'minimize ' if (task.metric[0] == '<') else 'maximize '
        prob += as_pddl(task.metric[1]) + ')\n\n'
    prob += ')'
    # print(prob)
    return prob


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
        zeta_cnt = 0
        zeta_dict_list = []
        for action in modified_task.actions:
            if isinstance(action.precondition, Conjunction):
                for pre in action.precondition.parts:
                    if isinstance(pre, Atom):
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
            else:
                raise NotImplemented
        return zeta_dict_list

    if isinstance(obj, Task):
        assert zeta_dict_list == [], f'expected empty list, got: {zeta_dict_list}'
        assert num_init_list == [], f'expected empty list, got: {zeta_dict_list}'
        modified_task = deepcopy(obj)
        num_init_list = [str(v.fluent) for v in obj.num_init]
        zeta_dict_list = get_zeta_dict_list(
            modified_task)  # compute zeta_dict_list: a list of dictionaries with data on needed zeta variables
        # add zeta variables to domain variables
        for z_dict in zeta_dict_list:
            function = Function(z_dict['name'], [], 'number')
            modified_task.functions.append(function)
        # modify actions
        modified_actions = []
        for action in obj.actions:
            mod_action = replace_complex_numerical_expressions_with_zeta_variables(action, zeta_dict_list, num_init_list)
            modified_actions.append(mod_action)
        modified_task.actions = modified_task
        # modify initial state
        zeta_num_init = []
        str_num_init_list = [str(a.fluent) for a in obj.num_init]
        for z_dict in zeta_dict_list:
            zeta_fluent = PrimitiveNumericExpression(symbol=z_dict['name'], args=tuple())
            zeta_initial_value = .0
            coeff_dict = z_dict['coeff_dict']
            for coeff in  coeff_dict.keys():
                idx = str_num_init_list.index(coeff)
                k = obj.num_init[idx].expression.value
                zeta_initial_value += coeff_dict[coeff] * k
            zeta_assign = Assign(fluent=zeta_fluent, expression=NumericConstant(zeta_initial_value))
            zeta_num_init.append(zeta_assign)
        modified_task.num_init.extend(zeta_num_init)
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
    elif isinstance(obj, Atom):
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
                    new_expression = NumericConstant(coeff * k)
                    new_peffect = Increase(new_fluent, new_expression) if isinstance(obj.peffect, Increase) else Decrease(new_fluent, new_expression)
                    zeta_effect = Effect(parameters=[], condition=conditions.Truth(), peffect=new_peffect)
                    zeta_effects.append(zeta_effect)
                else:
                    continue
            return [original_eff] + zeta_effects
        else:
            raise NotImplemented

    else:
        raise NotImplemented


def get_simplified_grounded_task(domain_filename, prob_filename):
    grounded_task = get_grounded_task(domain_filename, prob_filename)
    # get constants
    constants_dict = get_constants_from_grounded_task(grounded_task)
    # modify task - replace numeric expressions with numeric constants
    modified_grounded_task = replace_pne_with_numeric_constants(grounded_task, constants_dict)
    # modify task - convert numerical expressions to normal form
    modified_grounded_task = convert_numerical_expressions_to_normal_form(modified_grounded_task)
    # find and replaces complex numerical expressions and create new zeta variables
    domain = get_pddl_domain(modified_grounded_task)
    modified_grounded_task = replace_complex_numerical_expressions_with_zeta_variables(modified_grounded_task)

    prob = get_pddl_prob(modified_grounded_task)
    # find all numerical preconditions
    num_precondition_list = []
    for action in grounded_task.actions:
        num_precondition_list.extend(get_numerical_preconditions_from_action(action))
    print()

    # add new variables \zeta = w_1 * v_1 + ... + w_n * v_n >= v_0
    # update actions accordingly
    # update num init accordingly
    # update num goal accordingly
    pass


class SocialPlanningProblem:

    def __init__(self, domain_filename, prob_filename):
        self.domain_filename, self.prob_filename = domain_filename, prob_filename
        # self.task = pddl_parser.open_pddl(domain_filename, prob_filename)
        # self.sas_as_list = utils.get_sas_translation(domain_filename, prob_filename)
        # self.grounded_task = get_grounded_task(domain_filename, prob_filename)
        self.simplify_grounded_task = get_simplified_grounded_task(domain_filename, prob_filename)
        self.domain_name = self.grounded_task.domain_name
        self.problem_name = self.grounded_task.task_name

    # def get_grounded_predicates_from_sas_list(self):
    #     sas_list = deepcopy(self.sas_as_list)
    #     rel_lines = filter(lambda x: x.startswith('Atom'), sas_list)
    #     rel_lines = filter(lambda x: 'axiom' not in x, rel_lines)
    #     atoms = [replace_punctuation(l.strip().replace('Atom ', '')) for l in rel_lines]
    #     predicates = []
    #     for a in atoms:
    #         atom_as_list = a.split()
    #         name = atom_as_list[0]
    #         args = [] if len(a) == 1 else atom_as_list[1:]
    #         predicates.append(SocialPredicate(name, args))
    #     return predicates

    def get_predicates(self):
        predicates = []
        for pred in self.task.predicates:
            if pred.name == '=':
                # the translator creates fake predicates named '='
                continue
            predicates.append(SocialPredicate(pred.name, pred.arguments))
        return predicates

    def get_variables(self):
        vars = []
        for v in self.task.functions:
            vars.append(SocialVariable(v.name, v.arguments))
        return vars

    def get_init(self):
        return deepcopy(self.task.init)

    def get_num_init(self):
        return deepcopy(self.task.num_init)

    def get_actions(self):
        def get_rel_action_from_task(action_name):
            alist = [a for a in self.task.actions if a.name == action_name]
            assert len(alist) == 1
            return alist[0]

        def get_action_from_signature(signature):
            signature_as_list = signature.split()
            rel_action = get_rel_action_from_task(signature_as_list[0])
            type_dict = dict([(x.name, value) for x, value in zip(rel_action.parameters, signature_as_list[1:])])
            action_name = '_'.join(signature_as_list)
            pre = []
            num_pre = []
            new_variables = []
            for part in rel_action.precondition.parts:
                if isinstance(part, Atom):
                    name = part.predicate
                    args = tuple(type_dict[a] for a in part.args)
                    grounded_atom = Atom(name, args)
                    pre.append(grounded_atom)
                elif isinstance(part, FunctionComparison):
                    new_variable_idx = len(new_variables)
                    variable_name = '_'.join([action_name, 'pre', str(new_variable_idx)])
                    print()
                else:
                    raise NotImplemented

        grounded_action_signatures = self.get_grounded_grounded_action_signatures_from_sas_list()
        for signature in grounded_action_signatures:
            action = get_action_from_signature(signature)

    def compile_numericals(self):

        def get_all_numerical_preconditions(actions, numerical_vars=[]):

            def get_numerical_preconditions_from_action(action):
                if isinstance(action.precondition, Atom):
                    return []
                elif isinstance(action.precondition, Conjunction):
                    numerical_preconditions = []
                    for pre in action.precondition.parts:
                        if isinstance(pre, Atom):
                            continue
                        elif isinstance(pre, FunctionComparison):
                            numerical_preconditions.append(pre)
                        else:
                            raise NotImplemented
                return numerical_preconditions

            action = actions.pop()

            if actions:
                return get_all_numerical_preconditions(actions,
                                                       numerical_vars + get_numerical_preconditions_from_action(action))
            else:
                return numerical_vars + get_numerical_preconditions_from_action(action)

        numerical_preconditions = get_all_numerical_preconditions(deepcopy(self.task.actions))
        linear_expresions = []
        for npre in numerical_preconditions:
            linear_expresions.append(LinearPrecondition.parse_from_object(npre))

        print()


class LinearPrecondition:
    def __init__(self, w: list, v: list, v_0):
        assert len(w) == len(v), "v and w should be with the same left"
        self.w = w
        self.v = v
        self.v_0 = v_0

    def __repr__(self):
        return f"<LinearPrecondition: v:{self.v}  w:{self.w}>"

    @staticmethod
    def parse_from_object(obj):

        def tree_to_list(tree):
            if tree.parts:
                left = tree.parts[0]
                right = tree.parts[1]
                op = tree.op
                return tree_to_list(left) + [op] + tree_to_list(right)
            else:
                return [tree]

        if isinstance(obj, FunctionComparison):
            w_hat, v_hat, v_0 = [], [], None
            left = tree_to_list(obj.parts[0])
            right = tree_to_list(obj.parts[1])
            assert len(right) == 1, f'right: {right} is expected to be a 1-obj list'
            assert isinstance(right[0], NumericConstant) == 1, f'right: {right} is expected to be a 1-obj list'
            w = 1
            while left:
                element = left.pop(0)
                if isinstance(element, PrimitiveNumericExpression):
                    assert w is not None, f'w: {w} should not be None'
                    w_hat.append(w)
                    v_hat.append(element)
                    w = None
                elif isinstance(element, str) and (element in ['+', '-']):
                    w = 1 if element == '+' else -1
                else:
                    raise NotImplemented
            v_0 = right[0].value
            return LinearPrecondition(w_hat, v_hat, v_0)
        else:
            raise NotImplemented


class SocialPredicate:
    def __init__(self, name, arguments):
        self.name = name  # str
        self.arguments = arguments  # list of TypedObject

    def __str__(self):
        return f"Predicate: {self.name} ({', '.join(map(str, self.arguments))})"


class SocialVariable:
    def __init__(self, name, arguments):
        self.name = name  # str
        self.arguments = arguments  # list of TypedObject

    def __str__(self):
        return f"Function: {self.name} ({', '.join(map(str, self.arguments))})"


class SocialNumericInitialState:
    pass


class SocialAction:

    def __init__(self, name='', pre=[]):
        self.name = ''
        self.pre = []
        self.num_pre = []
        self.add_eff = []
        self.del_eff = []
        self.num_eff = []


class SocialPropositionalGoal:
    pass


class SocialNumericGoal:
    pass
