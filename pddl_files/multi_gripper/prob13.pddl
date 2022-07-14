(define (problem num-gripper-x-13)
   (:domain multi-gripper-num)
   (:objects rooma roomb roomc roomd roome - room
             ball28
             ball27 ball26 ball25 ball24 ball23 ball22 ball21 ball20 ball19
             ball18 ball17 ball16 ball15 ball14 ball13 ball12 ball11 ball10
             ball9 ball8 ball7 ball6 ball5 ball4 ball3 ball2 ball1 - ball 
             r1 r2 r3 - agent
             left1 right1 left2 right2 left3 right3 - gripper)
             
   (:init (= (weight ball28) 2)
          (= (weight ball27) 2)
          (= (weight ball26) 2)
          (= (weight ball25) 2)
          (= (weight ball24) 1)
          (= (weight ball23) 1)
          (= (weight ball22) 1)
          (= (weight ball21) 1)
          (= (weight ball20) 1)
          (= (weight ball19) 1)
          (= (weight ball18) 1)
          (= (weight ball17) 1)
          (= (weight ball16) 1)
          (= (weight ball15) 1)
          (= (weight ball14) 1)
          (= (weight ball13) 1)
          (= (weight ball12) 1)
          (= (weight ball11) 1)
          (= (weight ball10) 1)
          (= (weight ball9) 1)
          (= (weight ball8) 1)
          (= (weight ball7) 1)
          (= (weight ball6) 1)
          (= (weight ball5) 1)
          (= (weight ball4) 2)
          (= (weight ball3) 2)
          (= (weight ball2) 2)
          (= (weight ball1) 2)

          (at ball28 roome)
          (at ball27 roome)
          (at ball26 roome)
          (at ball25 roome)
          (at ball24 roomd)
          (at ball23 roomd)
          (at ball22 roomd)
          (at ball21 roomd)
          (at ball20 roomc)
          (at ball19 roomc)
          (at ball18 roomc)
          (at ball17 roomc)
          (at ball16 rooma)
          (at ball15 rooma)
          (at ball14 rooma)
          (at ball13 rooma)
          (at ball12 rooma)
          (at ball11 rooma)
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
          (at-robby r3 rooma)
          (free left1)
          (free right1)
          (free left2)
          (free right2)
          (free left3)
          (free right3)
          (mount left1 r1)
          (mount right1 r1)
          (mount left2 r2)
          (mount right2 r2)
          (mount left3 r3)
          (mount right3 r3)
          
          (door rooma roomb)
          (door roomb roomc)
          (door roomc roomd)
          (door roomd roome)
          (door roome rooma)
          
          (= (current_load r1) 0)
          (= (load_limit r1) 6)
          (= (current_load r2) 0)
          (= (load_limit r2) 6)
          (= (current_load r3) 0)
          (= (load_limit r3) 6)
          (= (cost) 0)
          )
   (:goal (and (at ball28 roomb)
               (at ball27 roomb)
               (at ball26 roomb)
               (at ball25 roomb)
               (at ball24 roomb)
               (at ball23 roomb)
               (at ball22 roomc)
               (at ball21 roomc)
               (at ball20 roomc)
               (at ball19 roomc)
               (at ball18 roomd)
               (at ball17 roomd)
               (at ball16 roomd)
               (at ball15 roomd)
               (at ball14 roome)
               (at ball13 roome)
               (at ball12 roome)
               (at ball11 roome)
               (at ball10 roome)
               (at ball9 roome)
               (at ball8 roome)
               (at ball7 roome)
               (at ball6 roome)
               (at ball5 roome)
               (at ball4 roome)
               (at ball3 roome)
               (at ball2 roome)
               (at ball1 roome)))
               
               (:metric minimize (cost))
               
)