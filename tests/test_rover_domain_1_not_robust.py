import os
import unittest
from pathlib import Path

from numeric_slv.main import main, Compilation, task_to_pddl
from numeric_slv.task_to_pddl import get_pddl_domain, get_pddl_prob
from numeric_slv.utils import solve_pddl, write_file, solve_task

test_pddl_files_dir = os.path.join(os.path.dirname(__file__), 'test_pddl_files')

domain_str = """; Enrico Scala (enricos83@gmail.com) and Miquel Ramirez (miquel.ramirez@gmail.com)
(define (domain rover)
;(:requirements :typing :fluents)
(:types agent waypoint store camera mode lander objective - object)

(:predicates 
       (in ?x - agent ?y - waypoint) 
       (at-lander ?x - lander ?y - waypoint)
       (can-traverse ?r - agent ?x - waypoint ?y - waypoint)
       (equipped-for-soil-analysis ?r - agent)
       (equipped-for-rock-analysis ?r - agent)
       (equipped-for-imaging ?r - agent)
       (empty ?s - store)
       (have-rock-analysis ?r - agent ?w - waypoint)
       (have-soil-analysis ?r - agent ?w - waypoint)
       (full ?s - store)
       (calibrated ?c - camera ?r - agent) 
       (supports ?c - camera ?m - mode)
       (available ?r - agent)
       (visible ?w - waypoint ?p - waypoint)
       (have-image ?r - agent ?o - objective ?m - mode)
       (communicated-soil-data ?w - waypoint)
       (communicated-rock-data ?w - waypoint)
       (communicated-image-data ?o - objective ?m - mode)
       (at-soil-sample ?w - waypoint)
       (at-rock-sample ?w - waypoint)
       (visible-from ?o - objective ?w - waypoint)
       (store-of ?s - store ?r - agent)
       (calibration-target ?i - camera ?o - objective)
       (on-board ?i - camera ?r - agent)
       (channel-free ?l - lander)
       (in-sun ?w - waypoint)
)

(:functions 
       (energy ?r - agent) 
       (recharges) 
       (total-cost)
)
	
(:action navigate
:parameters (?x - agent ?y - waypoint ?z - waypoint) 
:precondition (and 
       (can-traverse ?x ?y ?z)
       (available ?x) 
       (in ?x ?y)
       (visible ?y ?z) 
       (>= (energy ?x) 8))
:effect (and 
       (decrease (energy ?x) 8) 
       (not (in ?x ?y)) 
       (in ?x ?z)
       (increase (total-cost) 1))
)

(:action recharge
:parameters (?x - agent ?w - waypoint)
:precondition (and 
       (in ?x ?w) 
       (in-sun ?w)
       (<= (energy ?x) 80))
:effect (and 
       (increase (energy ?x) 20) 
       (increase (recharges) 1)
       (increase (total-cost) 1))
)

(:action sample-soil
:parameters (?x - agent ?s - store ?p - waypoint)
:precondition (and 
       (in ?x ?p)
       (>= (energy ?x) 3) 
       (at-soil-sample ?p)
       (equipped-for-soil-analysis ?x)
       (store-of ?s ?x)
       (empty ?s))
:effect (and 
       (not (empty ?s)) 
       (full ?s) 
       (decrease (energy ?x) 3) 
       (have-soil-analysis ?x ?p)
       (not (at-soil-sample ?p))
       (increase (total-cost) 1))
)

(:action sample-rock
:parameters (?x - agent ?s - store ?p - waypoint)
:precondition (and  
       (in ?x ?p) 
       (>= (energy ?x) 5)
       (at-rock-sample ?p)
       (equipped-for-rock-analysis ?x)
       (store-of ?s ?x)
       (empty ?s))
:effect (and 
       (not (empty ?s)) 
       (full ?s) 
       (decrease (energy ?x) 5) 
       (have-rock-analysis ?x ?p)
       (not (at-rock-sample ?p))
       (increase (total-cost) 1))
)

(:action drop
:parameters (?x - agent ?y - store)
:precondition (and 
       (store-of ?y ?x)
       (full ?y))
:effect (and 
       (not (full ?y)) 
       (empty ?y)
       (increase (total-cost) 1))
)

(:action calibrate
 :parameters (?r - agent ?i - camera ?t - objective ?w - waypoint)
 :precondition (and 
       (equipped-for-imaging ?r)
       (>= (energy ?r) 2)
       (calibration-target ?i ?t)
       (in ?r ?w) 
       (visible-from ?t ?w)
       (on-board ?i ?r))
 :effect (and 
       (decrease (energy ?r) 2)
       (calibrated ?i ?r)
       (increase (total-cost) 1))
)

(:action take-image
 :parameters (?r - agent ?p - waypoint ?o - objective ?i - camera ?m - mode)
 :precondition (and 
       (calibrated ?i ?r)
	(on-board ?i ?r)
       (equipped-for-imaging ?r)
       (supports ?i ?m)
	(visible-from ?o ?p)
       (in ?r ?p)
	(>= (energy ?r) 1))
 :effect (and 
       (have-image ?r ?o ?m)
       (not (calibrated ?i ?r))
       (decrease (energy ?r) 1)
       (increase (total-cost) 1))
)

(:action communicate-soil-data
 :parameters (?r - agent ?l - lander ?p - waypoint ?x - waypoint ?y - waypoint)
 :precondition (and 
       (in ?r ?x)
       (at-lander ?l ?y)
       (have-soil-analysis ?r ?p)
       (visible ?x ?y)
       (available ?r)
       (channel-free ?l)
       (>= (energy ?r) 4))
 :effect (and 
       (communicated-soil-data ?p)
       (available ?r)
       (decrease (energy ?r) 4)
       (increase (total-cost) 1))
)

(:action communicate-rock-data
 :parameters (?r - agent ?l - lander ?p - waypoint ?x - waypoint ?y - waypoint)
 :precondition (and 
       (in ?r ?x)
       (at-lander ?l ?y)
       (have-rock-analysis ?r ?p)
       (>= (energy ?r) 4)
       (visible ?x ?y)
       (available ?r)
       (channel-free ?l))
 :effect (and   
       (communicated-rock-data ?p)
       (available ?r)
       (decrease (energy ?r) 4)
       (increase (total-cost) 1))
)

(:action communicate-image-data
 :parameters (?r - agent ?l - lander ?o - objective ?m - mode ?x - waypoint ?y - waypoint)
 :precondition (and 
       (in ?r ?x)
       (at-lander ?l ?y)
       (have-image ?r ?o ?m)
       (visible ?x ?y)
       (available ?r)
       (channel-free ?l)
       (>= (energy ?r) 6))
 :effect (and
       (communicated-image-data ?o ?m)
       (available ?r)
       (decrease (energy ?r) 6)
       (increase (total-cost) 1))
)


)
"""

problem_str = """(define (problem roverprob3726) (:domain rover)
(:objects
	general - lander
	colour - mode
	rover0 rover1 - agent
	rover0store rover1store - store
	waypoint0 waypoint1 - waypoint
	camera0 camera1 - camera
	objective0 - objective
	)
(:init
	(visible waypoint0 waypoint1)
	(visible waypoint1 waypoint0)
	(= (recharges) 0)
	(at-rock-sample waypoint0)
	(in-sun waypoint0)
	(at-rock-sample waypoint1)
	(in-sun waypoint1)
	(at-lander general waypoint0)
	(channel-free general)
	(= (energy rover0) 50)
	(in rover0 waypoint1)
	(in rover1 waypoint1)
	(available rover0)
	(store-of rover0store rover0)
	(empty rover0store)
	(equipped-for-soil-analysis rover0)
	(equipped-for-rock-analysis rover0)
	(equipped-for-imaging rover0)
	(can-traverse rover0 waypoint1 waypoint0)
	(can-traverse rover0 waypoint0 waypoint1)
	(= (energy rover1) 50)
	(available rover1)
	(store-of rover1store rover1)
	(empty rover1store)
	(equipped-for-soil-analysis rover1)
	(equipped-for-rock-analysis rover1)
	(equipped-for-imaging rover1)
	(can-traverse rover1 waypoint0 waypoint1)
	(can-traverse rover1 waypoint1 waypoint0)
	(on-board camera0 rover0)
	(calibration-target camera0 objective0)
	(on-board camera1 rover1)
	(calibration-target camera1 objective0)
	(supports camera1 colour)
	(visible-from objective0 waypoint0)
	(visible-from objective0 waypoint1)
	(= (total-cost) 0.0)
)

(:goal (and
(communicated-rock-data waypoint0)
(in rover1 waypoint0)
	)
)

(:metric minimize (total-cost))
)
"""
info_str = """{
  "waitfor": [],
  "num_waitfor": [],
  "goal_affiliation":  ["rover0", "rover1"]
}"""

domain_path = os.path.join(test_pddl_files_dir, 'tmp_test_rover_domain.pddl')
problem_path = os.path.join(test_pddl_files_dir, 'tmp_test_rover_pfile1.pddl')
info_path = os.path.join(test_pddl_files_dir, 'tmp_test_rover_pfile1.json')
compiled_domain_path = os.path.join(test_pddl_files_dir, 'tmp_test_rover_domain_compiled.pddl')
compiled_problem_path = os.path.join(test_pddl_files_dir, 'tmp_test_rover_pfile1_compiled.pddl')
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
        res = solve_task(compiled_task)
        self.assertTrue(res['solved'] == True)


if __name__ == '__main__':
    unittest.main()
