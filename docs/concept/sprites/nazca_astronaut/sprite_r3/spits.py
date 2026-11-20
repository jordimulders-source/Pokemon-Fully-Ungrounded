# r3: spleet hoger als bewerking op het rollenraster van r1 (spleettop rij 35, zigzag heel).
# Spleet 1 px (kol 16) loopt door tot rij T; binnenlijnen kol 15 (zwart, schaduwkant) en kol 17 (selout) gaan mee omhoog,
# in de zigzagband in de donkere bandtint. Einde = dunne ^: een enkele lijnpixel op kol 16 boven de spleet.
# De platte kap en kreuk van r1 vervallen (kreuk -> beenvulling D, zoals de rij eronder).
import sys, numpy as np
T=int(sys.argv[1]); UIT=sys.argv[2]
o=np.array([list(l.rstrip('\n')[3:]) for l in open('../sprite_r1/rollen_hand.txt') if l.strip()]); r1=o.copy()
o[33,14]='D'                       # kreuk van de oude kap
band=lambda j,i: r1[j,i] in 'Bb'
for j in range(T,35):
    o[j,16]='.'
    o[j,15]='b' if band(j,15) else 'K'
    o[j,17]='b' if band(j,17) else 'S'
o[T-1,16]='K'   # punt van de ^ (altijd zwart, ook in de band)
open(UIT,'w').write('\n'.join('%2d '%j+''.join(r) for j,r in enumerate(o))+'\n')
d=o!=r1; ys,xs=np.where(d)
print('T',T,'gewijzigd',d.sum(),'rijen %d-%d kols %d-%d'%(ys.min(),ys.max(),xs.min(),xs.max()))
for j in range(T-3,37): print('%2d '%j+''.join(o[j,10:23]))
