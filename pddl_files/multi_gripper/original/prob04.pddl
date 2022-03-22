(define (problem num-gripper-x-4)
   (:domain multi-gripper-num)
   (:objects rooma roomb roomc roomd - room 
             ball12 ball11 ball10
             ball9 ball8 ball7 ball6 ball5 ball4 ball3 ball2 ball1 - ball 
             r1 r2 - robby
             left1 right1 left2 right2 - gripper)
   (:init (= (weight ball10) 2)
          (= (weight ball9) 2)
          (= (weight ball8) 1)
          (= (weight ball7) 1)
          (= (weight ball6) 1)
          (= (weight ball5) 1)
          (= (weight ball4) 1)
          (= (weight ball3) 1)
          (= (weight ball2) 1)
          (= (weight ball1) 1)
          (at ball10 rooma)
          (at ball9 rooma)
          (at ball8 rooma)
          (at ball7 rooma)
          (at ball6 rooma)
          (at ball5 rooma)
          (at ball4 rooma)
          (at ball3 rooma)
          (at ball2 rooma)
          (at ball1 rooma)
          
          (at-robby r1 rooma)
          (at-robby r2 rooma)
          (free left1)
          (free right1)
          (free left2)
          (free right2)
          (mount left1 r1)
          (mount right1 r1)
          (mount left2 r2)
          (mount right2 r2)
          
          (door rooma roomb)
          (door roomb rooma)
          (door roomd roomb)
          (door roomb roomd)
          (door rooma roomc)
          (door roomc rooma)
          
          (= (current_load r1) 0)
          (= (load_limit r1) 4)
          (= (current_load r2) 0)
          (= (load_limit r2) 4)
          (= (cost) 0)) 
          
   (:goal (and (at ball10 roomb)
               (at ball9 roomb)
               (at ball8 roomd)
               (at ball7 roomd)
               (at ball6 roomd)
               (at ball5 roomd)
               (at ball4 roomc)
               (at ball3 roomc)
               (at ball2 roomc)
               (at ball1 roomc)))
               
               (:metric minimize (cost))
               
)
