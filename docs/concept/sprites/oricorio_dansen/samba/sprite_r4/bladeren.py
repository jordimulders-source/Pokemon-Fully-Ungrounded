# Gele bladeren van de tooi (model r10: 7 puntige bladeren in een waaier rond het middenblad) als vlakken op de modelgeometrie:
# per blad een veelhoek door afgelezen modelpunten (punt, flanken, voet; spritecoördinaten), getekend van achter naar voor.
# Lijnen: rand van elk blad tegen een blad erachter of tegen groen = Y3 (donkere tint van het blad), onderrand tegen achtergrond/kop = zwart.
# Volume: per blad een smalle sikkel Y2 aan de kant rechtsonder (afstand tot de nerf > 0,9 px), de rest Y1.  gebruik: bladeren.py in.txt uit.txt
import numpy as np, sys
from dump import LET, INV
rows=[list(r) for r in open(sys.argv[1]).read().split('\n')[:64]]
o=np.array([[INV[c] for c in r] for r in rows]); oud=o.copy()
O,Y1,Y2,Y3=1,6,7,8; GEEL=(6,7,8)
BL=[ # naam, punt, voet, omtrek
 ('linksonder',(18.6,24.6),(28,24.5),[(18.2,24.6),(20.5,22.1),(26,21.8),(28.8,24),(26,26.6),(21,26.6)]),
 ('rechtsonder',(45.8,25.6),(34,24.5),[(46,25.6),(43,22.8),(37,22.8),(33.5,24.6),(36,26.6),(42.5,26.6)]),
 ('linksmidden',(19.4,18.6),(28.5,23),[(19.2,18.5),(23,17.4),(27.2,19.4),(29.2,23.4),(24,23.2),(20.4,20.6)]),
 ('rechtsmidden',(44.8,19),(33.5,23),[(45,18.9),(43.8,21.6),(38,23.6),(33,23.6),(36,20),(40,17.8)]),
 ('linksboven',(23.4,14.4),(29.5,22),[(23.2,14.3),(27.6,15.6),(30.2,19),(29.6,22.6),(25.4,20.2),(22.8,17)]),
 ('rechtsboven',(39.6,14.4),(32.5,22),[(39.8,14.3),(40.8,17),(36.6,21),(32,22.6),(32.4,19),(35.4,15.6)]),
 ('midden',(30.5,13.4),(30.5,25),[(30.5,13.3),(33.6,17),(33.6,21.2),(31.2,24.9),(29.8,24.9),(27.4,21.2),(27.4,17)]),
]
def binnen(px,py,P):
    c=False; n=len(P)
    for i in range(n):
        x1,y1=P[i]; x2,y2=P[(i+1)%n]
        if (y1>py)!=(y2>py) and px < x1+(py-y1)*(x2-x1)/(y2-y1): c=not c
    return c
H,W=o.shape; lab=-np.ones((H,W),int)
for k,(nm,tip,voet,P) in enumerate(BL):
    for y in range(12,28):
        for x in range(14,48):
            if binnen(x+0.5,y+0.5,P): lab[y,x]=k
# oude gele pixels buiten de bladeren in de zone: groen van de veer erachter (meest voorkomende groene buur) of transparant
zone=np.zeros((H,W),bool); zone[12:28,19:46]=True
from collections import Counter
for y,x in zip(*np.where(zone&np.isin(o,GEEL)&(lab<0))):
    c=Counter(o[a,b] for a,b in ((y-1,x),(y,x-1),(y,x+1)) if o[a,b] in (2,3,4,5))
    o[y,x]=c.most_common(1)[0][0] if c else Y3   # gat tussen bladvoeten: donkergeel (schaduw tussen de bladeren in het model)
# vullen + volume
for y,x in zip(*np.where(lab>=0)):
    nm,tip,voet,P=BL[lab[y,x]]
    ax=np.array(voet)-np.array(tip); ax/=np.linalg.norm(ax); nrm=np.array([-ax[1],ax[0]])
    if nrm@[1,1]<0: nrm=-nrm
    d=(np.array([x+0.5,y+0.5])-np.array(tip))@nrm
    o[y,x]=Y2 if d>0.9 else Y1
# lijnen: bladpixel met een 4-buur buiten het blad
for y,x in zip(*np.where(lab>=0)):
    k=lab[y,x]
    for a,b in ((y-1,x),(y+1,x),(y,x-1),(y,x+1)):
        if lab[a,b]==k: continue
        if lab[a,b]>k: o[y,x]=Y3; break          # blad ervoor: lijn op dit (achterste) blad
        if lab[a,b]<0:
            o[y,x]=O if (o[a,b]==0 or (a==y+1 and o[a,b] in (1,2,3,4,5))) else Y3; break
# dubbele lijnen (twee Y3 boven elkaar, blad erboven): bovenste wordt Y2 (sikkel van het blad erboven) -> één lijn tussen twee bladeren
nd2=0
for y in range(15,25):
    for x in range(16,46):
        if o[y,x]==Y3 and o[y+1,x] in (Y3,O) and o[y-1,x] in (Y1,Y2): o[y,x]=Y2; nd2+=1
for y in range(15,25):
    for x in range(17,45):
        if o[y,x]==Y3 and o[y,x+1]==Y3 and o[y,x-1] in (Y1,Y2) and o[y-1,x] in (Y1,Y2) and o[y+1,x] in (Y1,Y2): o[y,x]=Y2; nd2+=1
print('dubbele lijnen ontdubbeld',nd2)
open(sys.argv[2],'w').write('\n'.join(''.join(LET[v] for v in r) for r in o)+'\n')
print('dekking gewijzigd',int(((o>0)!=(oud>0)).sum()),'pixels gewijzigd',int((o!=oud).sum()))
