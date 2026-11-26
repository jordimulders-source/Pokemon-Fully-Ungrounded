# Eindkeuring r15: alleen benoemde indexwissels per pixel vanaf sprite/r15/sprite.png.
import sys, os
H=os.path.dirname(os.path.abspath(__file__)); SP=os.path.join(H,'..','sprite')
sys.path.insert(0,os.path.join(SP,'r10','pijp')); sys.path.insert(0,os.path.join(SP,'r14'))
from geo10 import GEO10
import recept, numpy as np
from PIL import Image
im=Image.open(os.path.join(SP,'r15','sprite.png')); PAL=im.getpalette()[:48]
A=np.array(im); B=A.copy(); LOG=[]
def zet(x,y,c,reden):
    if B[y,x]!=c: LOG.append((x,y,int(B[y,x]),int(c),reden)); B[y,x]=c
# 1 PB tweede rasterlijn gelijk aan de eerste (4 px tussen de lijnen, vakken 3 px)
for x,y,c in [(34,21,12),(34,22,13),(36,22,12),(36,23,13)]: zet(x,y,c,'PB: rasterlijn 2 = lijn 1 + 4 px')
# 2 PF bovenkant: rand/lichte rand in hetzelfde patroon als PB (vak 1 overal 3 px)
for x,y,c in [(36,41,2),(34,41,12),(34,42,14),(36,42,12),(36,43,14)]: zet(x,y,c,'PF-top: rand parallel aan rasterlijnen (zoals PB)')
# 3 PF onderkant: onderrand parallel aan de rasterlijnen (laatste vak overal 3 px)
for x,y,c in [(33,59,13),(33,60,1),(35,60,13),(35,61,1)]: zet(x,y,c,'PF-bodem: onderrand parallel aan rasterlijnen (zoals PB)')
# 4 PE-bovenrand volgens de PE-geometrie (PE voor PF), recept herberekend voor de buurt
P=np.load(os.path.join(SP,'r15','P.npy'),allow_pickle=True).astype(object)
for x,y in [(30,45),(31,45),(29,45),(32,46),(33,46),(31,46)]: P[y,x]='PE'
NEW=recept.recept('PE',GEO10['PE'],P)
for (x,y),c in NEW.items():
    if 27<=x<=35 and 45<=y<=47: zet(x,y,c,'PE-bovenrand/lichte rand volgens PE-geometrie (PE voor PF)')
# 5 onderrand voorbuis 1 px breed langs de modelrand (geen dubbel zwart)
for x,y,c in [(28,44,4),(27,45,4),(31,42,4),(32,41,4),(32,42,1)]: zet(x,y,c,'voorbuis: onderrand 1 px (dubbel zwart weg, buisschaduw 4)')
# 6 PC: dubbele rasterlijn (C+E naast elkaar) -> een lijn
zet(54,31,11,'PC: dubbele rasterlijn -> vak 3 (B)')
# 7 PA: einde bovenrand ligt aan de lichtkant -> navy i.p.v. zwart
zet(42,24,2,'PA: bovenrand lichtkant navy (geen zwart)')
# 8 kraag bovenop de hub: ruis 8-3-1-8-3-8 en losse witte pixel weg
for x,y,c in [(34,28,4),(38,28,8),(37,27,2)]: zet(x,y,c,'hubkraag: ruis weg (stok loopt door, rand 8 8 8, bovenrand navy)')
Image.fromarray(B.astype(np.uint8),'P').save(os.path.join(H,'tmp.png'))
i2=Image.fromarray(B.astype(np.uint8),'P'); i2.putpalette(PAL); i2.save(os.path.join(H,'sprite.png'),transparency=0)
with open(os.path.join(H,'log.txt'),'w') as f:
    f.write('x y oud->nieuw reden (t.o.v. sprite/r15/sprite.png)\n')
    for r in LOG: f.write('%d %d %d->%d %s\n'%r)
    f.write('totaal %d; silhouet +%d/-%d px; kleuren %d\n'%(len(LOG),int(((A==0)&(B!=0)).sum()),int(((A!=0)&(B==0)).sum()),len(set(B.flat))))
os.remove(os.path.join(H,'tmp.png'))
