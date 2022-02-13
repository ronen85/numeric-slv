from copy import deepcopy

from .problem import SocialPredicate, SocialVariable


def parse_task(task):
    predicates = parse_preds_from_task(task)
    functions = parse_funcs_from_task(task)
    initial_state = deepcopy(task.init)
    numeric_initial_state = deepcopy(task.num_init)
    # sanity check

    return


def parse_preds_from_task(task):
    preds = []
    for p in task.predicates:
        p = deepcopy(p)
        name = p.name
        arguments = p.arguments
        preds.append(SocialPredicate(name, arguments))
    return preds


def parse_funcs_from_task(task):
    funcs = []
    for f in task.functions:
        f = deepcopy(f)
        name = f.name
        arguments = f.arguments
        funcs.append(SocialVariable(name, arguments))
    return funcs
