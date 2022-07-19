import os
import unittest
from pathlib import Path

from numeric_slv.main import main, Compilation, task_to_pddl
from numeric_slv.task_to_pddl import get_pddl_domain, get_pddl_prob
from numeric_slv.utils import solve_pddl, write_file, solve_task

test_pddl_files_dir = os.path.join(os.path.dirname(__file__), 'test_pddl_files')

domain_str = """(define (domain sailing)
    
    (:types agent - object person - object)
    
    (:predicates 
        (saved ?t - person))
    
    (:functions
        (x ?b - agent)
        (y ?b - agent)
        (dx ?t - person)
        (dy ?t - person)
        (total-cost))
    
    ;; Increment the value in the given counter by one
    
    (:action go-est
        :parameters (?b - agent)
	:precondition (and )
        :effect (and (increase (total-cost) 1.0) (increase (x ?b) 1))
	)
    
    (:action go-west
        :parameters (?b - agent)
	:precondition (and )
        :effect (and (increase (total-cost) 1.0) (decrease (x ?b) 1))
	)
    
    (:action go-south
        :parameters(?b - agent)
	:precondition (and )
        :effect (and (increase (total-cost) 1.0) (decrease (y ?b) 1))
	)
	
	(:action go-north
        :parameters(?b - agent)
	:precondition (and )
        :effect (and (increase (total-cost) 1.0) (increase (y ?b) 1))
	)
    
    (:action save-person
        :parameters(?b - agent ?t - person)
        :precondition ( and
            (not (saved ?t))
            (<= (- (x ?b) (dx ?t)) 1)
            (<= (- (y ?b) (dy ?t)) 1)            
            (>= (- (x ?b) (dx ?t)) (- 0 1))
            (>= (- (y ?b) (dy ?t)) (- 0 1))
            )
        :effect (and (increase (total-cost) 1.0) (saved ?t))
	)
    )
"""

problem_str = """(define (problem instance_1_1_1229)

	(:domain sailing)

	(:objects
		b0 b1  - agent
		p0  - person)

  (:init
    (= (x b0) 0)
    (= (y b0) 0)
    (= (x b1) 0)
    (= (y b1) 0)
    (= (dx p0) 3)
    (= (dy p0) 3)
    (= (total-cost) 0))

	(:goal (and
	    (saved p0)))
	
	(:metric minimize (total-cost))
)
"""

info_str = """{
  "waitfor": [],
  "num_waitfor": [],
  "goal_affiliation":  ["b0"]
}"""

domain_path = os.path.join(test_pddl_files_dir, 'tmp_test_sailing_domain.pddl')
problem_path = os.path.join(test_pddl_files_dir, 'tmp_test_sailing_pfile1.pddl')
info_path = os.path.join(test_pddl_files_dir, 'tmp_test_sailing_pfile1.json')
compiled_domain_path = os.path.join(test_pddl_files_dir, 'tmp_test_sailing_domain_compiled.pddl')
compiled_problem_path = os.path.join(test_pddl_files_dir, 'tmp_test_sailing_pfile1_compiled.pddl')
write_file(domain_str, domain_path)
write_file(problem_str, problem_path)
write_file(info_str, info_path)


class Test(unittest.TestCase):

    # def test_solve_pddl(self):
    #     # problem is solvable by the planner
    #     res = solve_pddl(domain_path, problem_path)
    #     self.assertTrue(res['solved'])
    #     self.assertTrue(isinstance(res['plan'], list) and len(res['plan']) > 0)

    def test_compilation_works_with_tan_problem_no_social_law(self):
        # the compilation succeeds
        compilation = Compilation(domain_path, problem_path, info_path)
        # the compilation is solvable
        compiled_task = compilation.compiled_task
        grounded_task = compilation.grounded_task
        res = solve_task(grounded_task)
        self.assertTrue(res['solved'] == True)
        res = solve_task(compiled_task, timeout=300)
        self.assertTrue(res['solved'] == True)


if __name__ == '__main__':
    unittest.main()
