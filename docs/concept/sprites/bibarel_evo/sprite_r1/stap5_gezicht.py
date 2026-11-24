# Stap 5: gezichtszone (oogband, snuit, neus, tanden) uit reductie A (oppervlak-middeling; bewaart het modelgezicht beter dan de
# meerderheidsstem). Zone x20-41, y14-27; rand van de figuur blijft omlijning. Niets hertekend.
import numpy as np,sys; sys.path.insert(0,'sprite_r1'); from gemeen import *
o=laad('sprite_r1/ontruist.png').copy(); A=laad('sprite_r1/kaal_A_pal.png')
Z=np.zeros_like(o,bool); Z[14:28,20:42]=True
Z&=(o!=0)&(A!=0)
P=np.pad(o>0,1); rand=(o>0)&~(P[:-2,1:-1]&P[2:,1:-1]&P[1:-1,:-2]&P[1:-1,2:])
Z&=~rand
o[Z]=A[Z]
opslaan(o,'sprite_r1/gezicht.png',8)
