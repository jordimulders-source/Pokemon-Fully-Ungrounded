# r3 = r2-onderlaag (lijf, wielen, wolken) + gezicht, koeienvanger en kleine geest apart verkleind door te schrappen
# op een uitsnede van het natieve model (schrap_deel.py, lijnen beschermd). Plaats: de verschuiving waarbij de
# geschrapte uitsnede het best overeenkomt met de onderlaag (ankers = ogen/mond/spijlen op dezelfde plek).
# Alleen dekkende pixels van de uitsnede worden geplakt; de buitenste rand van 1 px (overgang) alleen waar de onderlaag ook dekkend is.
import sys; sys.path.insert(0,'.')
from schrap_deel import *
from PIL import Image
base=Image.open('../sprite_r2/onderlaag_r2.png'); B=np.array(base); BP=np.array(base.getpalette()[:39]).reshape(-1,3)
DELEN=[('gezicht',(10,42,42,67,25,20,(13,14,15,16,28,29,30),(43,44,48,49,50))),
       ('koeienvanger',(9,40,64,84,24,16,(13,14,15,16,17,22,23,24,31,32,33),())),
       ('geest',(29,62,6,22,26,13,(),()))]
kies_geest=sys.argv[1] if len(sys.argv)>1 else 'schrap'
log=[]
for nm,(x0,x1,y0,y1,W,H,vk,vr) in DELEN:
    if nm=='geest' and kies_geest!='schrap': continue
    o,c,r,_,_=verklein(x0,x1,y0,y1,W,H,vk,vr)
    ex=round((x0-9)*64/86); ey=round(2+(y0-6)*62/83)
    best=None
    for dy in range(-3,4):
        for dx in range(-3,4):
            X,Y=ex+dx,ey+dy; sc=0;n=0
            for y in range(H):
                for x in range(W):
                    if o[y,x] and 0<=Y+y<64 and 0<=X+x<64:
                        b=B[Y+y,X+x]; sc+=0 if b==o[y,x] else (np.abs(PAL[o[y,x]]-BP[b]).sum() if b else 300); n+=1
            if best is None or sc/n<best[0]: best=(sc/n,X,Y)
    _,X,Y=best; log.append((nm,'kolommen weg',c,'rijen weg',r,'plek',X,Y))
    for y in range(H):
        for x in range(W):
            if not (0<=Y+y<64 and 0<=X+x<64): continue
            rand=x in (0,W-1) or y in (0,H-1)
            if o[y,x] and (not rand or B[Y+y,X+x]): B[Y+y,X+x]=o[y,x]
            elif not o[y,x] and nm=='geest': B[Y+y,X+x]=0      # geest: lucht in de uitsnede is lucht
# koeienvanger: roestspikkels binnen de spijlen weg (meerderheidsfilter alleen op roest/ijzer-tinten; zwart = spijlgrens blijft)
for _ in range(2):
    n=B.copy()
    for y in range(46,62):
        for x in range(0,24):
            if B[y,x] in (7,8,9,10,11,12):
                c=[int(B[y+dy,x+dx]) for dy in (-1,0,1) for dx in (-1,0,1) if 0<=y+dy<64 and 0<=x+dx<64 and B[y+dy,x+dx] in (7,8,9,10,11,12)]
                mm=max(set(c),key=c.count)
                if c.count(mm)>c.count(int(B[y,x])): n[y,x]=mm
    B=n
im=Image.fromarray(B,'P'); im.putpalette(base.getpalette()); im.save('onderlaag_r3.png',transparency=0)
for l in log: print(*l)
