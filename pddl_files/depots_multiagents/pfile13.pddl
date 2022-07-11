(define (problem depotprob5646) (:domain depot)
(:objects
	a1 a2 - agent
	depot0 depot1 depot2 - depot
	distributor0 distributor1 distributor2 - distributor
	truck0 truck1 - truck
	pallet0 pallet1 pallet2 pallet3 pallet4 pallet5 pallet6 pallet7 pallet8 pallet9 - pallet
	crate0 crate1 crate2 crate3 crate4 crate5 - crate
	hoist0 hoist1 hoist2 hoist3 hoist4 hoist5 - hoist)
(:init
	(located pallet0 depot0)
	(clear crate2)
	(located pallet1 depot1)
	(clear pallet1)
	(located pallet2 depot2)
	(clear crate5)
	(located pallet3 distributor0)
	(clear crate4)
	(located pallet4 distributor1)
	(clear pallet4)
	(located pallet5 distributor2)
	(clear pallet5)
	(located pallet6 distributor1)
	(clear pallet6)
	(located pallet7 depot0)
	(clear pallet7)
	(located pallet8 depot0)
	(clear crate3)
	(located pallet9 distributor0)
	(clear pallet9)
	(located truck0 distributor1)
	(= (current_load truck0) 0)
	(= (load_limit truck0) 40)
	(located truck1 depot0)
	(= (current_load truck1) 0)
	(= (load_limit truck1) 20)
	(located hoist0 depot0)
	(available hoist0)
	(located hoist1 depot1)
	(available hoist1)
	(located hoist2 depot2)
	(available hoist2)
	(located hoist3 distributor0)
	(available hoist3)
	(located hoist4 distributor1)
	(available hoist4)
	(located hoist5 distributor2)
	(available hoist5)
	(located crate0 depot2)
	(on crate0 pallet2)
	(= (weight crate0) 8)
	(located crate1 depot2)
	(on crate1 crate0)
	(= (weight crate1) 24)
	(located crate2 depot0)
	(on crate2 pallet0)
	(= (weight crate2) 8)
	(located crate3 depot0)
	(on crate3 pallet8)
	(= (weight crate3) 24)
	(located crate4 distributor0)
	(on crate4 pallet3)
	(= (weight crate4) 8)
	(located crate5 depot2)
	(on crate5 crate1)
	(= (weight crate5) 8)
	(= (fuel-cost) 0)
)

(:goal (and
		(on crate0 pallet0)
		(on crate1 pallet5)
		(on crate2 pallet4)
		(on crate3 pallet7)
		(on crate4 pallet9)
		(on crate5 pallet1)
	)
)

(:metric minimize (fuel-cost))
)
