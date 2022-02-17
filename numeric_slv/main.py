import argparse
import json
from copy import deepcopy

from numeric_slv import SocialPlanningProblem
from translate.pddl import Predicate, Atom, Conjunction, NegatedAtom, FunctionComparison, PrimitiveNumericExpression, \
    Action, Literal, Effect, NumericConstant


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


class Compilation:

    def __init__(self, spp, waitfor_file=''):
        self.spp = deepcopy(spp)
        if waitfor_file:
            with open(waitfor_file, 'rb') as f:
                self.waitfor = json.load(f)
        self.sanity_check()
        self.agent_names_list = [o.name for o in self.spp.task.objects if o.type_name == 'agent']
        self.compiled_spp = self.compile_spp()

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
            # wt.f, i.e., there's an agent that is waiting for f
            # wt.v.w, i.e., there's an agent that is waiting for v >= w
            wt_f_list = []
            wt_v_w_list = []
            waitfor_predicates = set()
            waitfor_functions = set()
            for w_dict in self.waitfor:
                action_prefix = w_dict['action'] + '_' + w_dict['agent']
                actions_list = [a for a in grounded_task.actions if a.name.startswith(action_prefix)]
                for a in actions_list:
                    pre_list = get_action_precondition_as_list(a)
                if w_dict['type'] == 'predicate':
                    for pre in pre_list:
                        if isinstance(a.precondition, Atom) and w_dict['symbol_name'] == pre.predicate:
                            waitfor_predicates.add(pre)
                elif w_dict['type'] == 'function':
                    raise NotImplemented
            for pred in waitfor_predicates:
                wt_f_list.append(get_wt_f_predicate(pred))
            # act
            act_predicate = Predicate(name='act', arguments=[])
            # failure
            failure_predicate = Predicate(name='failure', arguments=[])
            # fin_i
            fin_i_list = []
            for a in agents:
                fin_i_list.append(Predicate(name='fin_' + a.name, arguments=[]))
            F = f_g_list + f_i_list + waiting_i_list + wt_f_list + wt_v_w_list + fin_i_list + [act_predicate,
                                                                                               failure_predicate]
            return F

        def get_V():
            # v_g
            v_g_list = []
            for v in grounded_task.functions:
                v_g = deepcopy(v)
                v_g.name += '_g'
                v_g_list.append(v_g)
            # v_i
            v_i_list = []
            for a in agents:
                for v in grounded_task.functions:
                    v_i = deepcopy(v)
                    v_i.name += '_' + a.name
                    v_i_list.append(v_i)
            V = v_g_list + v_i_list
            return V

        def get_I_p():
            # I_p
            # act
            act_predicate = Predicate(name='act', arguments=[])
            # f_g
            init_g_list = []
            for i in grounded_task.init:
                p = deepcopy(i)
                p.predicate += '_g'
                init_g_list.append(p)
            # f_i
            init_i_list = []
            for a in agents:
                for pred in grounded_task.init:
                    pred_i = deepcopy(pred)
                    pred_i.predicate += '_' + a.name
                    init_i_list.append(pred_i)
            I_p = [act_predicate] + init_g_list + init_i_list
            return I_p

        def get_I_v():
            # I_v
            # v_g
            v_g_list = []
            for v in grounded_task.num_init:
                v_g = deepcopy(v)
                v_g.fluent.symbol += '_g'
                v_g_list.append(v_g)
            # v_i
            v_i_list = []
            for a in agents:
                for v in grounded_task.num_init:
                    v_i = deepcopy(v)
                    v_i.fluent.symbol += '_' + a.name
                    v_i_list.append(v_i)
            I_v = v_g_list + v_i_list
            return I_v

        def get_G():
            goal_parts = []
            # failure
            goal_parts.append(Atom(predicate='failure', args=[]))
            # fin_i
            for ag in agents:
                goal_parts.append(Atom(predicate='fin_' + ag.name, args=[]))
            G = Conjunction(tuple(goal_parts))
            return G

        task = self.spp.task
        grounded_task = self.spp.final_grounded_task
        agents = [o for o in task.objects if o.type_name == 'agent']

        F = get_F()
        V = get_V()
        I_p = get_I_p()
        I_v = get_I_v()
        G = get_G()

        # A_i_s
        A_i_s = []
        for action in grounded_task.actions:
            agent_name = action.name.split('_')[1]
            # pre_p
            a_i_s_pre_p_parts = []
            # act
            a_i_s_pre_p_parts.append(Atom(predicate='act', args=[]))
            # not waiting_i
            a_i_s_pre_p_parts.append(NegatedAtom(predicate='waiting_' + agent_name, args=[]))
            # f_i \and f_g forall f \in pre_p(a_i)
            a_pre_p = get_pre_p_from_action(action)
            for pre in a_pre_p:
                pre_i = get_local_copy(pre, agent_name)
                pre_g = get_global_copy(pre)
                a_i_s_pre_p_parts.extend([pre_i, pre_g])
            # not wt.f for f in add(a)
            add_list = get_add_from_action(action)
            for eff in add_list:
                wt_atom = get_wt_f_atom(eff.peffect)
                a_i_s_pre_p_parts.append(wt_atom.negate())
            # pre_n
            a_i_s_pre_n_parts = []
            # v_i >= w \and v_g >= w for all v,w in pre_n(a)
            a_pre_n = get_pre_n_from_action(action)
            for func in a_pre_n:
                func_i = get_local_copy(func, agent_name)
                func_g = get_global_copy(func)
                a_i_s_pre_n_parts.extend([func_i, func_g])
            # \not wt.v.w \or v \smalle w - k for all (v,k) \in num(a), (v,w) \in


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
        assert 'agent' in [t.name for t in self.spp.task.types], "expected one 'agent' type"


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
