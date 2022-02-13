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
from .ground_task import get_grounded_task
from .remove_constants import get_constants_from_grounded_task, replace_pne_with_numeric_constants, \
    get_task_with_grounded_constants

from .task_to_pddl import get_pddl_domain, get_pddl_prob, as_pddl





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
    task_with_grounded_constants = get_task_with_grounded_constants(grounded_task)

    # modify task - convert numerical expressions to normal form
    modified_grounded_task = convert_numerical_expressions_to_normal_form(task_with_grounded_constants)
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
