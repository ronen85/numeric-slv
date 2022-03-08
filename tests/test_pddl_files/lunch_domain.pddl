(define (domain lunch)
    (:requirements :typing :fluents)

(:types edible agent - object)

(:predicates 
    (ready ?e - edible)
    (hungry ?p - agent)
    (satisfied ?p - agent)
)

(:functions 
    (fats_in ?e - edible)
    (carbs_in ?e - edible)
    (protein_in ?e - edible)
    (fats_got ?p - agent)
    (carbs_got ?p - agent)
    (protein_got ?p - agent)
    (fats_need ?p - agent)
    (carbs_need ?p - agent)
    (protein_need ?p - agent)
    (calorie_need ?p - agent)
    (cost)
)


(:action eat 
:parameters (?p - agent ?e - edible)
:precondition (and (ready ?e))
:effect (and 
    (not (ready ?e))
    (increase (fats_got ?p) (fats_in ?e))
    (increase (carbs_got ?p) (carbs_in ?e))
    (increase (protein_got ?p) (protein_in ?e))
    (increase (cost) 1)
)
)

(:action finish 
:parameters (?p - agent)
:precondition (and 
    (hungry ?p) 
    (>= (fats_got ?p) 
    (fats_need ?p)) 
    (>= (protein_got ?p) (protein_need ?p)) 
    (>= (carbs_got ?p) (carbs_need ?p))     
    (>= (+ (* (+ (carbs_got ?p) (protein_got ?p)) 4.0) (* (fats_got ?p) 8.0)) (calorie_need ?p))
    ) 
:effect (and 
    (not (hungry ?p))
    (satisfied ?p)
)
)

)
