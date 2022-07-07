(define (problem depotprob9876) (:domain depot)
(:objects
	depot0 depot1 depot2 - depot
	distributor0 distributor1 distributor2 - distributor
	truck0 truck1 - truck
	pallet0 pallet1 pallet2 pallet3 pallet4 pallet5 - pallet
	crate0 crate1 crate2 crate3 crate4 crate5 crate6 crate7 crate8 crate9 crate10 crate11 crate12 crate13 crate14 - crate
	hoist0 hoist1 hoist2 hoist3 hoist4 hoist5 - hoist)
(:init
	(located pallet0 depot0)
	(clear pallet0)
	(located pallet1 depot1)
	(clear crate12)
	(located pallet2 depot2)
	(clear pallet2)
	(located pallet3 distributor0)
	(clear crate4)
	(located pallet4 distributor1)
	(clear crate14)
	(located pallet5 distributor2)
	(clear crate13)
	(located truck0 distributor1)
	(= (current_load truck0) 0)
	(= (load_limit truck0) 20)
	(located truck1 depot1)
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
	(located crate0 distributor2)
	(on crate0 pallet5)
	(= (weight crate0) 8)
	(located crate1 depot1)
	(on crate1 pallet1)
	(= (weight crate1) 8)
	(located crate2 distributor0)
	(on crate2 pallet3)
	(= (weight crate2) 8)
	(located crate3 distributor2)
	(on crate3 crate0)
	(= (weight crate3) 8)
	(located crate4 distributor0)
	(on crate4 crate2)
	(= (weight crate4) 8)
	(located crate5 depot1)
	(on crate5 crate1)
	(= (weight crate5) 4)
	(located crate6 distributor2)
	(on crate6 crate3)
	(= (weight crate6) 4)
	(located crate7 distributor2)
	(on crate7 crate6)
	(= (weight crate7) 4)
	(located crate8 distributor2)
	(on crate8 crate7)
	(= (weight crate8) 4)
	(located crate9 distributor2)
	(on crate9 crate8)
	(= (weight crate9) 4)
	(located crate10 depot1)
	(on crate10 crate5)
	(= (weight crate10) 4)
	(located crate11 distributor1)
	(on crate11 pallet4)
	(= (weight crate11) 2)
	(located crate12 depot1)
	(on crate12 crate10)
	(= (weight crate12) 2)
	(located crate13 distributor2)
	(on crate13 crate9)
	(= (weight crate13) 2)
	(located crate14 distributor1)
	(on crate14 crate11)
	(= (weight crate14) 2)
	(= (fuel-cost) 0)
)

(:goal (and

		(on crate5 pallet0)

		
		(on crate13 pallet1)
		(on crate11 crate13)
		(on crate14 crate11)
		
		(on crate9 pallet2)
		(on crate6 crate9)		
					
		(on crate0 pallet4)
		(on crate2 crate0)
			
		(on crate10 pallet5)
		(on crate1 crate10)
	)
)

(:metric minimize (fuel-cost)))
