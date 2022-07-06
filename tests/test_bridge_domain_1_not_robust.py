import os
import unittest
from pathlib import Path

from numeric_slv.main import main, Compilation, task_to_pddl
from numeric_slv.task_to_pddl import get_pddl_domain, get_pddl_prob
from numeric_slv.utils import solve_pddl, write_file, solve_task

test_pddl_files_dir = os.path.join(os.path.dirname(__file__), 'test_pddl_files')

domain_str = """(define (domain bridge)

(:requirements :fluents :typing)

(:types agent bridge)

(:predicates
(on-right-bank ?a - agent)
(on-left-bank ?a - agent)
(on-bridge ?a - agent ?b - bridge)
)


(:functions 
(weight ?a - agent)
(curr-load ?b - bridge)
(weight-limit ?b - bridge)
)

(:action right-get-on-bridge
    :parameters (?a - agent ?b - bridge)
    :precondition (and 
    (on-right-bank ?a)
    (>= (weight-limit ?b) (+ (curr-load ?b) (weight ?a)))
    )
    :effect (and 
    (on-bridge ?a ?b)
    (not (on-right-bank ?a))
    (increase (curr-load ?b) (weight ?a))
    )
)

(:action left-get-on-bridge
    :parameters (?a - agent ?b - bridge)
    :precondition (and 
    (on-left-bank ?a)
    (>= (weight-limit ?b) (+ (curr-load ?b) (weight ?a)))
    )
    :effect (and 
    (on-bridge ?a ?b)
    (not (on-left-bank ?a))
    (increase (curr-load ?b) (weight ?a))
    )
)

(:action bridge-get-on-right
    :parameters (?a - agent ?b - bridge)
    :precondition (and 
    (on-bridge ?a ?b)
    )
    :effect (and 
    (on-right-bank ?a)
    (not (on-bridge ?a ?b))
    (decrease (curr-load ?b) (weight ?a))
    )
)

(:action bridge-get-on-left
    :parameters (?a - agent ?b - bridge)
    :precondition (and 
    (on-bridge ?a ?b)
    )
    :effect (and 
    (on-left-bank ?a)
    (not (on-bridge ?a ?b))
    (decrease (curr-load ?b) (weight ?a))
    )
)
)
"""

problem_str = """(define (problem b1) (:domain bridge)
(:objects 
a1 a2 - agent
b1 - bridge
)

(:init
(on-right-bank a1)
(on-right-bank a2)
(= (weight a1) 50)
(= (weight a2) 60)
(= (weight-limit b1) 100)
(= (curr-load b1) 0)
)

(:goal (and
    (on-left-bank a1)
    (on-left-bank a2)
))

)

"""

info_str = """{
  "waitfor": [],
  "num_waitfor": [],
  "goal_affiliation": ["a1", "a2"]
}
"""
domain_path = os.path.join(test_pddl_files_dir, 'tmp_test_bridge_domain.pddl')
problem_path = os.path.join(test_pddl_files_dir, 'tmp_test_bridge_pfile1.pddl')
info_path = os.path.join(test_pddl_files_dir, 'tmp_test_bridge_pfile1.json')
compiled_domain_path = os.path.join(test_pddl_files_dir, 'tmp_test_bridge_domain_compiled.pddl')
compiled_problem_path = os.path.join(test_pddl_files_dir, 'tmp_test_bridge_pfile1_compiled.pddl')
write_file(domain_str, domain_path)
write_file(problem_str, problem_path)
write_file(info_str, info_path)


class Test(unittest.TestCase):

    def test_solve_pddl(self):
        # problem is solvable by the planner
        res = solve_pddl(domain_path, problem_path)
        self.assertTrue(res['solved'])
        self.assertTrue(isinstance(res['plan'], list) and len(res['plan']) > 0)

    def test_compilation_works_with_tan_problem_no_social_law(self):
        # the compilation succeeds
        compilation = Compilation(domain_path, problem_path, info_path)
        # the compilation is solvable
        compiled_task = compilation.compiled_task
        res = solve_task(compiled_task)
        self.assertTrue(res['solved'] == True)


if __name__ == '__main__':
    unittest.main()
