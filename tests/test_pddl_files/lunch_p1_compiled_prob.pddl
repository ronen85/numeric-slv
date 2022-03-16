(define (problem lunch_p1_compiled) (:domain lunch_compiled)

(:objects
ronen - agent
	alex - agent
	pizza - edible
	cake - edible)

(:init
	(act )
	(ready_g cake)
	(hungry_g alex)
	(ready_g pizza)
	(hungry_g ronen)
	(ready_ronen cake)
	(hungry_ronen alex)
	(ready_ronen pizza)
	(hungry_ronen ronen)
	(ready_alex cake)
	(hungry_alex alex)
	(ready_alex pizza)
	(hungry_alex ronen)
	(= (fats_got_g ronen) 0.0)
	(= (carbs_got_g ronen) 0.0)
	(= (protein_got_g ronen) 0.0)
	(= (fats_got_g alex) 0.0)
	(= (carbs_got_g alex) 0.0)
	(= (protein_got_g alex) 0.0)
	(= (total-cost_g ) 0.0)
	(= (zeta_0_g ) 0.0)
	(= (zeta_1_g ) 0.0)
	(= (fats_got_ronen ronen) 0.0)
	(= (carbs_got_ronen ronen) 0.0)
	(= (protein_got_ronen ronen) 0.0)
	(= (fats_got_ronen alex) 0.0)
	(= (carbs_got_ronen alex) 0.0)
	(= (protein_got_ronen alex) 0.0)
	(= (total-cost_ronen ) 0.0)
	(= (zeta_0_ronen ) 0.0)
	(= (zeta_1_ronen ) 0.0)
	(= (fats_got_alex ronen) 0.0)
	(= (carbs_got_alex ronen) 0.0)
	(= (protein_got_alex ronen) 0.0)
	(= (fats_got_alex alex) 0.0)
	(= (carbs_got_alex alex) 0.0)
	(= (protein_got_alex alex) 0.0)
	(= (total-cost_alex ) 0.0)
	(= (zeta_0_alex ) 0.0)
	(= (zeta_1_alex ) 0.0)
)

(:goal (and
	(failure )
	(fin_ronen )
	(fin_alex )))

(:metric minimize (total-cost ))

)