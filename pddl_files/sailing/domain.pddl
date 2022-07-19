;; Enrico Scala (enricos83@gmail.com) and Miquel Ramirez (miquel.ramirez@gmail.com)
(define (domain sailing)

(:types agent - object person - object)

(:predicates
(saved ?t - person)
)

(:functions
(x ?b - agent)
(y ?b - agent)
(d ?t - person)
(total-cost))


(:action go-north-east
:parameters (?b - agent)
:precondition (and )
:effect (and
(increase (total-cost) 1.0) (increase (x ?b) 1.5) (increase (y ?b) 1.5))
)

(:action go-north-west
:parameters (?b - agent)
:precondition (and )
:effect (and
(increase (total-cost) 1.0) (decrease (x ?b) 1.5) (increase (y ?b) 1.5))
)

(:action go-est
:parameters (?b - agent)
:precondition (and )
:effect (and
(increase (total-cost) 1.0) (increase (x ?b) 3))
)

(:action go-west
:parameters (?b - agent)
:precondition (and )
:effect (and
(increase (total-cost) 1.0) (decrease (x ?b) 3))
)

(:action go-south-west
:parameters(?b - agent)
:precondition (and )
:effect (and
(increase (total-cost) 1.0) (increase (x ?b) 2) (decrease (y ?b) 2))
)

(:action go-south-east
:parameters(?b - agent)
:precondition (and )
:effect (and
(increase (total-cost) 1.0) (decrease (x ?b) 2) (decrease (y ?b) 2))
)

(:action go-south
:parameters(?b - agent)
:precondition (and )
:effect (and
(increase (total-cost) 1.0) (decrease (y ?b) 2))
)

(:action save-person
:parameters(?b - agent ?t - person)
:precondition ( and
(not (saved ?t))
(>= (+ (x ?b) (y ?b)) (d ?t))
(>= (- (y ?b) (x ?b)) (d ?t))
(<= (+ (x ?b) (y ?b)) (+ (d ?t) 25))
(<= (- (y ?b) (x ?b)) (+ (d ?t) 25))
)
:effect (and
(increase (total-cost) 1.0) (saved ?t))
)

)
