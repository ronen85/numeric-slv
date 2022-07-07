(define (problem depotprob4398) (:domain depot)
(:objects
	a1 a2 - agent
	depot0 depot1 - depot
	distributor0 distributor1 - distributor
	truck0 truck1 truck2 truck3 - truck
	pallet0 pallet1 pallet2 pallet3 pallet4 pallet5 pallet6 pallet7 - pallet
	crate0 crate1 crate2 crate3 crate4 crate5 - crate
	hoist0 hoist1 hoist2 hoist3 hoist4 hoist5 hoist6 hoist7 - hoist)
(:init
	(located pallet0 depot0)
	(clear crate5)
	(located pallet1 depot1)
	(clear crate3)
	(located pallet2 distributor0)
	(clear crate4)
	(located pallet3 distributor1)
	(clear pallet3)
	(located pallet4 depot1)
	(clear crate0)
	(located pallet5 distributor1)
	(clear pallet5)
	(located pallet6 depot1)
	(clear pallet6)
	(located pallet7 distributor0)
	(clear pallet7)
	(located truck0 depot1)
	(= (current_load truck0) 0)
	(= (load_limit truck0) 20)
	(located truck1 depot1)
	(= (current_load truck1) 0)
	(= (load_limit truck1) 20)
	(located truck2 depot0)
	(= (current_load truck2) 0)
	(= (load_limit truck2) 40)
	(located truck3 distributor1)
	(= (current_load truck3) 0)
	(= (load_limit truck3) 40)
	(located hoist0 depot0)
	(available hoist0)
	(located hoist1 depot1)
	(available hoist1)
	(located hoist2 distributor0)
	(available hoist2)
	(located hoist3 distributor1)
	(available hoist3)
	(located hoist4 distributor1)
	(available hoist4)
	(located hoist5 depot1)
	(available hoist5)
	(located hoist6 depot1)
	(available hoist6)
	(located hoist7 distributor1)
	(available hoist7)
	(located crate0 depot1)
	(on crate0 pallet4)
	(= (weight crate0) 4)
	(located crate1 depot1)
	(on crate1 pallet1)
	(= (weight crate1) 8)
	(located crate2 depot0)
	(on crate2 pallet0)
	(= (weight crate2) 4)
	(located crate3 depot1)
	(on crate3 crate1)
	(= (weight crate3) 4)
	(located crate4 distributor0)
	(on crate4 pallet2)
	(= (weight crate4) 4)
	(located crate5 depot0)
	(on crate5 crate2)
	(= (weight crate5) 4)
	(= (fuel-cost) 0)
)

(:goal (and
		(on crate0 pallet3)
		(on crate2 pallet1)
		(on crate3 pallet0)
		(on crate4 crate3)
		(on crate5 pallet2)
	)
)

; (:metric minimize (fuel-cost))
)
