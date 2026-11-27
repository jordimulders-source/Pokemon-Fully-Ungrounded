# Ronde 6: één gevouwen vleugel (Jordi: bovenarm + grijze band + lichte lob + "staart" = vleugel, punt naar rechts en een onderpunt
# boven de rechterpoot). Vanaf r4 haren B. Alleen pixels binnen de vleugelvorm krijgen nieuwe kleur; silhouet blijft gelijk.
#  - vleugelvorm = de grijze pixels (5,8,9,10,12) + hun zwarte randpixels in het vak x31-53, y34-52 van r4, zonder de verre poot
#    (x<=33, y>=45), de lijfonderlijn (y>=44, x<=34), de haren en de rechterpoot (alleen (37,52) als onderpunt);
#  - buitenlijn langs die vorm: zwart waar de buur buiten de vleugel onder/rechts ligt (schaduwkant), anders donkerste grijs (12);
#  - binnenin: modellijnen waar >= DREMPEL van het spritevlak modellijn is (natief_bewerkt) in 12, de rest vleugeltinten
#    uit de modelhelderheid (kwantielen over de vleugel -> 10/9/8/5).
import numpy as np
from PIL import Image
from collections import deque
DREMPEL=0.45
im=Image.open('../r4/kuiken_r4_haarB.png'); a=np.array(im); r4=a.copy()
frac=np.load('frac64.npy'); lum=np.load('lum64.npy')
HAAR={(43,35),(44,36),(43,38),(44,39),(43,41),(44,41),(46,44),(47,43)}
G={5,8,9,10,12}
def inbox(x,y): return 31<=x<=53 and 34<=y<=51 and not (x<=33 and y>=45) and (x,y) not in HAAR
W=np.zeros((64,64),bool)
for y in range(64):
    for x in range(64):
        if inbox(x,y) and a[y,x] in G: W[y,x]=True
W[52,37]=True                                   # onderpunt boven de rechterpoot
# alleen de samenhangende vorm vanaf de band
lab=np.zeros_like(W); q=deque([(45,36)]); lab[45,36]=True
while q:
    y,x=q.popleft()
    for dy,dx in ((-1,0),(1,0),(0,-1),(0,1)):
        yy,xx=y+dy,x+dx
        if W[yy,xx] and not lab[yy,xx]: lab[yy,xx]=True; q.append((yy,xx))
W=lab
for y in range(64):
    for x in range(64):
        if a[y,x]==1 and inbox(x,y) and not (y>=44 and x<=34) and any(W[y+dy,x+dx] for dy,dx in ((-1,0),(1,0),(0,-1),(0,1))):
            W[y,x]=True
W2=W.copy()
out=a.copy(); n={}
def zet(x,y,v,k):
    if out[y,x]!=v: out[y,x]=v; n[k]=n.get(k,0)+1
rand=np.zeros_like(W)
for y,x in zip(*np.nonzero(W)):
    nb={(dy,dx):W[y+dy,x+dx] for dy,dx in ((-1,0),(1,0),(0,-1),(0,1))}
    if all(nb.values()): continue
    rand[y,x]=True
    schaduw=(not nb[(1,0)]) or (not nb[(0,1)])
    zet(x,y,1 if schaduw else 12,'buitenlijn')
binnen=W&~rand
vals=lum[binnen&(frac<DREMPEL)]; q=np.quantile(vals,[0.15,0.40,0.75])
for y,x in zip(*np.nonzero(binnen)):
    if frac[y,x]>=DREMPEL: zet(x,y,12,'modellijn'); continue
    l=lum[y,x]; zet(x,y,5 if l<q[0] else 8 if l<q[1] else 9 if l<q[2] else 10,'vleugeltint')
assert ((out>0)!=(r4>0)).sum()==0
print(n,'totaal gewijzigd',int((out!=r4).sum()),'vleugel px',int(W.sum()),'drempels',q.round(0),'zwart %',round((out==1).sum()/(out>0).sum()*100,1))
o=Image.fromarray(out,'P'); o.putpalette(im.getpalette()); o.save('kuiken_r6.png',transparency=0)
np.save('vleugel.npy',W); np.save('modellijn.npy',binnen&(frac>=DREMPEL))
