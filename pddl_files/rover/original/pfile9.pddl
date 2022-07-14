(define (problem roverprob4132) (:domain rover)
(:objects
	general - lander
	colour high-res low-res - mode
	rover0 rover1 rover2 rover3 - rover
	rover0store rover1store rover2store rover3store - store
	waypoint0 waypoint1 waypoint2 waypoint3 waypoint4 waypoint5 waypoint6 - waypoint
	camera0 camera1 camera2 camera3 camera4 - camera
	objective0 objective1 objective2 - objective
	)
(:init
	(visible waypoint0 waypoint5)
	(visible waypoint5 waypoint0)
	(visible waypoint0 waypoint6)
	(visible waypoint6 waypoint0)
	(visible waypoint1 waypoint0)
	(visible waypoint0 waypoint1)
	(visible waypoint1 waypoint2)
	(visible waypoint2 waypoint1)
	(visible waypoint1 waypoint4)
	(visible waypoint4 waypoint1)
	(visible waypoint1 waypoint6)
	(visible waypoint6 waypoint1)
	(visible waypoint2 waypoint0)
	(visible waypoint0 waypoint2)
	(visible waypoint2 waypoint5)
	(visible waypoint5 waypoint2)
	(visible waypoint2 waypoint6)
	(visible waypoint6 waypoint2)
	(visible waypoint3 waypoint0)
	(visible waypoint0 waypoint3)
	(visible waypoint3 waypoint1)
	(visible waypoint1 waypoint3)
	(visible waypoint4 waypoint3)
	(visible waypoint3 waypoint4)
	(visible waypoint4 waypoint6)
	(visible waypoint6 waypoint4)
	(visible waypoint5 waypoint1)
	(visible waypoint1 waypoint5)
	(visible waypoint6 waypoint3)
	(visible waypoint3 waypoint6)
	(visible waypoint6 waypoint5)
	(visible waypoint5 waypoint6)
	(= (recharges) 0)
	(at-soil-sample waypoint0)
	(at-rock-sample waypoint0)
	(at-soil-sample waypoint1)
	(at-rock-sample waypoint1)
	(at-rock-sample waypoint3)
	(at-soil-sample waypoint4)
	(at-soil-sample waypoint5)
	(at-rock-sample waypoint5)
	(in-sun waypoint5)
	(at-soil-sample waypoint6)
	(at-rock-sample waypoint6)
	(at-lander general waypoint4)
	(channel-free general)
	(= (energy rover0) 50)
	(in rover0 waypoint5)
	(available rover0)
	(store-of rover0store rover0)
	(empty rover0store)
	(equipped-for-imaging rover0)
	(can-traverse rover0 waypoint5 waypoint0)
	(can-traverse rover0 waypoint0 waypoint5)
	(can-traverse rover0 waypoint5 waypoint1)
	(can-traverse rover0 waypoint1 waypoint5)
	(can-traverse rover0 waypoint5 waypoint2)
	(can-traverse rover0 waypoint2 waypoint5)
	(can-traverse rover0 waypoint5 waypoint6)
	(can-traverse rover0 waypoint6 waypoint5)
	(can-traverse rover0 waypoint1 waypoint3)
	(can-traverse rover0 waypoint3 waypoint1)
	(can-traverse rover0 waypoint1 waypoint4)
	(can-traverse rover0 waypoint4 waypoint1)
	(= (energy rover1) 50)
	(in rover1 waypoint2)
	(available rover1)
	(store-of rover1store rover1)
	(empty rover1store)
	(equipped-for-rock-analysis rover1)
	(equipped-for-imaging rover1)
	(can-traverse rover1 waypoint2 waypoint0)
	(can-traverse rover1 waypoint0 waypoint2)
	(can-traverse rover1 waypoint2 waypoint1)
	(can-traverse rover1 waypoint1 waypoint2)
	(can-traverse rover1 waypoint2 waypoint5)
	(can-traverse rover1 waypoint5 waypoint2)
	(can-traverse rover1 waypoint2 waypoint6)
	(can-traverse rover1 waypoint6 waypoint2)
	(can-traverse rover1 waypoint1 waypoint3)
	(can-traverse rover1 waypoint3 waypoint1)
	(can-traverse rover1 waypoint1 waypoint4)
	(can-traverse rover1 waypoint4 waypoint1)
	(= (energy rover2) 50)
	(in rover2 waypoint0)
	(available rover2)
	(store-of rover2store rover2)
	(empty rover2store)
	(equipped-for-soil-analysis rover2)
	(equipped-for-imaging rover2)
	(can-traverse rover2 waypoint0 waypoint1)
	(can-traverse rover2 waypoint1 waypoint0)
	(can-traverse rover2 waypoint0 waypoint3)
	(can-traverse rover2 waypoint3 waypoint0)
	(can-traverse rover2 waypoint0 waypoint6)
	(can-traverse rover2 waypoint6 waypoint0)
	(can-traverse rover2 waypoint1 waypoint2)
	(can-traverse rover2 waypoint2 waypoint1)
	(can-traverse rover2 waypoint1 waypoint5)
	(can-traverse rover2 waypoint5 waypoint1)
	(can-traverse rover2 waypoint3 waypoint4)
	(can-traverse rover2 waypoint4 waypoint3)
	(= (energy rover3) 50)
	(in rover3 waypoint2)
	(available rover3)
	(store-of rover3store rover3)
	(empty rover3store)
	(equipped-for-soil-analysis rover3)
	(equipped-for-imaging rover3)
	(can-traverse rover3 waypoint2 waypoint0)
	(can-traverse rover3 waypoint0 waypoint2)
	(can-traverse rover3 waypoint2 waypoint1)
	(can-traverse rover3 waypoint1 waypoint2)
	(can-traverse rover3 waypoint2 waypoint6)
	(can-traverse rover3 waypoint6 waypoint2)
	(can-traverse rover3 waypoint0 waypoint3)
	(can-traverse rover3 waypoint3 waypoint0)
	(can-traverse rover3 waypoint0 waypoint5)
	(can-traverse rover3 waypoint5 waypoint0)
	(can-traverse rover3 waypoint1 waypoint4)
	(can-traverse rover3 waypoint4 waypoint1)
	(on-board camera0 rover3)
	(calibration-target camera0 objective2)
	(supports camera0 colour)
	(supports camera0 low-res)
	(on-board camera1 rover0)
	(calibration-target camera1 objective2)
	(supports camera1 colour)
	(on-board camera2 rover0)
	(calibration-target camera2 objective0)
	(supports camera2 low-res)
	(on-board camera3 rover2)
	(calibration-target camera3 objective0)
	(supports camera3 colour)
	(supports camera3 high-res)
	(supports camera3 low-res)
	(on-board camera4 rover1)
	(calibration-target camera4 objective1)
	(supports camera4 colour)
	(supports camera4 low-res)
	(visible-from objective0 waypoint0)
	(visible-from objective0 waypoint1)
	(visible-from objective0 waypoint2)
	(visible-from objective1 waypoint0)
	(visible-from objective1 waypoint1)
	(visible-from objective1 waypoint2)
	(visible-from objective1 waypoint3)
	(visible-from objective1 waypoint4)
	(visible-from objective1 waypoint5)
	(visible-from objective2 waypoint0)
	(visible-from objective2 waypoint1)
	(visible-from objective2 waypoint2)
	(visible-from objective2 waypoint3)
	(visible-from objective2 waypoint4)
	(visible-from objective2 waypoint5)
	(visible-from objective2 waypoint6)
)

(:goal (and
(communicated-soil-data waypoint6)
(communicated-soil-data waypoint4)
(communicated-soil-data waypoint0)
(communicated-rock-data waypoint6)
(communicated-rock-data waypoint0)
(communicated-rock-data waypoint3)
(communicated-image-data objective2 low-res)
(communicated-image-data objective2 colour)
	)
)

(:metric minimize (recharges))
)
