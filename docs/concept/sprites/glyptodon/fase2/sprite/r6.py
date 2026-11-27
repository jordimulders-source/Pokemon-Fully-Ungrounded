# Ronde 5: lid-lijn direct boven/links van de oranje iris in een andere kleur dan zwart. Twee varianten, verder niets.
import numpy as np
from basis import png,PAL
I=np.load('r4_I.npy')
LID=[(13,40),(14,40),(15,40),(12,41),(13,41)]   # (x,y): r4 zwart; vizieronderrand links (x<=11, rij 41) blijft zwart
for v,naam in ((10,'A'),(5,'B')):
    J=I.copy()
    for x,y in LID: assert J[y,x]==1; J[y,x]=v

    np.save(f'r6_{naam}_I.npy',J); png(J,f'r6_{naam}.png'); png(J,f'r6_{naam}_8x.png',8)
    print(naam,'index',v,PAL[v],'verschil met r4',(J!=I).sum())
# Jordi: "en als de rest van de lijn moet mee kleuren dan moet je dat doen": de hele vizieronderrand over de kop
# (grens beige vizier / grijze kop) meekleuren; buitenlijn (x3,rij41) blijft zwart, ook de schildonderrand verderop.
LIJN=[(x,41) for x in range(4,12)]+[(15,39),(16,39),(17,39),(18,39),(19,39),(20,40),(21,41),(21,42)]
for v,naam in ((10,'A'),(5,'B')):
    J=np.load(f'r6_{naam}_I.npy').copy()
    for x,y in LIJN: assert J[y,x]==1,(x,y); J[y,x]=v
    np.save(f'r6_{naam}_lijn_I.npy',J); png(J,f'r6_{naam}_lijn.png'); png(J,f'r6_{naam}_lijn_8x.png',8)
    print(naam+'_lijn','extra',len(LIJN))
np.save('r6_lijnpix.npy',np.array(LIJN+LID))
# controle: oogpixels (alle oranje in r4) 0 px verschil met r4
I4=np.load('r4_I.npy'); oog=(I4==14)|(I4==15)
for f in ['r6_A','r6_B','r6_A_lijn','r6_B_lijn']:
    J=np.load(f+'_I.npy'); print(f,'oogpixels',int(oog.sum()),'verschil met r4 in het oog:',int((J[oog]!=I4[oog]).sum()),' totaal verschil met r4:',int((J!=I4).sum()))
