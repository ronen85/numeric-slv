;; Enrico Scala (enricos83@gmail.com) and Miquel Ramirez (miquel.ramirez@gmail.com)
;;Setting seed to 1229
(define (problem instance_4_4_1229)

(:domain sailing)

(:objects
b0 b1 b2 b3  - agent
p0 p1 p2 p3  - person
)

(:init
(= (x b0) -2)
(= (y b0) 0)
(= (x b1) 0)
(= (y b1) 0)
(= (x b2) -5)
(= (y b2) 0)
(= (x b3) -5)
(= (y b3) 0)


(= (d p0) 32)
(= (d p1) 110)
(= (d p2) 140)
(= (d p3) 26)

(= (total-cost) 0)
)

(:goal
(and
(saved p0)
(saved p1)
(saved p2)
(saved p3)

)
)
(:metric minimize (total-cost))
)


