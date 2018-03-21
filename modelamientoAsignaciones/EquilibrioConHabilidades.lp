\* Equilibrio de asignaciones *\
Minimize
OBJ: 21.6666666667 Asignacion_(1,_1) + 29.8 Asignacion_(1,_2)
 + 25 Asignacion_(2,_1) + 26.4666666667 Asignacion_(2,_2)
Subject To
_C1: Asignacion_(1,_1) + Asignacion_(2,_1) = 1
_C2: Asignacion_(1,_2) + Asignacion_(2,_2) = 1
_C3: Asignacion_(1,_1) + Asignacion_(1,_2) >= 1
_C4: Asignacion_(2,_1) + Asignacion_(2,_2) >= 1
Binaries
Asignacion_(1,_1)
Asignacion_(1,_2)
Asignacion_(2,_1)
Asignacion_(2,_2)
End
