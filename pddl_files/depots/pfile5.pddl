(define (problem depotprob1212) (:domain depot)
(:objects
	depot0 - depot
	distributor0 distributor1 - distributor
	truck0 truck1 - truck
	pallet0 pallet1 pallet2 - pallet
	crate0 crate1 crate2 crate3 crate4 crate5 crate6 crate7 crate8 crate9 - crate
	hoist0 hoist1 hoist2 - hoist)
(:init
	(located pallet0 depot0)
	(clear crate4)
	(located pallet1 distributor0)
	(clear crate8)
	(located pallet2 distributor1)
	(clear crate9)
	(located truck0 depot0)
	(= (current_load truck0) 0)
	(= (load_limit truck0) 20)
	(located truck1 distributor0)
	(= (current_load truck1) 0)
	(= (load_limit truck1) 20)
	(located hoist0 depot0)
	(available hoist0)
	(located hoist1 distributor0)
	(available hoist1)
	(located hoist2 distributor1)
	(available hoist2)
	(located crate0 distributor1)
	(on crate0 pallet2)
	(= (weight crate0) 4)
	(located crate1 depot0)
	(on crate1 pallet0)
	(= (weight crate1) 4)
	(located crate2 distributor1)
	(on crate2 crate0)
	(= (weight crate2) 4)
	(located crate3 depot0)
	(on crate3 crate1)
	(= (weight crate3) 4)
	(located crate4 depot0)
	(on crate4 crate3)
	(= (weight crate4) 4)
	(located crate5 distributor1)
	(on crate5 crate2)
	(= (weight crate5) 4)
	(located crate6 distributor0)
	(on crate6 pallet1)
	(= (weight crate6) 4)
	(located crate7 distributor0)
	(on crate7 crate6)
	(= (weight crate7) 4)
	(located crate8 distributor0)
	(on crate8 crate7)
	(= (weight crate8) 4)
	(located crate9 distributor1)
	(on crate9 crate5)
	(= (weight crate9) 4)
	(= (fuel-cost) 0)
)

(:goal (and
		(on crate1 pallet1)
		(on crate0 crate1)
		(on crate2 crate0)
		(on crate7 crate2)
		(on crate3 pallet2)
		(on crate8 crate3)
		(on crate9 pallet0)
		(on crate6 crate9)
		(on crate4 crate6)
		(on crate5 crate4)
	)
)

(:metric minimize (fuel-cost)))