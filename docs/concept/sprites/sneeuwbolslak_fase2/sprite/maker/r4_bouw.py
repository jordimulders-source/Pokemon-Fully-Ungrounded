# r4 = r3b + rechte lijnen weg (Jordi: "let er wederom op dat je teveel rechte lijnen gebruikt"); vanuit sprite/.
# Silhouetwijzigingen (alleen weghalen, max 1 px): zie WEG. Nieuw silhouet: sil56_r4.npy
import numpy as np
R=[list(l.rstrip('\n')) for l in open('maker/raster_r3b.txt')]
def P(x,y,c): R[y][x]=c
WEG=[(11,56),(12,56),(18,56),(19,56),(20,56),(21,57),(22,57),(33,58),(34,58),(35,58),(45,56),(54,40),(42,35),(17,36),(5,43),(9,52)]
for x,y in WEG: P(x,y,'.')
E={ # nieuwe rand na het weghalen
 (11,55):'#',(12,55):'#',(18,55):'#',(19,55):'#',(20,55):'#',(21,56):'#',(22,56):'#',(33,57):'#',(34,57):'#',(28,57):'b',(35,56):'b',
 (45,55):'#',(42,55):'a',(43,55):'a',(44,55):'a',(53,40):'#',(42,36):'d',(17,37):'d',(6,43):'d',(9,51):'#',
 # kopachterlijn bol naar buiten: (22,39-40) (23,41-44) (22,45-46) (21,47)
 (23,41):'d',(23,42):'d',(23,43):'d',(23,44):'d',(22,41):'b',(22,42):'b',(22,43):'b',(22,44):'b',(24,41):'c',(21,46):'b',
 # staartlijnen onderbroken/taps
 (53,30):'c',(50,30):'c',(43,42):'d',(43,43):'b',(38,48):'b',(41,42):'c',(41,43):'d',
 # bolbodem en ring als boog
 (29,40):'#',(29,41):'t',(29,42):'s',(29,43):'d',(29,44):'c',(34,40):'#',(34,41):'s',(34,42):'r',(34,43):'d',(34,44):'e',
 # flaponderrand: drie trappen van 4
 (30,51):'d',(31,51):'b',(32,51):'b',(33,51):'b',(34,51):'b',(35,51):'d',(36,51):'d',(39,51):'b',(39,50):'d',
 (30,52):'b',(35,52):'b',(36,52):'b',(34,53):'c',
 (15,51):'a',(53,39):'b',(25,41):'t',(33,56):'b',(17,55):'a',(38,55):'a',(26,39):'#',(26,40):'t',(26,42):'d',(26,43):'c',
}
for (x,y),c in E.items(): P(x,y,c)
# flap als eigen volume: vlak licht (e/c), schaduwsikkel b alleen langs de onderrand
for y,xs in ((45,range(37,41)),(46,range(34,40)),(47,range(34,38)),(48,range(29,32))):
    for x in xs:
        if R[y][x]=='b': P(x,y,'c')
open('maker/raster_r4.txt','w').write('\n'.join(''.join(r) for r in R)+'\n')
S=np.load('sil56_rond.npy').copy()
for x,y in WEG: S[y,x]=False
np.save('sil56_r4.npy',S)
