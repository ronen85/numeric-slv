import os
import unittest
from pathlib import Path

from numeric_slv.main import main, Compilation, task_to_pddl, get_single_agent_projection
from numeric_slv.task_to_pddl import get_pddl_domain, get_pddl_prob
from numeric_slv.utils import solve_pddl, write_file, solve_task
from translate import pddl_parser

test_pddl_files_dir = os.path.join(os.path.dirname(__file__), 'test_pddl_files')

domain_str = """(define (domain tanning)
(:requirements :fluents :typing)
(:types agent bed - object)
(:predicates
    (free ?b - bed)
    (ready ?a - agent)
    (in ?a - agent ?b - bed))
(:functions 
(tan_level ?a - agent)
(total-cost)
)
; enter bed
(:action enter-bed
    :parameters (?a - agent ?b - bed)
    :precondition (and (free ?b) (ready ?a))
    :effect (and 
        (not (free ?b))
        (not (ready ?a))
        (in ?a ?b)
        (increase (total-cost) 1)
        ))
; tan
(:action tan
    :parameters (?a - agent ?b - bed)
    :precondition (and (in ?a ?b))
    :effect (and 
        (increase (tan_level ?a) 1)
        (increase (total-cost) 1)
        ))
; leave bed
(:action leave-bed
    :parameters (?a - agent ?b - bed)
    :precondition (and (in ?a ?b))
    :effect (and 
        (free ?b)
        (ready ?a)
        (not (in ?a ?b))
        (increase (total-cost) 1)
        ))
)
"""

problem_str = """(define (problem tan1) (:domain tanning)
(:objects 
a1 a2 - agent
bed1 - bed)
(:init
    (free bed1)
    (ready a1)
    (ready a2)
    (= (tan_level a1) 0)
    (= (tan_level a2) 0)
    (= (total-cost) 0))
(:goal (and
    (>= (tan_level a2) 3)
    (in a1 bed1)
    ))
(:metric minimize (total-cost))
)
"""

info_str = """{
  "waitfor": [],
  "num_waitfor": [],
  "goal_affiliation": ["a2", "a1"]
}
"""
domain_path = os.path.join(test_pddl_files_dir, 'tmp_test_tan_domain.pddl')
problem_path = os.path.join(test_pddl_files_dir, 'tmp_test_tan_pfile1.pddl')
info_path = os.path.join(test_pddl_files_dir, 'tmp_test_tan_pfile1.json')
compiled_domain_path = os.path.join(test_pddl_files_dir, 'tmp_test_tan_domain_compiled.pddl')
compiled_problem_path = os.path.join(test_pddl_files_dir, 'tmp_test_tan_pfile1_compiled.pddl')
write_file(domain_str, domain_path)
write_file(problem_str, problem_path)
write_file(info_str, info_path)


class Test(unittest.TestCase):

    def test_task_projection(self):
        task = pddl_parser.open_pddl(domain_path, problem_path)
        agent_name = "a1"
        single_agent_task = get_single_agent_projection(task, ["a2", "a1"], agent_name)
        res = solve_task(single_agent_task)
        self.assertTrue(all(map(lambda x: x == agent_name, [a.split(' ')[1] for a in res['plan']])))
        agent_name = "a2"
        single_agent_task = get_single_agent_projection(task, ["a2", "a1"], agent_name)
        res = solve_task(single_agent_task)
        self.assertTrue(all(map(lambda x: x == agent_name, [a.split(' ')[1] for a in res['plan']])))

if __name__ == '__main__':
    unittest.main()
