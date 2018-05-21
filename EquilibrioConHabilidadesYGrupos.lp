\* Equilibrio de asignaciones *\
Minimize
OBJ: 0 Asignacion_(1,_0) + 0 Asignacion_(1,_1) + 10 Asignacion_(1,_2)
 + 0 Asignacion_(2,_0) + 0 Asignacion_(2,_1) + 100 Asignacion_(2,_2)
Subject To
_C1: Asignacion_(1,_0) + Asignacion_(2,_0) = 1
_C2: Asignacion_(1,_1) + Asignacion_(2,_1) = 1
_C3: Asignacion_(1,_2) + Asignacion_(2,_2) = 1
_C4: Asignacion_(1,_0) + Asignacion_(1,_1) + Asignacion_(1,_2) >= 1
_C5: Asignacion_(2,_0) + Asignacion_(2,_1) + Asignacion_(2,_2) >= 1
Binaries
Asignacion_(1,_0)
Asignacion_(1,_1)
Asignacion_(1,_2)
Asignacion_(2,_0)
Asignacion_(2,_1)
Asignacion_(2,_2)
End
