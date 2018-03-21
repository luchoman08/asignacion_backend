\* Equilibrio de asignaciones *\
Minimize
OBJ: 25 Asignacion_(1,_2) + 21.6666666667 Asignacion_(1,_3)
 + 21.6666666667 Asignacion_(2,_2) + 25 Asignacion_(2,_3)
Subject To
_C1: Asignacion_(1,_2) + Asignacion_(2,_2) = 1
_C2: Asignacion_(1,_3) + Asignacion_(2,_3) = 1
_C3: Asignacion_(1,_2) + Asignacion_(1,_3) >= 1
_C4: Asignacion_(2,_2) + Asignacion_(2,_3) >= 1
Binaries
Asignacion_(1,_2)
Asignacion_(1,_3)
Asignacion_(2,_2)
Asignacion_(2,_3)
End
