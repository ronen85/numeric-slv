from copy import deepcopy
from itertools import product

from numeric_slv import utils
from translate import pddl_parser
from translate.pddl import NumericConstant, Effect, FunctionAssignment, PrimitiveNumericExpression, NumericEffect, \
    Action, Type


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


def get_grounded_task_with_sas(domain_filename, prob_filename):
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


def get_type_dict_from_task(task):
    """
    input: task
    output: type dictionary where keys are type names and values are set of the type and its children types
    e.g.
    {'object': set(['object', 'agent', 'edible']), ....]
    """
    type_dict = dict([(t.name, set()) for t in task.types])
    for t in task.types:
        type_dict[t.name].add(t.name)
        for super_type in t.supertype_names:
            type_dict[super_type].add(t.name)
    return type_dict


def get_grounded_action_signatures_from_task(task):
    type_dict = get_type_dict_from_task(task)
    action_signatures = set()
    for action in task.actions:
        action_name = action.name
        objects = []
        for p in action.parameters:
            possible_objects = [o for o in task.objects if o.type_name in type_dict[p.type_name]]
            objects.append(possible_objects)
        for param in product(*objects):
            action_signatures.add(' '.join([action_name] + [p.name for p in param]))
    return action_signatures


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
    # sas_as_list = utils.get_sas_translation(domain_filename, prob_filename)

    grounded_task = deepcopy(task)
    grounded_task.domain_name = '_'.join([task.domain_name, task.task_name, 'grounded'])
    grounded_task.task_name = '_'.join([task.task_name, 'grounded'])
    # ground actions
    action_signatures = get_grounded_action_signatures_from_task(task)
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
