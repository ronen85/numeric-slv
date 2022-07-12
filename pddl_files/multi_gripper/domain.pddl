;; Unonimized
(define (domain multi-gripper-num)
  (:types room ball gripper agent - object)
   (:predicates (at-robby ?r - agent ?x - room)
		 (at ?b - ball ?x - room)
		 (door ?x - room ?y - room)
		 (free ?g - gripper)
		 (in-g ?b - ball ?g - gripper)
		 (in-tray ?b - ball ?r - agent) 
		 (mount ?g - gripper ?r - agent))
		
   (:functions 
	(load_limit ?r - agent) 
	(current_load ?r - agent) 
	(weight ?b - ball)
	(cost))

   (:action move
       :parameters (?r - agent ?x - room ?y - room) 
       :precondition (and (at-robby ?r ?x)
                          (door ?x ?y))
       :effect (and  (at-robby ?r ?y)
		     (not (at-robby ?r ?x))
		     (increase (cost) 2)
		     ))



   (:action pick
       :parameters (?r - agent ?b - ball ?x - room ?g - gripper)
       :precondition  (and (at ?b ?x) (at-robby ?r ?x) (free ?g) (mount ?g ?r)
                           (<= (+ (current_load ?r) (weight ?b)) (load_limit ?r)))
       :effect (and (in-g ?b ?g)
		    (not (at ?b ?x)) 
		    (not (free ?g))
		    (increase (current_load ?r) (weight ?b))
		    (increase (cost) 1)
		    ))
		    

   (:action drop
       :parameters (?r - agent ?b - ball ?x - room ?g - gripper)
       :precondition (and (in-g ?b ?g) 
                     (at-robby ?r ?x) 
                     (mount ?g ?r))
       :effect (and (free ?g)
                    (at ?b ?x) 
                    (not (in-g ?b ?g))
                    (decrease (current_load ?r) (weight ?b))
                    (increase (cost) 1)
                    ))
   
   (:action to-tray
       :parameters (?r - agent ?b - ball ?g - gripper) 
       :precondition (and (in-g ?b ?g)
                          (mount ?g ?r))
       :effect (and (free ?g)
		     (not (in-g ?b ?g))
		     (in-tray ?b ?r)
		     (increase (cost) 0)
		     ))
		  
   (:action from-tray
       :parameters (?r - agent ?b - ball ?g - gripper) 
       :precondition (and  (in-tray ?b ?r)
                           (mount ?g ?r)
                           (free ?g))
       :effect (and  (not (free ?g))
		     (in-g ?b ?g)
		     (not (in-tray ?b ?r))
		     (increase (cost) 0)
		     ))
)
