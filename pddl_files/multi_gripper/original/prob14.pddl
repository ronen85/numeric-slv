(define (problem num-gripper-x-14)
   (:domain multi-gripper-num)
   (:objects rooma roomb roomc roomd roome roomf - room
             ball30 ball29 ball28
             ball27 ball26 ball25 ball24 ball23 ball22 ball21 ball20 ball19
             ball18 ball17 ball16 ball15 ball14 ball13 ball12 ball11 ball10
             ball9 ball8 ball7 ball6 ball5 ball4 ball3 ball2 ball1 - ball 
             r1 r2 r3 - robby
             left1 right1 left2 right2 left3 right3 - gripper)
             
   (:init (= (weight ball30) 3)
          (= (weight ball29) 3)
          (= (weight ball28) 3)
          (= (weight ball27) 3)
          (= (weight ball26) 2)
          (= (weight ball25) 2)
          (= (weight ball24) 2)
          (= (weight ball23) 2)
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
          (= (weight ball4) 1)
          (= (weight ball3) 1)
          (= (weight ball2) 1)
          (= (weight ball1) 1)

          (at ball30 rooma)
          (at ball29 rooma)
          (at ball28 rooma)
          (at ball27 rooma)
          (at ball26 rooma)
          (at ball25 rooma)
          (at ball24 rooma)
          (at ball23 rooma)
          (at ball22 roomb)
          (at ball21 roomb)
          (at ball20 roomb)
          (at ball19 roomb)
          (at ball18 roomb)
          (at ball17 roomb)
          (at ball16 roomb)
          (at ball15 roomb)
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
          (door rooma roomf)
          (door roomf roomd)
          
          (= (current_load r1) 0)
          (= (load_limit r1) 6)
          (= (current_load r2) 0)
          (= (load_limit r2) 6)
          (= (current_load r3) 0)
          (= (load_limit r3) 6)
          (= (cost) 0)
          )
   (:goal (and (at ball30 roome)
               (at ball29 roome)
               (at ball28 roome)
               (at ball27 roome)
               (at ball26 roome)
               (at ball25 roome)
               (at ball24 roome)
               (at ball23 roome)
               (at ball22 roomb)
               (at ball21 roomb)
               (at ball20 roomb)
               (at ball19 roomb)
               (at ball18 roomb)
               (at ball17 roomb)
               (at ball16 roomb)
               (at ball15 roomb)
               (at ball14 roomc)
               (at ball13 roomc)
               (at ball12 roomc)
               (at ball11 roomc)
               (at ball10 roomc)
               (at ball9 roomc)
               (at ball8 roomf)
               (at ball7 roomf)
               (at ball6 roomf)
               (at ball5 roomf)
               (at ball4 roomf)
               (at ball3 roomf)
               (at ball2 roomf)
               (at ball1 roomf)))
               
               (:metric minimize (cost))
               
)
