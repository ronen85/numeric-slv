(define (problem depotprob1935) (:domain depot)
(:objects
	depot0 - depot
	distributor0 distributor1 - distributor
	truck0 truck1 - truck
	pallet0 pallet1 pallet2 - pallet
	crate0 crate1 crate2 crate3 crate4 crate5 - crate
	hoist0 hoist1 hoist2 - hoist)
(:init
	(located pallet0 depot0)
	(clear crate1)
	(located pallet1 distributor0)
	(clear crate4)
	(located pallet2 distributor1)
	(clear crate5)
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
	(located crate0 distributor0)
	(on crate0 pallet1)
	(= (weight crate0) 4)
	(located crate1 depot0)
	(on crate1 pallet0)
	(= (weight crate1) 4)
	(located crate2 distributor1)
	(on crate2 pallet2)
	(= (weight crate2) 4)
	(located crate3 distributor0)
	(on crate3 crate0)
	(= (weight crate3) 4)
	(located crate4 distributor0)
	(on crate4 crate3)
	(= (weight crate4) 4)
	(located crate5 distributor1)
	(on crate5 crate2)
	(= (weight crate5) 4)
	(= (fuel-cost) 0)
)

(:goal (and
		(on crate0 crate1)
		(on crate1 pallet2)
		(on crate2 pallet0)
		(on crate3 crate2)
		(on crate4 pallet1)
		(on crate5 crate4)
	)
)

(:metric minimize (fuel-cost))
)


