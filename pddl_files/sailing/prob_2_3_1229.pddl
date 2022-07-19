;; Enrico Scala (enricos83@gmail.com) and Miquel Ramirez (miquel.ramirez@gmail.com)
;;Setting seed to 1229
(define (problem instance_2_3_1229)

(:domain sailing)

(:objects
b0 b1  - agent
p0 p1 p2  - person
)

(:init
(= (x b0) -7)
(= (y b0) 0)
(= (x b1) -2)
(= (y b1) 0)
(= (d p0) 32)
(= (d p1) 110)
(= (d p2) 140)
(= (total-cost) 0))

(:goal
(and
(saved p0)
(saved p1)
(saved p2)))
(:metric minimize (total-cost))
)


