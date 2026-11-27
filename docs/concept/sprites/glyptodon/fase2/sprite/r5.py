# Ronde 5: lid-lijn direct boven/links van de oranje iris in een andere kleur dan zwart. Twee varianten, verder niets.
import numpy as np
from basis import png,PAL
I=np.load('r4_I.npy')
LID=[(13,40),(14,40),(15,40),(12,41),(13,41)]   # (x,y): r4 zwart; vizieronderrand links (x<=11, rij 41) blijft zwart
for v,naam in ((10,'A'),(5,'B')):
    J=I.copy()
    for x,y in LID: assert J[y,x]==1; J[y,x]=v
    np.save(f'r5_{naam}_I.npy',J); png(J,f'r5_{naam}.png'); png(J,f'r5_{naam}_8x.png',8)
    print(naam,'index',v,PAL[v],'verschil met r4',(J!=I).sum())
