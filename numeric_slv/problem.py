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
from .ground_task import get_grounded_task, get_grounded_task_with_sas
from .remove_constants import get_constants_from_grounded_task, replace_pne_with_numeric_constants, \
    get_task_with_grounded_constants

from .task_to_pddl import get_pddl_domain, get_pddl_prob, as_pddl
from .zeta_compilation import convert_numerical_expressions_to_normal_form, \
    replace_complex_numerical_expressions_with_zeta_variables


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


def get_simplified_grounded_task(domain_filename, prob_filename):
    # grounded_task = get_grounded_task_with_sas(domain_filename, prob_filename)
    grounded_task = get_grounded_task(domain_filename, prob_filename)
    task_with_grounded_constants = get_task_with_grounded_constants(grounded_task)
    modified_grounded_task = convert_numerical_expressions_to_normal_form(task_with_grounded_constants)
    modified_grounded_task = replace_complex_numerical_expressions_with_zeta_variables(modified_grounded_task)
    return modified_grounded_task





