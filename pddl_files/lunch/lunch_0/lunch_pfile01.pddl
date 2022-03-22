(define (problem lunch_p1) 
(:domain lunch)
(:objects ronen alex - agent
          pizza - edible
          cake - edible
          )

(:init
    (hungry ronen)
    (hungry alex)
    (ready pizza)
    (ready cake)
    (= (fats_in pizza) 1)
    (= (carbs_in pizza) 1)
    (= (protein_in pizza) 1)
    (= (fats_in cake) 1)
    (= (carbs_in cake) 1)
    (= (protein_in cake) 1)
    (= (fats_got ronen) 0)
    (= (carbs_got ronen) 0)
    (= (protein_got ronen) 0)
    (= (fats_need ronen) 1)
    (= (carbs_need ronen) 1)
    (= (protein_need ronen) 1)
    (= (calorie_need ronen) 1)
    (= (fats_got alex) 0)
    (= (carbs_got alex) 0)
    (= (protein_got alex) 0)
    (= (fats_need alex) 1)
    (= (carbs_need alex) 1)
    (= (protein_need alex) 1)
    (= (calorie_need alex) 1)    
)

(:goal
(and
(satisfied ronen) 
(satisfied alex) 
(>= (protein_got ronen) 0)
))


)
