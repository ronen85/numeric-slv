;; Enrico Scala (enricos83@gmail.com) and Miquel Ramirez (miquel.ramirez@gmail.com)
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