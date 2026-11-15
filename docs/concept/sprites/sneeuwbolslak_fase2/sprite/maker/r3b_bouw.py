# r3b = r3 + alleen de bol (rij 19-38) op het nieuwe silhouet sil56_rond.npy (vanuit sprite/). Met de hand; elke rij = x21..x42.
import numpy as np
S=np.load('sil56_rond.npy')
R=[list(l.rstrip('\n')) for l in open('maker/raster_r3.txt')]
#      x: 2222222223333333333444
#         1234567890123456789012
RIJ={19:"...d..................",
     20:"..ded..d.dddd.........",
     21:"..debddedeeeed##......",
     22:"..debdebdeecceee#.##..",
     23:"...dbbcbcccceeeec#e#..",
     24:"...dcecbbbbbccecbceb#.",
     25:"..deweeccbbbbbbdcbb#..",
     26:".dewwwweeccbce#ecbbc#.",
     27:".dewwwwebbwwcc#eeccb#.",
     28:".deewwebbewccc#eebbb#.",
     29:"deccecceeeecc#e#ecbbb#",
     30:"decbbbbbcee##ee#eecbb#",
     31:"dcbbbeebbc#eeeec#cbbc#",
     32:"dbbbebbbc#eeccce#cbbb#",
     33:".dbbbbbbcdeeecce#bbb#.",
     34:".dbceecceeeeeec#cbbb#.",
     35:".dceebbbbbwwwec#cbbb#",
     36:"#ceeeccbbbcwwwccdcbb#",
     37:".#cewwwwwcbbceeeccb#",
     38:"dc#cewweeeewwweccb#"}
for y,s in RIJ.items():
    for i,c in enumerate(s): R[y][21+i]=c
# opschonen tintvlakjes < 3 px (ijspuntvlakken van 2 px blijven: facet)
for (x,y),c in {(25,24):'e',(34,26):'c',(25,29):'c',(41,31):'b',(26,36):'e',(27,36):'b',(31,36):'b',(30,37):'w',(33,37):'b',(25,38):'c'}.items(): R[y][x]=c
for y in range(18,41):
    for x in range(19,45):
        if not S[y,x]: R[y][x]='.'
open('maker/raster_r3b.txt','w').write('\n'.join(''.join(r) for r in R)+'\n')
