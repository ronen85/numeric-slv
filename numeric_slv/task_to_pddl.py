from translate.pddl import Atom, NegatedAtom, TypedObject, Predicate, Function, Action, Conjunction, conditions, \
    Increase, Decrease, PrimitiveNumericExpression, NumericConstant, FunctionComparison, Assign, ArithmeticExpression, \
    Effect


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