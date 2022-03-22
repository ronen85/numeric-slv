from copy import deepcopy

from translate.pddl import FunctionAssignment, Literal, PrimitiveNumericExpression, Task, Action, Conjunction, \
    FunctionComparison, ArithmeticExpression, Effect, NumericConstant


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

def replace_pne_with_numeric_constants(obj, constants_dict):
    """
    gets an object (e.g. Action, Conjunction) and a dictionary with constants information
    and returns the same object with constants (instead of numeric expressions)
    """
    if isinstance(obj, Task):
        modified_task = deepcopy(obj)
        modified_task.num_init = [a for a in modified_task.num_init if not(a.fluent in constants_dict.keys())]
        modified_task.actions = [replace_pne_with_numeric_constants(a, constants_dict) for a in modified_task.actions]
        symbol_list = [a.fluent.symbol for a in modified_task.num_init]
        modified_task.functions = [f for f in modified_task.functions if f.name in symbol_list]
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
        assert isinstance(f_assignment.fluent, PrimitiveNumericExpression), \
            f'expected a PNE, got: {f_assignment.fluent}'
        f_assignment.expression = replace_pne_with_numeric_constants(f_assignment.expression, constants_dict)
        if not isinstance(f_assignment.expression, NumericConstant):
            raise NotImplemented
        elif f_assignment.expression.value < 0.:
            raise NotImplemented
        return f_assignment
    elif isinstance(obj, PrimitiveNumericExpression):
        return constants_dict[obj] if obj in constants_dict.keys() else deepcopy(obj)
    elif isinstance(obj, NumericConstant):
        return deepcopy(obj)
    else:
        raise NotImplemented


def get_task_with_grounded_constants(grounded_task):
    # get constants
    constants_dict = get_constants_from_grounded_task(grounded_task)
    # modify task - replace numeric expressions with numeric constants
    modified_grounded_task = replace_pne_with_numeric_constants(grounded_task, constants_dict)
    return modified_grounded_task