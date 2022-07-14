(define (problem roverprob6232) (:domain rover)
(:objects
	general - lander
	colour high-res low-res - mode
	rover0 rover1 - agent
	rover0store rover1store - store
	waypoint0 waypoint1 waypoint2 waypoint3 - waypoint
	camera0 camera1 camera2 - camera
	objective0 objective1 objective2 - objective
	)
(:init
	(visible waypoint1 waypoint0)
	(visible waypoint0 waypoint1)
	(visible waypoint2 waypoint1)
	(visible waypoint1 waypoint2)
	(visible waypoint2 waypoint3)
	(visible waypoint3 waypoint2)
	(visible waypoint3 waypoint1)
	(visible waypoint1 waypoint3)
	(= (recharges) 0)
	(at-rock-sample waypoint1)
	(in-sun waypoint1)
	(at-soil-sample waypoint2)
	(in-sun waypoint2)
	(at-soil-sample waypoint3)
	(at-rock-sample waypoint3)
	(at-lander general waypoint2)
	(channel-free general)
	(= (energy rover0) 50)
	(in rover0 waypoint3)
	(available rover0)
	(store-of rover0store rover0)
	(empty rover0store)
	(equipped-for-soil-analysis rover0)
	(equipped-for-imaging rover0)
	(can-traverse rover0 waypoint3 waypoint1)
	(can-traverse rover0 waypoint1 waypoint3)
	(= (energy rover1) 50)
	(in rover1 waypoint2)
	(available rover1)
	(store-of rover1store rover1)
	(empty rover1store)
	(equipped-for-soil-analysis rover1)
	(equipped-for-rock-analysis rover1)
	(equipped-for-imaging rover1)
	(can-traverse rover1 waypoint2 waypoint1)
	(can-traverse rover1 waypoint1 waypoint2)
	(can-traverse rover1 waypoint2 waypoint3)
	(can-traverse rover1 waypoint3 waypoint2)
	(can-traverse rover1 waypoint1 waypoint0)
	(can-traverse rover1 waypoint0 waypoint1)
	(on-board camera0 rover1)
	(calibration-target camera0 objective0)
	(supports camera0 colour)
	(supports camera0 high-res)
	(on-board camera1 rover0)
	(calibration-target camera1 objective0)
	(supports camera1 colour)
	(supports camera1 low-res)
	(on-board camera2 rover0)
	(calibration-target camera2 objective1)
	(supports camera2 low-res)
	(visible-from objective0 waypoint0)
	(visible-from objective0 waypoint1)
	(visible-from objective0 waypoint2)
	(visible-from objective0 waypoint3)
	(visible-from objective1 waypoint0)
	(visible-from objective1 waypoint1)
	(visible-from objective2 waypoint0)
	(visible-from objective2 waypoint1)
	(visible-from objective2 waypoint2)
)

(:goal (and
(communicated-soil-data waypoint3)
(communicated-rock-data waypoint1)
(communicated-image-data objective0 high-res)
	)
)

(:metric minimize (recharges))
)