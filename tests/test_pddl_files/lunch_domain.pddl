(define (domain lunch)
    (:requirements :typing :fluents)

(:types edible person - object)

(:predicates 
    (ready ?e - edible)
    (hungry ?p - person)
    (satisfied ?p - person)
)

(:functions 
    (fats_in ?e - edible)
    (carbs_in ?e - edible)
    (protein_in ?e - edible)
    (fats_got ?p - person)
    (carbs_got ?p - person)
    (protein_got ?p - person)
    (fats_need ?p - person)
    (carbs_need ?p - person)
    (protein_need ?p - person)
    (calorie_need ?p - person)
)


(:action eat 
:parameters (?p - person ?e - edible)
:precondition (and (ready ?e))
:effect (and 
    (not (ready ?e))
    (increase (fats_got ?p) (fats_in ?e))
    (increase (carbs_got ?p) (carbs_in ?e))
    (increase (protein_got ?p) (protein_in ?e))
)
)

(:action finish 
:parameters (?p - person)
:precondition (and 
    (hungry ?p) 
    (>= (fats_got ?p) 
    (fats_need ?p)) 
    (>= (protein_got ?p) (protein_need ?p)) 
    (>= (carbs_got ?p) (carbs_need ?p))     
    ; (>= (+ (+ (* (fats_got ?p) 8.0) (* (protein_got ?p) 4.0)) (* (carbs_got ?p) 4.0)) (calorie_need ?p))    
    (>= (+ (* (fats_got ?p) 8.0) (* (protein_got ?p) 4.0)) (calorie_need ?p))    
    ; (>= (+ (* (fats_got ?p) 8.0) (* (protein_got ?p) 4.0) (* (carbs_got ?p) 4.0)) (calorie_need ?p)) 
    ) 
:effect (and 
    (not (hungry ?p))
    (satisfied ?p)
)
)

)