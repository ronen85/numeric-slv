import argparse
import json
import pandas as pd
from copy import deepcopy

from numeric_slv import SocialPlanningProblem
from numeric_slv.zeta_compilation import is_function_comparison_simple
from translate.pddl import Predicate, Atom, Conjunction, NegatedAtom, FunctionComparison, PrimitiveNumericExpression, \
    Action, Literal, Effect, NumericConstant, Function, Assign, Increase, Decrease, Disjunction, Task


def str_eq(arg1, arg2):
    return arg1 == arg2 or '*' in [arg1, arg2]


def str_list_eq(arg_list_1, arg_list_2):
    if len(arg_list_1) != len(arg_list_2):
        return False
    elif arg_list_1 == [] and arg_list_2 == []:
        return True
    else:
        return str_eq(arg_list_1[0], arg_list_2[0]) and str_list_eq(arg_list_1[1:], arg_list_2[1:])


def get_pre_p_w_from_action(action: Action, waitfor_list):
    # get all relevant waitfor dictionaries from waitfor_list
    action_str_list = action.name.split('_')
    rel_waitfor_list = []
    for wfd in waitfor_list:
        wfd_str_list = [wfd['action_name']] + wfd['action_args']
        if str_list_eq(action_str_list, wfd_str_list):
            rel_waitfor_list.append(wfd)
    # return the relevant atoms
    if rel_waitfor_list == []:
        return []
    else:
        pre_p_list = get_pre_p_from_action(action)
        pre_p_w = []
        wfd_str_list = [[d['predicate_name']] + d['predicate_args'] for d in rel_waitfor_list]
        for atom in pre_p_list:
            atom_str_list = [atom.predicate] + list(atom.args)
            if True in [str_list_eq(atom_str_list, wfd_str) for wfd_str in wfd_str_list]:
                pre_p_w.append(atom)
        return pre_p_w


def get_pre_n_w_from_action(action, num_waitfor):
    # get all relevant waitfor dictionaries from waitfor_list
    action_str_list = action.name.split('_')
    rel_waitfor_list = []
    for wfd in num_waitfor:
        wfd_str_list = [wfd['action_name']] + wfd['action_args']
        if str_list_eq(action_str_list, wfd_str_list):
            rel_waitfor_list.append(wfd)
    # return the relevant atoms
    if rel_waitfor_list == []:
        return []
    else:
        pre_n_list = get_pre_n_from_action(action)
        pre_n_w = []
        wfd_str_list = [[d['fluent_name']] + d['fluent_args'] for d in rel_waitfor_list]
        for fc in pre_n_list:
            assert is_function_comparison_simple(fc), f"expected a simple function comparison, got {fc}"
            fc_str_list = [fc.parts[0].symbol] + list(fc.parts[0].args)
            if True in [str_list_eq(fc_str_list, wfd_str) for wfd_str in wfd_str_list]:
                pre_n_w.append(fc)
        return pre_n_w
    pass


def get_action_precondition_as_list(a: Action):
    assert isinstance(a, Action), f'expected an action, got {a}'
    if isinstance(a.precondition, Atom):
        return [a.precondition]
    elif isinstance(a.precondition, Conjunction):
        return a.precondition.parts
    else:
        raise NotImplemented


def get_global_copy(obj):
    return get_local_copy(obj, 'g')


def get_local_copy(obj, agent_name: str):
    assert isinstance(agent_name, str), f'expected a str, got {agent_name}'
    if isinstance(obj, Literal):
        literal_i = deepcopy(obj)
        literal_i.predicate += '_' + agent_name
        return literal_i
    elif isinstance(obj, Predicate):
        pred_i = deepcopy(obj)
        pred_i.name += '_' + agent_name
        return pred_i
    elif isinstance(obj, FunctionComparison):
        left, right = obj.parts
        assert isinstance(left, PrimitiveNumericExpression) and isinstance(right, NumericConstant)
        new_left = get_local_copy(left, agent_name)
        func = deepcopy(obj)
        func.parts = new_left, right
        return func
    elif isinstance(obj, PrimitiveNumericExpression):
        pne = deepcopy(obj)
        pne.symbol += '_' + agent_name
        return pne
    elif isinstance(obj, Function):
        f = deepcopy(obj)
        f.name += '_' + agent_name
        return f
    elif isinstance(obj, Assign):
        a = deepcopy(obj)
        a.fluent = PrimitiveNumericExpression(symbol=a.fluent.symbol + f'_{agent_name}', args=a.fluent.args)
        return a
    elif isinstance(obj, Effect):
        eff = deepcopy(obj)
        eff.peffect = get_local_copy(eff.peffect, agent_name)
        return eff
    elif isinstance(obj, Increase) or isinstance(obj, Decrease):
        num_eff = deepcopy(obj)
        num_eff.fluent = get_local_copy(num_eff.fluent, agent_name)
        return num_eff
    else:
        raise NotImplemented


def get_pre_p_from_action(action: Action):
    pre_list = get_action_precondition_as_list(action)
    pre_p_list = []
    for pre in pre_list:
        if isinstance(pre, Atom):
            pre_p_list.append(pre)
        elif isinstance(pre, FunctionComparison):
            continue
        else:
            raise NotImplemented
    return pre_p_list


def get_pre_n_from_action(action):
    pre_list = get_action_precondition_as_list(action)
    pre_n_list = []
    for pre in pre_list:
        if isinstance(pre, FunctionComparison):
            pre_n_list.append(pre)
        elif isinstance(pre, Atom):
            continue
        else:
            raise NotImplemented
    return pre_n_list


def get_waiting_predicate(name: str):
    return Predicate(name='waiting_' + name, arguments=[])


def get_waiting_atom(name: str):
    return predicate_to_atom(get_waiting_predicate(name))


def get_wt_f_predicate(obj):
    if isinstance(obj, Atom):
        return Predicate(name='_'.join(['wt', obj.predicate] + list(obj.args)), arguments=[])
    elif isinstance(obj, Predicate):
        return Predicate(name='_'.join(['wt', obj.name] + list(obj.arguments)), arguments=[])
    else:
        raise NotImplemented


def get_wt_f_atom(obj):
    pred = get_wt_f_predicate(obj)
    return Atom(predicate=pred.name, args=[])


def get_add_from_action(action):
    add = []
    for eff in action.effects:
        assert isinstance(eff, Effect), f"expected Effect, got: {eff}"
        if isinstance(eff.peffect, Atom):
            add.append(eff)
    return add


def get_del_from_action(action):
    del_list = []
    for eff in action.effects:
        assert isinstance(eff, Effect), f"expected Effect, got: {eff}"
        if isinstance(eff.peffect, NegatedAtom):
            del_list.append(eff)
    return del_list


def get_wt_v_w_predicate(fc: FunctionComparison):
    if isinstance(fc, FunctionComparison):
        v = '_'.join([fc.parts[0].symbol] + list(fc.parts[0].args))
        w = str(fc.parts[1].value)
        return Predicate(name='_'.join(['wt', v, w]), arguments=[])
    else:
        raise NotImplemented


def get_wt_v_w_atom(fc: FunctionComparison):
    return predicate_to_atom(get_wt_v_w_predicate(fc))


def get_act_predicate():
    return Predicate(name='act', arguments=[])


def get_failure_predicate():
    return Predicate(name='failure', arguments=[])


def get_fin_predicate(agent_name):
    return Predicate(name='fin_' + agent_name, arguments=[])


def get_failure_atom():
    return predicate_to_atom(get_failure_predicate())


def get_fin_atom(name):
    return predicate_to_atom(get_fin_predicate(name))


def predicate_to_atom(p: Predicate):
    name = p.name
    args = p.arguments
    return Atom(predicate=name, args=args)


def get_act_atom():
    return predicate_to_atom(get_act_predicate())


def get_num_eff_from_action(action):
    num_eff = []
    for eff in action.effects:
        if isinstance(eff.peffect, Atom) or isinstance(eff.peffect, NegatedAtom):
            continue
        elif isinstance(eff.peffect, Increase) or isinstance(eff.peffect, Decrease):
            num_eff.append(eff)
        else:
            raise NotImplemented
    return num_eff


class Compilation:

    def __init__(self, spp, waitfor_file=''):
        self.spp = deepcopy(spp)
        if waitfor_file:
            with open(waitfor_file, 'rb') as f:
                json_file = json.load(f)
                self.waitfor = json_file.get('waitfor', dict())
                self.num_waitfor = json_file.get('num_waitfor', dict())
        self.sanity_check()
        self.action_df = self.get_action_df()
        self.agent_names_list = [o.name for o in self.spp.task.objects if o.type_name == 'agent']
        self.compiled_task = self.compile_spp()
        print()

    def compile_spp(self):
        """
        implementation of the compilation in '''Automated Verification of Social Laws in Numeric Settings'''
        """

        def get_F():
            # global copies of f
            f_g_list = []
            for pred in task.predicates:
                if pred.name == '=':
                    continue
                f_g_list.append(get_global_copy(pred))
            # agent copies of f
            f_i_list = []
            for a in agents:
                for pred in task.predicates:
                    if pred.name == '=':
                        continue
                    f_i_list.append(get_local_copy(pred, a.name))
            # waiting_i
            waiting_i_list = []
            for a in agents:
                waiting_i_list.append(get_waiting_predicate(a.name))
            # wt.f, i.e., there's an agent that is waiting for f for every f in U_a pre_w(a)
            wt_f_list = []
            for action in grounded_task.actions:
                pre_p_w = get_pre_p_w_from_action(action, self.waitfor)
                for atom in pre_p_w:
                    wt_f_list.append(get_wt_f_predicate(atom))
            wt_f_list = list(set(wt_f_list))
            # wt.v.w, i.e., there's an agent that is waiting for v >= w
            wt_v_w_list = []
            for action in grounded_task.actions:
                pre_n_w = get_pre_n_w_from_action(action, self.num_waitfor)
                for fc in pre_n_w:
                    wt_v_w_list.append(get_wt_v_w_predicate(fc))
            wt_v_w_list = list(set(wt_v_w_list))
            # act
            act_predicate = get_act_predicate()
            # failure
            failure_predicate = get_failure_predicate()
            # fin_i
            fin_i_list = []
            for a in agents:
                fin_i_list.append(get_fin_predicate(a.name))
            # F
            F = f_g_list + f_i_list + waiting_i_list + wt_f_list + wt_v_w_list + fin_i_list + [act_predicate,
                                                                                               failure_predicate]
            return F

        def get_V():
            # v_g
            v_g_list = []
            for v in grounded_task.functions:
                v_g_list.append(get_global_copy(v))
            # v_i
            v_i_list = []
            for a in agents:
                for v in grounded_task.functions:
                    v_i_list.append(get_local_copy(v, a.name))
            V = v_g_list + v_i_list
            return V

        def get_I_p():
            # I_p
            # act
            act_predicate = get_act_predicate()
            # f_g
            init_g_list = []
            for i in grounded_task.init:
                init_g_list.append(get_global_copy(i))
            # f_i
            init_i_list = []
            for a in agents:
                for pred in grounded_task.init:
                    init_i_list.append(get_local_copy(pred, a.name))
            I_p = [act_predicate] + init_g_list + init_i_list
            return I_p

        def get_I_v():
            # I_v
            # v_g
            v_g_list = []
            for v in grounded_task.num_init:
                v_g_list.append(get_global_copy(v))
            # v_i
            v_i_list = []
            for a in agents:
                for v in grounded_task.num_init:
                    v_i_list.append(get_local_copy(v, a.name))
            I_v = v_g_list + v_i_list
            return I_v

        def get_G():
            goal_parts = []
            # failure
            goal_parts.append(get_failure_atom())
            # fin_i
            for ag in agents:
                goal_parts.append(get_fin_atom(ag.name))
            G = Conjunction(tuple(goal_parts))
            return G

        def get_a_s(action):
            agent_name = action.name.split('_')[1]
            # pre_p
            pre_p = []
            pre_p.append(get_act_atom())  # act
            pre_p.append(get_waiting_atom(agent_name).negate())  # not waiting_i
            # f_i \and f_g forall f \in pre_p(a_i)
            a_pre_p = get_pre_p_from_action(action)
            for pre in a_pre_p:
                pre_i = get_local_copy(pre, agent_name)
                pre_g = get_global_copy(pre)
                pre_p.extend([pre_i, pre_g])
            # not wt.f for f in add(a)
            add_list = get_add_from_action(action)
            for eff in add_list:
                wt_atom = get_wt_f_atom(eff.peffect)
                pre_p.append(wt_atom.negate())
            # pre_n
            pre_n = []
            # v_i >= w \and v_g >= w for all v,w in pre_n(a)
            a_pre_n = get_pre_n_from_action(action)
            for func in a_pre_n:
                func_i = get_local_copy(func, agent_name)
                func_g = get_global_copy(func)
                pre_n.extend([func_i, func_g])
            # \not wt.v.w \or v \smalle w - k for all (v,k) \in num(a), (v,w) \in
            num_eff_list = get_num_eff_from_action(action)
            for num_eff in num_eff_list:
                rel_num_waitfor_list = [fc for fc in all_pre_n_w if fc.parts[0] == num_eff.peffect.fluent]
                for num_waitfor in rel_num_waitfor_list:
                    v = num_eff.peffect.fluent
                    k = num_eff.peffect.expression
                    w = num_waitfor.parts[1]
                    # \not wt.v.w
                    p1 = get_wt_v_w_atom(num_waitfor).negate()
                    # v \smaller w - k
                    comparator = '<'
                    fc_part_0 = v
                    fc_part_1 = NumericConstant(w.value - k.value)
                    p2 = FunctionComparison('<', [fc_part_0, fc_part_1])
                    pre_n.append(Disjunction([p1, p2]))
            pre = Conjunction(pre_p + pre_n)
            # add
            add_list = []
            for eff in get_add_from_action(action):
                add_list.append(get_global_copy(eff))
                add_list.append(get_local_copy(eff, agent_name))
            # del
            del_list = []
            for eff in get_del_from_action(action):
                del_list.append(get_global_copy(eff))
                del_list.append(get_local_copy(eff, agent_name))
            # num
            num_list = []
            for num_eff in get_num_eff_from_action(action):
                num_list.append(get_local_copy(num_eff, agent_name))
                num_list.append(get_global_copy(num_eff))
            # Action
            action_s = Action(name=action.name + f'_s_{agent_name}', parameters=action.parameters,
                              num_external_parameters=action.num_external_parameters, precondition=pre,
                              _effects=add_list + del_list + num_list, cost=action.cost)
            return action_s

        def get_a_p(action):
            agent_name = action.name.split('_')[1]
            # pre_p
            pre_p = []
            pre_p.append(get_act_atom())  # act
            pre_p.append(get_waiting_atom(agent_name).negate())  # not waiting_i
            # f_i for all f \in pre_p(a_i)
            a_pre_p = get_pre_p_from_action(action)
            for pre in a_pre_p:
                pre_i = get_local_copy(pre, agent_name)
                pre_p.append(pre_i)
            # f_g for all f \in pre_w_p(a_i)
            a_pre_w_p = get_pre_p_w_from_action(action, self.waitfor)
            for pre in a_pre_w_p:
                pre_g = get_global_copy(pre)
                pre_p.append(pre_g)
            # exists \not f_g for f \in {pre_p / pre_w_p} s.t
            not_f_g = []
            for pre in list(set(a_pre_p) - set(a_pre_w_p)):
                not_f_g.append(get_global_copy(pre).negate())
            pre_p.append(Disjunction(not_f_g))
            # pre_n
            pre_n = []
            # v_i >= w for all v,w in pre_n(a)
            a_pre_n = get_pre_n_from_action(action)
            for func in a_pre_n:
                func_i = get_local_copy(func, agent_name)
                pre_n.append(func_i)
            # v_g >= w for all v,w in pre_w_n(a)
            a_pre_w_n = get_pre_n_w_from_action(action, self.num_waitfor)
            for func in a_pre_w_n:
                func_g = get_global_copy(func)
                pre_n.append(func_g)
            pre = Conjunction(pre_p + pre_n)
            # add
            add_list = []
            for eff in get_add_from_action(action):
                add_list.append(get_local_copy(eff, agent_name))
            add_list.append(get_failure_atom())
            # del
            del_list = []
            for eff in get_del_from_action(action):
                del_list.append(get_local_copy(eff, agent_name))
            # num
            num_list = []
            for num_eff in get_num_eff_from_action(action):
                num_list.append(get_local_copy(num_eff, agent_name))
            # Action
            action_p = Action(name=action.name + f'_p_{agent_name}', parameters=action.parameters,
                              num_external_parameters=action.num_external_parameters, precondition=pre,
                              _effects=add_list + del_list + num_list, cost=action.cost)
            return action_p

        def get_a_n(action):
            agent_name = action.name.split('_')[1]
            # pre_p
            pre_p = []
            pre_p.append(get_act_atom())  # act
            pre_p.append(get_waiting_atom(agent_name).negate())  # not waiting_i
            # f_i for all f \in pre_p(a_i)
            a_pre_p = get_pre_p_from_action(action)
            for pre in a_pre_p:
                pre_i = get_local_copy(pre, agent_name)
                pre_p.append(pre_i)
            # f_g for all f \in pre_w_p(a_i)
            a_pre_w_p = get_pre_p_w_from_action(action, self.waitfor)
            for pre in a_pre_w_p:
                pre_g = get_global_copy(pre)
                pre_p.append(pre_g)
            # pre_n
            pre_n = []
            # v_i >= w for all v,w in pre_n(a)
            a_pre_n = get_pre_n_from_action(action)
            for func in a_pre_n:
                func_i = get_local_copy(func, agent_name)
                pre_n.append(func_i)
            # v_g >= w for all v,w in pre_n_w(a)
            a_pre_n_w = get_pre_n_w_from_action(action, self.num_waitfor)
            for func in a_pre_n_w:
                func_g = get_global_copy(func)
                pre_n.append(func_g)
            # exists v_g < w in ((v,w) in pre_n(a) / pre_n_w(a)
            v_g_smaller_w = []
            for func in list(set(a_pre_n) - set(a_pre_n_w)):
                v_g = get_global_copy(func.parts[0])
                w = func.parts[1]
                v_g_smaller_w.append(FunctionComparison('<', [v_g, w]))
            pre_n.append(Disjunction(v_g_smaller_w))
            pre = Conjunction(pre_p + pre_n)
            # add
            add_list = []
            for eff in get_add_from_action(action):
                add_list.append(get_local_copy(eff, agent_name))
            add_list.append(get_failure_atom())
            # del
            del_list = []
            for eff in get_del_from_action(action):
                del_list.append(get_local_copy(eff, agent_name))
            # num
            num_list = []
            for num_eff in get_num_eff_from_action(action):
                num_list.append(get_local_copy(num_eff, agent_name))
            # Action
            action_n = Action(name=action.name + f'_n_{agent_name}', parameters=action.parameters,
                              num_external_parameters=action.num_external_parameters, precondition=pre,
                              _effects=add_list + del_list + num_list, cost=action.cost)
            return action_n

        def get_a_wt_p(action, x):
            agent_name = action.name.split('_')[1]
            x_name = '_'.join([x.predicate] + list(x.args))
            # pre_p
            pre_p = []
            pre_p.append(get_act_atom())  # act
            pre_p.append(get_waiting_atom(agent_name).negate())  # not waiting_i
            # f_i \and f_g forall f \in pre_p(a_i)
            a_pre_p = get_pre_p_from_action(action)
            for pre in a_pre_p:
                pre_i = get_local_copy(pre, agent_name)
                pre_p.append(pre_i)
            # \not x_g
            pre_p.append(get_global_copy(x).negate())
            # pre_n
            pre_n = []
            # v_i >= w for all v,w in pre_n(a)
            a_pre_n = get_pre_n_from_action(action)
            for func in a_pre_n:
                func_i = get_local_copy(func, agent_name)
                pre_n.append(func_i)
            pre = Conjunction(pre_p + pre_n)
            # add
            add_list = []
            for eff in get_add_from_action(action):
                add_list.append(get_local_copy(eff, agent_name))
            add_list.append(get_failure_atom())
            add_list.append(get_waiting_atom(agent_name))
            add_list.append(get_wt_f_atom(x))
            # del
            del_list = []
            for eff in get_del_from_action(action):
                del_list.append(get_local_copy(eff, agent_name))
            # num
            num_list = []
            for num_eff in get_num_eff_from_action(action):
                num_list.append(get_local_copy(num_eff, agent_name))
            # Action
            action_wt_p = Action(name=action.name + f'_wt_{x_name}_{agent_name}', parameters=action.parameters,
                                 num_external_parameters=action.num_external_parameters, precondition=pre,
                                 _effects=add_list + del_list + num_list, cost=action.cost)
            return action_wt_p

        def get_a_wt_n(action, x):
            agent_name = action.name.split('_')[1]
            x_name = '_'.join([x.parts[0].symbol] + list(x.parts[0].args) + [str(x.parts[1].value)])
            # pre_p
            pre_p = []
            pre_p.append(get_act_atom())  # act
            pre_p.append(get_waiting_atom(agent_name).negate())  # not waiting_i
            # f_i \and f_g forall f \in pre_p(a_i)
            a_pre_p = get_pre_p_from_action(action)
            for pre in a_pre_p:
                pre_i = get_local_copy(pre, agent_name)
                pre_p.append(pre_i)
            # pre_n
            pre_n = []
            # v_i >= w for all v,w in pre_n(a)
            a_pre_n = get_pre_n_from_action(action)
            for func in a_pre_n:
                func_i = get_local_copy(func, agent_name)
                pre_n.append(func_i)
            # x_g < w
            x_g = get_global_copy(x.parts[0])
            w = x.parts[1]
            pre_n.append(FunctionComparison('<', [x_g, w]))
            pre = Conjunction(pre_p + pre_n)
            # add
            add_list = []
            for eff in get_add_from_action(action):
                add_list.append(get_local_copy(eff, agent_name))
            add_list.append(get_failure_atom())
            add_list.append(get_waiting_atom(agent_name))
            add_list.append(get_wt_v_w_atom(x))
            # del
            del_list = []
            for eff in get_del_from_action(action):
                del_list.append(get_local_copy(eff, agent_name))
            # num
            num_list = []
            for num_eff in get_num_eff_from_action(action):
                num_list.append(get_local_copy(num_eff, agent_name))
            # Action
            action_wt_n = Action(name=action.name + f'_wt_{x_name}_{agent_name}', parameters=action.parameters,
                                 num_external_parameters=action.num_external_parameters, precondition=pre,
                                 _effects=add_list + del_list + num_list, cost=action.cost)
            return action_wt_n

        def get_a_wt(action):
            agent_name = action.name.split('_')[1]
            # pre_p
            pre_p = []
            pre_p.append(get_act_atom())  # act
            pre_p.append(get_waiting_atom(agent_name))  # waiting_i
            # f_i \and f_g forall f \in pre_p(a_i)
            for pre in get_pre_p_from_action(action):
                pre_i = get_local_copy(pre, agent_name)
                pre_p.append(pre_i)
            # pre_n
            pre_n = []
            # v_i >= w for all v,w in pre_n(a)
            for func in get_pre_n_from_action(action):
                func_i = get_local_copy(func, agent_name)
                pre_n.append(func_i)
            pre = Conjunction(pre_p + pre_n)
            # add
            add_list = []
            for eff in get_add_from_action(action):
                add_list.append(get_local_copy(eff, agent_name))
            # del
            del_list = []
            for eff in get_del_from_action(action):
                del_list.append(get_local_copy(eff, agent_name))
            # num
            num_list = []
            for num_eff in get_num_eff_from_action(action):
                num_list.append(get_local_copy(num_eff, agent_name))
            # Action
            action_wt = Action(name=action.name + f'_wt_{agent_name}', parameters=action.parameters,
                               num_external_parameters=action.num_external_parameters, precondition=pre,
                               _effects=add_list + del_list + num_list, cost=action.cost)
            return action_wt

        def get_A():
            # A_s
            A_s = []
            for action in grounded_task.actions:
                action_s = get_a_s(action)
                A_s.append(action_s)

            # A_p
            A_p = []
            for action in grounded_task.actions:
                action_p = get_a_p(action)
                A_p.append(action_p)

            # A_n
            A_n = []
            for action in grounded_task.actions:
                action_n = get_a_n(action)
                A_n.append(action_n)

            # A_wt_p
            A_wt_p = []
            for action in grounded_task.actions:
                for x in get_pre_p_w_from_action(action, self.waitfor):
                    action_wt_x = get_a_wt_p(action, x)
                    A_wt_p.append(action_wt_x)

            # A_wt_n
            A_wt_n = []
            for action in grounded_task.actions:
                for x in get_pre_n_w_from_action(action, self.num_waitfor):
                    action_wt_x = get_a_wt_n(action, x)
                    A_wt_p.append(action_wt_x)

            # A_wt
            A_wt = []
            for action in grounded_task.actions:
                action_wt = get_a_wt(action)

            return A_s + A_p + A_n + A_wt_p + A_wt_n + A_wt

        task = self.spp.task
        grounded_task = self.spp.final_grounded_task
        agents = [o for o in task.objects if o.type_name == 'agent']
        all_pre_n_w = []
        for action in grounded_task.actions:
            all_pre_n_w.extend(get_pre_n_w_from_action(action, self.num_waitfor))

        F = get_F()
        V = get_V()
        I_p = get_I_p()
        I_v = get_I_v()
        G = get_G()
        A = get_A()
        compiled_task = Task(domain_name=task.domain_name + '_compiled',
                             task_name=task.task_name + '_compiled',
                             requirements=task.requirements, types=task.types, objects=task.objects,
                             predicates=F, functions=V, init=I_p, num_init=I_v, goal=G,
                             actions=A, axioms=task.axioms, metric=task.metric)
        return compiled_task

        # for waitfor_dict in self.waitfor:
        #     if waitfor_dict['type'] != 'predicate':
        #         continue
        #     Predicate(name='wt_' + , arguments=[])

    def sanity_check(self):
        # sanity check
        # 1. there's an "agent" type
        # 2. actions in self.spp.final_grounded_task are grounded TODO
        # 3. first argument in any action is an agent
        # 4. actions precondition is either Atom or Conjunction
        # 5. actions numerical conditions have normal form
        # 6. waitfor conditions are of the form v >= 0
        assert 'agent' in [t.name for t in self.spp.task.types], "expected one 'agent' type"

    def get_action_df(self):
        action_name_list = []
        action_agent_list = []
        action_args_list = []

        for action in self.spp.final_grounded_task.actions:
            action_name_list.append(action.name.split('_')[0])
            action_agent_list.append(action.name.split('_')[1])
            action_args_list.append(action.name.split('_')[1:])
        return pd.DataFrame.from_dict(dict(action_name=action_name_list,
                                           action_agent=action_agent_list,
                                           action_args=action_args_list))


def main(domain_file, problem_file, waitfor_file=''):
    spp = SocialPlanningProblem(domain_file, problem_file)
    compiled_spp = Compilation(spp, waitfor_file=waitfor_file)
    print()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("domain-file", type=str, help="path to domain file")
    parser.add_argument("problem-file", type=str, help="path to problem file")
    args = parser.parse_args()
    main(domain_file=args.domain_file,
         problem_file=args.problem_file)
