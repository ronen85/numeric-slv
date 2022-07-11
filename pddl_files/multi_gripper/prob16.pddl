(define (problem num-gripper-x-16)
   (:domain multi-gripper-num)
   (:objects rooma roomb roomc roomd roome roomf - room  
             ball34 ball33 ball32 ball31 ball30 ball29 ball28
             ball27 ball26 ball25 ball24 ball23 ball22 ball21 ball20 ball19
             ball18 ball17 ball16 ball15 ball14 ball13 ball12 ball11 ball10
             ball9 ball8 ball7 ball6 ball5 ball4 ball3 ball2 ball1 - ball 
             r1 r2 r3 - robby
             left1 mid1 right1 left2 mid2 right2 left3 mid3 right3 - gripper)
             
   (:init (= (weight ball34) 1)
          (= (weight ball33) 1)
          (= (weight ball32) 1)
          (= (weight ball31) 1)
          (= (weight ball30) 1)
          (= (weight ball29) 1)
          (= (weight ball28) 1)
          (= (weight ball27) 1)
          (= (weight ball26) 1)
          (= (weight ball25) 1)
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
          (= (weight ball4) 1)
          (= (weight ball3) 1)
          (= (weight ball2) 1)
          (= (weight ball1) 1)

          (at ball34 roomb)
          (at ball33 roomb)
          (at ball32 roomb)
          (at ball31 roomb)
          (at ball30 roomb)
          (at ball29 rooma)
          (at ball28 rooma)
          (at ball27 rooma)
          (at ball26 rooma)
          (at ball25 rooma)
          (at ball24 rooma)
          (at ball23 rooma)
          (at ball22 rooma)
          (at ball21 rooma)
          (at ball20 roomc)
          (at ball19 roomc)
          (at ball18 roomc)
          (at ball17 roomc)
          (at ball16 roomc)
          (at ball15 roomc)
          (at ball14 roomc)
          (at ball13 roomc)
          (at ball12 roomc)
          (at ball11 roomc)
          (at ball10 roomc)
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
          (free mid1)
          (free right1)
          (free left2)
          (free mid2)
          (free right2)
          (free left3)
          (free mid3)
          (free right3)
          (mount left1 r1)
          (mount mid1 r1)
          (mount right1 r1)
          (mount left2 r2)
          (mount mid2 r2)
          (mount right2 r2)
          (mount left3 r3)
          (mount mid3 r3)
          (mount right3 r3)
          
          (door rooma roomb)
          (door roomb roomc)
          (door roomc roomd)
          (door roomd roome)
          (door roome rooma)
          (door rooma roomf)
          (door roomf roomd)
          
          (= (current_load r1) 0)
          (= (load_limit r1) 10)
          (= (current_load r2) 0)
          (= (load_limit r2) 10)
          (= (current_load r3) 0)
          (= (load_limit r3) 10)
          (= (cost) 0)
          )
   (:goal (and (at ball34 roome)
               (at ball33 roome)
               (at ball32 roome)
               (at ball31 roome)
               (at ball30 roome)
               (at ball29 roome)
               (at ball28 roome)
               (at ball27 roome)
               (at ball26 roome)
               (at ball25 roome)
               (at ball24 roomd)
               (at ball23 roomd)
               (at ball22 roomd)
               (at ball21 roomd)
               (at ball20 roomd)
               (at ball19 roomd)
               (at ball18 roomd)
               (at ball17 roomd)
               (at ball16 roomf)
               (at ball15 roomf)
               (at ball14 roomf)
               (at ball13 roomf)
               (at ball12 roomf)
               (at ball11 roomf)
               (at ball10 roomf)
               (at ball9 roomf)
               (at ball8 roomb)
               (at ball7 roomb)
               (at ball6 roomb)
               (at ball5 roomb)
               (at ball4 roomb)
               (at ball3 roomb)
               (at ball2 roomb)
               (at ball1 roomb)))
               
               (:metric minimize (cost))
               
)
