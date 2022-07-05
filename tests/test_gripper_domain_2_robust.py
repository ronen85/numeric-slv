import os
import unittest
from pathlib import Path

from numeric_slv.main import main, Compilation, task_to_pddl
from numeric_slv.task_to_pddl import get_pddl_domain, get_pddl_prob
from numeric_slv.utils import solve_pddl, write_file, solve_task

test_pddl_files_dir = os.path.join(os.path.dirname(__file__), 'test_pddl_files')

domain_str = """(define (domain multi-gripper-num)
  (:types room ball gripper agent - object)
   (:predicates (at-robby ?r - agent ?x - room)
		 (at ?b - ball ?x - room)
		 (door ?x - room ?y - room)
		 (free ?g - gripper)
		 (in-g ?b - ball ?g - gripper)
		 (in-tray ?b - ball ?r - agent) 
		 (mount ?g - gripper ?r - agent)
		 (belongs ?b - ball ?r - agent)
		 )
		
   (:functions 
	(load_limit ?r - agent) 
	(current_load ?r - agent) 
	(weight ?b - ball))
	; (cost))

   (:action move
       :parameters (?r - agent ?x - room ?y - room) 
       :precondition (and (at-robby ?r ?x)
                          (door ?x ?y))
       :effect (and  (at-robby ?r ?y)
		     (not (at-robby ?r ?x))
		    ;  (increase (cost) 2)
		     ))



   (:action pick
       :parameters (?r - agent ?b - ball ?x - room ?g - gripper)
       :precondition  (and (at ?b ?x) (at-robby ?r ?x) (free ?g) (mount ?g ?r) (belongs ?b ?r)
                           (<= (+ (current_load ?r) (weight ?b)) (load_limit ?r)))
       :effect (and (in-g ?b ?g)
		    (not (at ?b ?x)) 
		    (not (free ?g))
		    (increase (current_load ?r) (weight ?b))
		    ; (increase (cost) 1)
		    ))
		    

   (:action drop
       :parameters (?r - agent ?b - ball ?x - room ?g - gripper)
       :precondition (and (in-g ?b ?g) 
                     (at-robby ?r ?x) 
                     (mount ?g ?r))
       :effect (and (free ?g)
                    (at ?b ?x) 
                    (not (in-g ?b ?g))
                    (decrease (current_load ?r) (weight ?b))
                    ; (increase (cost) 1)
                    ))
   
   (:action to-tray
       :parameters (?r - agent ?b - ball ?g - gripper) 
       :precondition (and (in-g ?b ?g)
                          (mount ?g ?r))
       :effect (and (free ?g)
		     (not (in-g ?b ?g))
		     (in-tray ?b ?r)
		    ;  (increase (cost) 0)
		     ))
		  
   (:action from-tray
       :parameters (?r - agent ?b - ball ?g - gripper) 
       :precondition (and  (in-tray ?b ?r)
                           (mount ?g ?r)
                           (free ?g))
       :effect (and  (not (free ?g))
		     (in-g ?b ?g)
		     (not (in-tray ?b ?r))
		    ;  (increase (cost) 0)
		     ))
)
"""

problem_str = """(define (problem num-gripper-x-1)   (:domain multi-gripper-num)
   (:objects rooma roomb - room
             ball1 - ball
             r1 r2 - agent
             left1 left2 - gripper)
   (:init (= (weight ball1) 1)
          (at-robby r1 rooma)
          (at-robby r2 rooma)
          (free left1)
          (free left2)          
          (mount left1 r1)          
          (mount left2 r2)          
          (at ball1 rooma)
          (door rooma roomb)
          (door roomb rooma)
          (= (current_load r1) 0)
          (= (load_limit r1) 4)
          (= (current_load r2) 0)
          (= (load_limit r2) 4)
          (belongs ball1 r1)
          )
          
   (:goal (and (at ball1 roomb)))
               
   ; (:metric minimize (cost))
)
"""
info_str = """{
  "waitfor": [],
  "num_waitfor": [],
  "goal_affiliation": ["r1"]
}"""

domain_path = os.path.join(test_pddl_files_dir, 'tmp_test_gripper_domain.pddl')
problem_path = os.path.join(test_pddl_files_dir, 'tmp_test_gripper_pfile1.pddl')
info_path = os.path.join(test_pddl_files_dir, 'tmp_test_gripper_pfile1.json')
compiled_domain_path = os.path.join(test_pddl_files_dir, 'tmp_test_gripper_domain_compiled.pddl')
compiled_problem_path = os.path.join(test_pddl_files_dir, 'tmp_test_gripper_pfile1_compiled.pddl')
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
        self.assertTrue(res['solved'] == False)


if __name__ == '__main__':
    unittest.main()
