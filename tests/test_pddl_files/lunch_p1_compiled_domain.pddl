(define (domain lunch_compiled)

(:requirements  :fluents :typing)

(:types
	edible agent - object
)

(:predicates
	(ready_g ?e - edible)
	(hungry_g ?p - agent)
	(satisfied_g ?p - agent)
	(ready_ronen ?e - edible)
	(hungry_ronen ?p - agent)
	(satisfied_ronen ?p - agent)
	(ready_alex ?e - edible)
	(hungry_alex ?p - agent)
	(satisfied_alex ?p - agent)
	(waiting_ronen )
	(waiting_alex )
	(wt_ready_cake )
	(wt_ready_cake )
	(wt_ready_pizza )
	(wt_ready_pizza )
	(wt_protein_got_ronen_1.0 )
	(wt_protein_got_alex_1.0 )
	(fin_ronen )
	(fin_alex )
	(act )
	(failure )
)

(:functions
	(fats_got_g ?p - agent)
	(carbs_got_g ?p - agent)
	(protein_got_g ?p - agent)
	(zeta_0_g )
	(zeta_1_g )
	(fats_got_ronen ?p - agent)
	(carbs_got_ronen ?p - agent)
	(protein_got_ronen ?p - agent)
	(zeta_0_ronen )
	(zeta_1_ronen )
	(fats_got_alex ?p - agent)
	(carbs_got_alex ?p - agent)
	(protein_got_alex ?p - agent)
	(zeta_0_alex )
	(zeta_1_alex )
)


(:action eat_alex_pizza_s
:parameters ()
:precondition (and
	(act )
	(not (waiting_alex ))
	(ready_alex pizza)
	(ready_g pizza)
	(hungry_alex alex)
	(hungry_g alex)
	(or
	(not (wt_protein_got_alex_1.0 ))
	(< (protein_got alex) 0.0)))
:effect (and
	(not (ready_g pizza))
	(not (ready_alex pizza))
	(increase (fats_got_alex alex) 1.0)
	(increase (fats_got_g alex) 1.0)
	(increase (carbs_got_alex alex) 1.0)
	(increase (carbs_got_g alex) 1.0)
	(increase (protein_got_alex alex) 1.0)
	(increase (protein_got_g alex) 1.0)
	(increase (zeta_0_alex ) 16.0)
	(increase (zeta_0_g ) 16.0)
))

(:action eat_alex_cake_s
:parameters ()
:precondition (and
	(act )
	(not (waiting_alex ))
	(ready_alex cake)
	(ready_g cake)
	(hungry_alex alex)
	(hungry_g alex)
	(or
	(not (wt_protein_got_alex_1.0 ))
	(< (protein_got alex) 0.0)))
:effect (and
	(not (ready_g cake))
	(not (ready_alex cake))
	(increase (fats_got_alex alex) 1.0)
	(increase (fats_got_g alex) 1.0)
	(increase (carbs_got_alex alex) 1.0)
	(increase (carbs_got_g alex) 1.0)
	(increase (protein_got_alex alex) 1.0)
	(increase (protein_got_g alex) 1.0)
	(increase (zeta_0_alex ) 16.0)
	(increase (zeta_0_g ) 16.0)
))

(:action finish_alex_s
:parameters ()
:precondition (and
	(act )
	(not (waiting_alex ))
	(hungry_alex alex)
	(hungry_g alex)
	(>= (fats_got_alex alex) 1.0)
	(>= (fats_got_g alex) 1.0)
	(>= (protein_got_alex alex) 1.0)
	(>= (protein_got_g alex) 1.0)
	(>= (carbs_got_alex alex) 1.0)
	(>= (carbs_got_g alex) 1.0)
	(>= (zeta_0_alex ) 1.0)
	(>= (zeta_0_g ) 1.0))
:effect (and
	(satisfied_g alex)
	(satisfied_alex alex)
	(not (hungry_g alex))
	(not (hungry_alex alex))
))

(:action finish_ronen_s
:parameters ()
:precondition (and
	(act )
	(not (waiting_ronen ))
	(hungry_ronen ronen)
	(hungry_g ronen)
	(>= (fats_got_ronen ronen) 1.0)
	(>= (fats_got_g ronen) 1.0)
	(>= (protein_got_ronen ronen) 1.0)
	(>= (protein_got_g ronen) 1.0)
	(>= (carbs_got_ronen ronen) 1.0)
	(>= (carbs_got_g ronen) 1.0)
	(>= (zeta_1_ronen ) 1.0)
	(>= (zeta_1_g ) 1.0))
:effect (and
	(satisfied_g ronen)
	(satisfied_ronen ronen)
	(not (hungry_g ronen))
	(not (hungry_ronen ronen))
))

(:action eat_ronen_pizza_s
:parameters ()
:precondition (and
	(act )
	(not (waiting_ronen ))
	(ready_ronen pizza)
	(ready_g pizza)
	(hungry_ronen ronen)
	(hungry_g ronen)
	(or
	(not (wt_protein_got_ronen_1.0 ))
	(< (protein_got ronen) 0.0)))
:effect (and
	(not (ready_g pizza))
	(not (ready_ronen pizza))
	(increase (fats_got_ronen ronen) 1.0)
	(increase (fats_got_g ronen) 1.0)
	(increase (carbs_got_ronen ronen) 1.0)
	(increase (carbs_got_g ronen) 1.0)
	(increase (protein_got_ronen ronen) 1.0)
	(increase (protein_got_g ronen) 1.0)
	(increase (zeta_1_ronen ) 16.0)
	(increase (zeta_1_g ) 16.0)
))

(:action eat_ronen_cake_s
:parameters ()
:precondition (and
	(act )
	(not (waiting_ronen ))
	(ready_ronen cake)
	(ready_g cake)
	(hungry_ronen ronen)
	(hungry_g ronen)
	(or
	(not (wt_protein_got_ronen_1.0 ))
	(< (protein_got ronen) 0.0)))
:effect (and
	(not (ready_g cake))
	(not (ready_ronen cake))
	(increase (fats_got_ronen ronen) 1.0)
	(increase (fats_got_g ronen) 1.0)
	(increase (carbs_got_ronen ronen) 1.0)
	(increase (carbs_got_g ronen) 1.0)
	(increase (protein_got_ronen ronen) 1.0)
	(increase (protein_got_g ronen) 1.0)
	(increase (zeta_1_ronen ) 16.0)
	(increase (zeta_1_g ) 16.0)
))

(:action eat_alex_pizza_pf
:parameters ()
:precondition (and
	(act )
	(not (waiting_alex ))
	(ready_alex pizza)
	(hungry_alex alex)
	(ready_g pizza)
	(not (hungry_g alex)))
:effect (and
	(failure )
	(not (ready_alex pizza))
	(increase (fats_got_alex alex) 1.0)
	(increase (carbs_got_alex alex) 1.0)
	(increase (protein_got_alex alex) 1.0)
	(increase (zeta_0_alex ) 16.0)
))

(:action eat_alex_cake_pf
:parameters ()
:precondition (and
	(act )
	(not (waiting_alex ))
	(ready_alex cake)
	(hungry_alex alex)
	(ready_g cake)
	(not (hungry_g alex)))
:effect (and
	(failure )
	(not (ready_alex cake))
	(increase (fats_got_alex alex) 1.0)
	(increase (carbs_got_alex alex) 1.0)
	(increase (protein_got_alex alex) 1.0)
	(increase (zeta_0_alex ) 16.0)
))

(:action finish_alex_pf
:parameters ()
:precondition (and
	(act )
	(not (waiting_alex ))
	(hungry_alex alex)
	(not (hungry_g alex))
	(>= (fats_got_alex alex) 1.0)
	(>= (protein_got_alex alex) 1.0)
	(>= (carbs_got_alex alex) 1.0)
	(>= (zeta_0_alex ) 1.0)
	(>= (protein_got_g alex) 1.0))
:effect (and
	(satisfied_alex alex)
	(failure )
	(not (hungry_alex alex))
))

(:action finish_ronen_pf
:parameters ()
:precondition (and
	(act )
	(not (waiting_ronen ))
	(hungry_ronen ronen)
	(not (hungry_g ronen))
	(>= (fats_got_ronen ronen) 1.0)
	(>= (protein_got_ronen ronen) 1.0)
	(>= (carbs_got_ronen ronen) 1.0)
	(>= (zeta_1_ronen ) 1.0)
	(>= (protein_got_g ronen) 1.0))
:effect (and
	(satisfied_ronen ronen)
	(failure )
	(not (hungry_ronen ronen))
))

(:action eat_ronen_pizza_pf
:parameters ()
:precondition (and
	(act )
	(not (waiting_ronen ))
	(ready_ronen pizza)
	(hungry_ronen ronen)
	(ready_g pizza)
	(not (hungry_g ronen)))
:effect (and
	(failure )
	(not (ready_ronen pizza))
	(increase (fats_got_ronen ronen) 1.0)
	(increase (carbs_got_ronen ronen) 1.0)
	(increase (protein_got_ronen ronen) 1.0)
	(increase (zeta_1_ronen ) 16.0)
))

(:action eat_ronen_cake_pf
:parameters ()
:precondition (and
	(act )
	(not (waiting_ronen ))
	(ready_ronen cake)
	(hungry_ronen ronen)
	(ready_g cake)
	(not (hungry_g ronen)))
:effect (and
	(failure )
	(not (ready_ronen cake))
	(increase (fats_got_ronen ronen) 1.0)
	(increase (carbs_got_ronen ronen) 1.0)
	(increase (protein_got_ronen ronen) 1.0)
	(increase (zeta_1_ronen ) 16.0)
))

(:action finish_alex_nf
:parameters ()
:precondition (and
	(act )
	(not (waiting_alex ))
	(hungry_alex alex)
	(>= (fats_got_alex alex) 1.0)
	(>= (protein_got_alex alex) 1.0)
	(>= (carbs_got_alex alex) 1.0)
	(>= (zeta_0_alex ) 1.0)
	(>= (protein_got_g alex) 1.0)
	(or
	(< (zeta_0_g ) 1.0)
	(< (carbs_got_g alex) 1.0)
	(< (fats_got_g alex) 1.0)))
:effect (and
	(satisfied_alex alex)
	(failure )
	(not (hungry_alex alex))
))

(:action finish_ronen_nf
:parameters ()
:precondition (and
	(act )
	(not (waiting_ronen ))
	(hungry_ronen ronen)
	(>= (fats_got_ronen ronen) 1.0)
	(>= (protein_got_ronen ronen) 1.0)
	(>= (carbs_got_ronen ronen) 1.0)
	(>= (zeta_1_ronen ) 1.0)
	(>= (protein_got_g ronen) 1.0)
	(or
	(< (fats_got_g ronen) 1.0)
	(< (carbs_got_g ronen) 1.0)
	(< (zeta_1_g ) 1.0)))
:effect (and
	(satisfied_ronen ronen)
	(failure )
	(not (hungry_ronen ronen))
))

(:action eat_alex_pizza_wt_ready_pizza
:parameters ()
:precondition (and
	(act )
	(not (waiting_alex ))
	(ready_alex pizza)
	(hungry_alex alex)
	(not (ready_g pizza)))
:effect (and
	(failure )
	(waiting_alex )
	(wt_ready_pizza )
	(not (ready_alex pizza))
	(increase (fats_got_alex alex) 1.0)
	(increase (carbs_got_alex alex) 1.0)
	(increase (protein_got_alex alex) 1.0)
	(increase (zeta_0_alex ) 16.0)
))

(:action eat_alex_cake_wt_ready_cake
:parameters ()
:precondition (and
	(act )
	(not (waiting_alex ))
	(ready_alex cake)
	(hungry_alex alex)
	(not (ready_g cake)))
:effect (and
	(failure )
	(waiting_alex )
	(wt_ready_cake )
	(not (ready_alex cake))
	(increase (fats_got_alex alex) 1.0)
	(increase (carbs_got_alex alex) 1.0)
	(increase (protein_got_alex alex) 1.0)
	(increase (zeta_0_alex ) 16.0)
))

(:action eat_ronen_pizza_wt_ready_pizza
:parameters ()
:precondition (and
	(act )
	(not (waiting_ronen ))
	(ready_ronen pizza)
	(hungry_ronen ronen)
	(not (ready_g pizza)))
:effect (and
	(failure )
	(waiting_ronen )
	(wt_ready_pizza )
	(not (ready_ronen pizza))
	(increase (fats_got_ronen ronen) 1.0)
	(increase (carbs_got_ronen ronen) 1.0)
	(increase (protein_got_ronen ronen) 1.0)
	(increase (zeta_1_ronen ) 16.0)
))

(:action eat_ronen_cake_wt_ready_cake
:parameters ()
:precondition (and
	(act )
	(not (waiting_ronen ))
	(ready_ronen cake)
	(hungry_ronen ronen)
	(not (ready_g cake)))
:effect (and
	(failure )
	(waiting_ronen )
	(wt_ready_cake )
	(not (ready_ronen cake))
	(increase (fats_got_ronen ronen) 1.0)
	(increase (carbs_got_ronen ronen) 1.0)
	(increase (protein_got_ronen ronen) 1.0)
	(increase (zeta_1_ronen ) 16.0)
))

(:action finish_alex_wt_protein_got_alex_1.0
:parameters ()
:precondition (and
	(act )
	(not (waiting_alex ))
	(hungry_alex alex)
	(>= (fats_got_alex alex) 1.0)
	(>= (protein_got_alex alex) 1.0)
	(>= (carbs_got_alex alex) 1.0)
	(>= (zeta_0_alex ) 1.0)
	(< (protein_got_g alex) 1.0))
:effect (and
	(satisfied_alex alex)
	(failure )
	(waiting_alex )
	(wt_protein_got_alex_1.0 )
	(not (hungry_alex alex))
))

(:action finish_ronen_wt_protein_got_ronen_1.0
:parameters ()
:precondition (and
	(act )
	(not (waiting_ronen ))
	(hungry_ronen ronen)
	(>= (fats_got_ronen ronen) 1.0)
	(>= (protein_got_ronen ronen) 1.0)
	(>= (carbs_got_ronen ronen) 1.0)
	(>= (zeta_1_ronen ) 1.0)
	(< (protein_got_g ronen) 1.0))
:effect (and
	(satisfied_ronen ronen)
	(failure )
	(waiting_ronen )
	(wt_protein_got_ronen_1.0 )
	(not (hungry_ronen ronen))
))

(:action eat_alex_pizza_wt
:parameters ()
:precondition (and
	(act )
	(waiting_alex )
	(ready_alex pizza)
	(hungry_alex alex))
:effect (and
	(not (ready_alex pizza))
	(increase (fats_got_alex alex) 1.0)
	(increase (carbs_got_alex alex) 1.0)
	(increase (protein_got_alex alex) 1.0)
	(increase (zeta_0_alex ) 16.0)
))

(:action eat_alex_cake_wt
:parameters ()
:precondition (and
	(act )
	(waiting_alex )
	(ready_alex cake)
	(hungry_alex alex))
:effect (and
	(not (ready_alex cake))
	(increase (fats_got_alex alex) 1.0)
	(increase (carbs_got_alex alex) 1.0)
	(increase (protein_got_alex alex) 1.0)
	(increase (zeta_0_alex ) 16.0)
))

(:action finish_alex_wt
:parameters ()
:precondition (and
	(act )
	(waiting_alex )
	(hungry_alex alex)
	(>= (fats_got_alex alex) 1.0)
	(>= (protein_got_alex alex) 1.0)
	(>= (carbs_got_alex alex) 1.0)
	(>= (zeta_0_alex ) 1.0))
:effect (and
	(satisfied_alex alex)
	(not (hungry_alex alex))
))

(:action finish_ronen_wt
:parameters ()
:precondition (and
	(act )
	(waiting_ronen )
	(hungry_ronen ronen)
	(>= (fats_got_ronen ronen) 1.0)
	(>= (protein_got_ronen ronen) 1.0)
	(>= (carbs_got_ronen ronen) 1.0)
	(>= (zeta_1_ronen ) 1.0))
:effect (and
	(satisfied_ronen ronen)
	(not (hungry_ronen ronen))
))

(:action eat_ronen_pizza_wt
:parameters ()
:precondition (and
	(act )
	(waiting_ronen )
	(ready_ronen pizza)
	(hungry_ronen ronen))
:effect (and
	(not (ready_ronen pizza))
	(increase (fats_got_ronen ronen) 1.0)
	(increase (carbs_got_ronen ronen) 1.0)
	(increase (protein_got_ronen ronen) 1.0)
	(increase (zeta_1_ronen ) 16.0)
))

(:action eat_ronen_cake_wt
:parameters ()
:precondition (and
	(act )
	(waiting_ronen )
	(ready_ronen cake)
	(hungry_ronen ronen))
:effect (and
	(not (ready_ronen cake))
	(increase (fats_got_ronen ronen) 1.0)
	(increase (carbs_got_ronen ronen) 1.0)
	(increase (protein_got_ronen ronen) 1.0)
	(increase (zeta_1_ronen ) 16.0)
))

(:action end_s_ronen
:parameters ()
:precondition (and
	(not (fin_ronen ))
	(satisfied_ronen ronen)
	(satisfied_g ronen)
	(>= (protein_got_ronen ronen) 0.0)
	(>= (protein_got_g ronen) 0.0))
:effect (and
	(fin_ronen )
	(not (act ))
))

(:action end_s_alex
:parameters ()
:precondition (and
	(not (fin_alex ))
	(satisfied_alex alex)
	(satisfied_g alex))
:effect (and
	(fin_alex )
	(not (act ))
))

(:action end_f_ronen
:parameters ()
:precondition (and
	(not (fin_ronen ))
	(satisfied_ronen ronen)
	(>= (protein_got_ronen ronen) 0.0)
	(or
	(not (satisfied_g ronen))
	(< (protein_got_g ronen) 0.0)))
:effect (and
	(fin_ronen )
	(failure )
	(not (act ))
))

(:action end_f_alex
:parameters ()
:precondition (and
	(not (fin_alex ))
	(satisfied_alex alex)
	(not (satisfied_g alex)))
:effect (and
	(fin_alex )
	(failure )
	(not (act ))
))

(:action end_w_ronen
:parameters ()
:precondition (and
	(not (fin_ronen ))
	(waiting_ronen )
	(satisfied_ronen ronen)
	(>= (protein_got_ronen ronen) 0.0))
:effect (and
	(fin_ronen )
	(not (act ))
))

(:action end_w_alex
:parameters ()
:precondition (and
	(not (fin_alex ))
	(waiting_alex )
	(satisfied_alex alex))
:effect (and
	(fin_alex )
	(not (act ))
))
)