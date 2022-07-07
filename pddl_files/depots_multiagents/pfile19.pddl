(define (problem depotprob6178) (:domain depot)
(:objects
	a1 a2 - agent
	depot0 depot1 depot2 depot3 - depot
	distributor0 distributor1 distributor2 distributor3 - distributor
	truck0 truck1 truck2 truck3 - truck
	pallet0 pallet1 pallet2 pallet3 pallet4 pallet5 pallet6 pallet7 pallet8 pallet9 - pallet
	crate0 crate1 crate2 crate3 crate4 crate5 crate6 crate7 - crate
	hoist0 hoist1 hoist2 hoist3 hoist4 hoist5 hoist6 hoist7 - hoist)
(:init
	(located pallet0 depot0)
	(clear crate6)
	(located pallet1 depot1)
	(clear crate1)
	(located pallet2 depot2)
	(clear pallet2)
	(located pallet3 depot3)
	(clear crate7)
	(located pallet4 distributor0)
	(clear crate2)
	(located pallet5 distributor1)
	(clear crate5)
	(located pallet6 distributor2)
	(clear pallet6)
	(located pallet7 distributor3)
	(clear pallet7)
	(located pallet8 distributor2)
	(clear crate4)
	(located pallet9 depot3)
	(clear crate0)
	(located truck0 depot0)
	(= (current_load truck0) 0)
	(= (load_limit truck0) 20)
	(located truck1 distributor0)
	(= (current_load truck1) 0)
	(= (load_limit truck1) 40)
	(located truck2 depot2)
	(= (current_load truck2) 0)
	(= (load_limit truck2) 40)
	(located truck3 distributor3)
	(= (current_load truck3) 0)
	(= (load_limit truck3) 20)
	(located hoist0 depot0)
	(available hoist0)
	(located hoist1 depot1)
	(available hoist1)
	(located hoist2 depot2)
	(available hoist2)
	(located hoist3 depot3)
	(available hoist3)
	(located hoist4 distributor0)
	(available hoist4)
	(located hoist5 distributor1)
	(available hoist5)
	(located hoist6 distributor2)
	(available hoist6)
	(located hoist7 distributor3)
	(available hoist7)
	(located crate0 depot3)
	(on crate0 pallet9)
	(= (weight crate0) 8)
	(located crate1 depot1)
	(on crate1 pallet1)
	(= (weight crate1) 4)
	(located crate2 distributor0)
	(on crate2 pallet4)
	(= (weight crate2) 4)
	(located crate3 distributor1)
	(on crate3 pallet5)
	(= (weight crate3) 8)
	(located crate4 distributor2)
	(on crate4 pallet8)
	(= (weight crate4) 8)
	(located crate5 distributor1)
	(on crate5 crate3)
	(= (weight crate5) 4)
	(located crate6 depot0)
	(on crate6 pallet0)
	(= (weight crate6) 8)
	(located crate7 depot3)
	(on crate7 pallet3)
	(= (weight crate7) 4)
	(= (fuel-cost) 0)
)

(:goal (and
		(on crate0 pallet6)
		(on crate1 pallet8)
		(on crate3 crate1)
		(on crate4 pallet5)
		(on crate5 crate4)
		(on crate6 pallet4)
		(on crate7 crate6)
	)
)

; (:metric minimize (fuel-cost))
)
