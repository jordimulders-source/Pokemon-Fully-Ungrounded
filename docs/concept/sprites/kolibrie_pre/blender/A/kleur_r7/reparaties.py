"""r7 = kleur_r6/raster_S.txt + reparaties R1-R9 uit kleur_r6/EINDKEURING.md (alleen indexwissels) -> raster.txt + kolibrie_pre.png"""
import sys
A='/home/user/Pokemon-Fully-Ungrounded/docs/concept/sprites/kolibrie_pre/blender/A/'
R={
 'R1':[((32,23),'1'),((34,24),'1'),((35,24),'1'),((38,26),'1')],
 'R2':[((26,14),'1')],
 'R3':[((p),'3') for p in [(43,37),(42,38),(43,38),(42,39),(43,39),(42,40),(43,40),(44,40)]],
 'R4':[((p),'3') for p in [(32,41),(33,41),(34,41),(35,41),(32,42),(33,42),(34,42),(35,42),(35,40)]],
 'R5':[((p),'8') for p in [(35,34),(35,35),(35,36)]],
 'R6':[((29,17),'B'),((29,18),'B')],
 'R7':[((15,17),'2'),((15,20),'2')],
 'R8':[((28,43),'C'),((28,44),'D')],
 'R9':[((p),'3') for p in [(32,30),(31,31),(31,32),(31,33),(32,34)]],
}
g=[list(l.rstrip('\n')) for l in open(A+'kleur_r6/raster_S.txt')][:64]
for k,lst in R.items():
    for (x,y),c in lst: g[y][x]=c
open(A+'kleur_r7/raster.txt','w').write('\n'.join(''.join(r) for r in g)+'\n')
sys.path.insert(0,A+'kleur_r7'); import palet; palet.build(A+'kleur_r7/raster.txt',A+'kleur_r7/kolibrie_pre.png')
