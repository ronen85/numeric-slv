import os
import unittest
from pathlib import Path

from numeric_slv.main import main, Compilation, task_to_pddl
from numeric_slv.task_to_pddl import get_pddl_domain, get_pddl_prob
from numeric_slv.utils import solve_pddl, write_file, solve_task
from translate.pddl_parser.parsing_functions import parse_typed_list
from translate.pddl_parser.pddl_file import parse_pddl_file

test_pddl_files_dir = os.path.join(os.path.dirname(__file__), 'test_pddl_files')

domain_str = """;; Enrico Scala (enricos83@gmail.com) and Miquel Ramirez (miquel.ramirez@gmail.com)
(define (domain depot)
(:requirements :typing :fluents)
(:types agent place locatable - object  ; add agent type
    depot distributor - place
    truck hoist surface - locatable
    pallet crate - surface)

(:predicates (located ?x - locatable ?y - place) 
             (on ?x - crate ?y - surface)
             (in ?x - crate ?y - truck)
             (lifting ?x - hoist ?y - crate)
             (available ?x - hoist)
             (clear ?x - surface)
)

(:functions 
	(load_limit ?t - truck) 
	(current_load ?t - truck) 
	(weight ?c - crate)
	(fuel-cost)
)
	
(:action Drive
:parameters (?a - agent ?x - truck ?y - place ?z - place)  ; add agent argument 
:precondition (and (located ?x ?y))
:effect (and (not (located ?x ?y)) (located ?x ?z)
		(increase (fuel-cost) 10)))

(:action Lift
:parameters (?a - agent ?x - hoist ?y - crate ?z - surface ?p - place)  ; add agent argument
:precondition (and (located ?x ?p) (available ?x) (located ?y ?p) (on ?y ?z) (clear ?y))
:effect (and (not (located ?y ?p)) (lifting ?x ?y) (not (clear ?y)) (not (available ?x)) 
             (clear ?z) (not (on ?y ?z)) (increase (fuel-cost) 1)))

(:action Drop 
:parameters (?a - agent ?x - hoist ?y - crate ?z - surface ?p - place)  ; add agent argument
:precondition (and (located ?x ?p) (located ?z ?p) (clear ?z) (lifting ?x ?y))
:effect (and (available ?x) (not (lifting ?x ?y)) (located ?y ?p) (not (clear ?z)) (clear ?y)
		(on ?y ?z)))

(:action Load
:parameters (?a - agent ?x - hoist ?y - crate ?z - truck ?p - place)  ; add agent argument
:precondition (and (located ?x ?p) (located ?z ?p) (lifting ?x ?y)
		(<= (+ (current_load ?z) (weight ?y)) (load_limit ?z)))
:effect (and (not (lifting ?x ?y)) (in ?y ?z) (available ?x)
		(increase (current_load ?z) (weight ?y))))

(:action Unload 
:parameters (?a - agent ?x - hoist ?y - crate ?z - truck ?p - place)  ; add agent argument
:precondition (and (located ?x ?p) (located ?z ?p) (available ?x) (in ?y ?z))
:effect (and (not (in ?y ?z)) (not (available ?x)) (lifting ?x ?y)
		(decrease (current_load ?z) (weight ?y))))

)
"""

problem_str = """(define (problem depotprob1818) (:domain depot)
(:objects
    a1 a2 - agent  ; add two agents 
	depot0 - depot
	distributor0 distributor1 - distributor
	truck0 truck1 - truck
	pallet0 pallet1 pallet2 - pallet
	crate0 crate1 - crate
	hoist0 hoist1 hoist2 - hoist)
(:init
	(located pallet0 depot0)
	(clear crate1)
	(located pallet1 distributor0)
	(clear crate0)
	(located pallet2 distributor1)
	(clear pallet2)
	(located truck0 distributor1)
	(= (current_load truck0) 0)
	(= (load_limit truck0) 323)
	(located truck1 depot0)
	(= (current_load truck1) 0)
	(= (load_limit truck1) 220)
	(located hoist0 depot0)
	(available hoist0)
	(located hoist1 distributor0)
	(available hoist1)
	(located hoist2 distributor1)
	(available hoist2)
	(located crate0 distributor0)
	(on crate0 pallet1)
	(= (weight crate0) 11)
	(located crate1 depot0)
	(on crate1 pallet0)
	(= (weight crate1) 86)
	(= (fuel-cost) 0)
)

(:goal (and
		(on crate0 pallet2)
		(on crate1 pallet1)
	)
)

(:metric minimize (fuel-cost))
)
"""

info_str = """{
  "waitfor": [], 
  "num_waitfor": [],
  "goal_affiliation": ["a1", "a2"]
}
"""

domain_path = os.path.join(test_pddl_files_dir, 'tmp_test_depots_domain.pddl')
problem_path = os.path.join(test_pddl_files_dir, 'tmp_test_depots_pfile1.pddl')
info_path = os.path.join(test_pddl_files_dir, 'tmp_test_depots_pfile1.json')
compiled_domain_path = os.path.join(test_pddl_files_dir, 'tmp_test_depots_domain_compiled.pddl')
compiled_problem_path = os.path.join(test_pddl_files_dir, 'tmp_test_depots_pfile1_compiled.pddl')
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
        res = solve_task(compiled_task, timeout=120)
        self.assertTrue(res['solved'] == True)


if __name__ == '__main__':
    unittest.main()
