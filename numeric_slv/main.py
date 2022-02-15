import argparse
import json
from copy import deepcopy

from numeric_slv import SocialPlanningProblem
from translate.pddl import Predicate, Atom, Conjunction, NegatedAtom, FunctionComparison, PrimitiveNumericExpression, \
    Action


def get_action_precondition_as_list(a: Action):
    assert isinstance(a, Action), f'expected an action, got {a}'
    if isinstance(a.precondition, Atom):
        return [a.precondition]
    elif isinstance(a.precondition, Conjunction):
        return a.precondition.parts
    else:
        raise NotImplemented


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
                pred_g = deepcopy(pred)
                pred_g.name += '_g'
                f_g_list.append(pred_g)
            # agent copies of f
            f_i_list = []
            agents = [o for o in task.objects if o.type_name == 'agent']
            for a in agents:
                for pred in task.predicates:
                    if pred.name == '=':
                        continue
                    pred_i = deepcopy(pred)
                    pred_i.name += '_' + a.name
                    f_i_list.append(pred_i)
            # waiting_i
            waiting_i_list = []
            for a in agents:
                waiting_i_list.append(Predicate(name='waiting_' + a.name, arguments=[]))
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
                wt_f_list.append(Predicate(name='_'.join(['wt', pred.predicate] + list(pred.args)), arguments=[]))
            # act
            act_predicate = Predicate(name='act', arguments=[])
            # failure
            failure_predicate = Predicate(name='failure', arguments=[])
            F = f_g_list + f_i_list + waiting_i_list + wt_f_list + wt_v_w_list + [act_predicate, failure_predicate]
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
            agents = [o for o in task.objects if o.type_name == 'agent']
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
                p.name += '_g'
                init_g_list.append(p)
            # f_i
            init_i_list = []
            agents = [o for o in task.objects if o.type_name == 'agent']
            for a in agents:
                for pred in grounded_task.init:
                    pred_i = deepcopy(pred)
                    pred_i.name += '_' + a.name
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
            agents = [o for o in task.objects if o.type_name == 'agent']
            for a in agents:
                for v in grounded_task.num_init:
                    v_i = deepcopy(v)
                    v_i.fluent.symbol += '_' + a.name
                    v_i_list.append(v_i)
            I_v = v_g_list + v_i_list
            return I_v

        task = self.spp.task
        grounded_task = self.spp.final_grounded_task

        F = get_F()
        V = get_V()
        I_p = get_I_p()
        I_v = get_I_v()









        print()


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
