# Kale reductie: natief model (99x99) -> 64x64, uniforme factor, niets getekend.
# Elke modelpixel gaat naar de spritepixel waar zijn middelpunt in valt (1-4 modelpixels per spritepixel).
# Regels: achtergrond bij >helft; zwart als er een zwarte modelpixel in zit; anders meerderheid per kleurgroep
# (gelijkspel: teal > paars > lijf), binnen de groep vlakgemiddelde -> dichtstbijzijnde spritetint.
import numpy as np, sys
from PIL import Image
from collections import deque
M='../model/model_gekozen_natief.png'
a=np.asarray(Image.open(M).convert('RGB')).astype(float); H,W=a.shape[:2]
near=a.min(axis=2)>=244
bg=np.zeros((H,W),bool); q=deque([(0,0)])
while q:
    y,x=q.popleft()
    if not(0<=y<H and 0<=x<W) or bg[y,x] or not near[y,x]: continue
    bg[y,x]=True; q.extend([(y+1,x),(y-1,x),(y,x+1),(y,x-1)])
lum=0.299*a[...,0]+0.587*a[...,1]+0.114*a[...,2]
sat=a.max(2)-a.min(2)
# modelklassen
blk=(lum<45)&~bg
teal=(a[...,1]>a[...,0]+15)&~bg&~blk
purp=(sat>=55)&~bg&~blk&~teal        # paars: antennes, voetjes, naad, oogringen, selout
body=~bg&~blk&~teal&~purp
PAL=[(152,208,160),(24,20,32),            # 0 transp, 1 zwart
     (84,46,108),(118,70,150),(168,118,202), # 2-4 paars donker/mid/licht
     (255,255,255),(224,218,242),(180,170,220),(140,128,192), # 5-8 lijf licht/basis/schaduw/diep
     (60,132,140),(150,206,202)]          # 9-10 teal
GROUP={'p':[2,3,4],'b':[5,6,7,8],'t':[9,10]}
# kleurdoelen waartegen het modelgemiddelde wordt gemeten (modeltinten per spritetint)
TGT={2:(90,52,114),3:(112,66,139),4:(165,115,190),5:(255,255,255),6:(234,228,242),7:(163,154,196),8:(137,130,178),9:(88,144,150),10:(165,212,208)}
f=float(sys.argv[1]) if len(sys.argv)>1 else 0.617
X0,Y0=17,16; OX=int(sys.argv[2]) if len(sys.argv)>2 else 9; OY=int(sys.argv[3]) if len(sys.argv)>3 else 14
from collections import defaultdict
cells=defaultdict(list)
for y in range(H):
    for x in range(W):
        sx=int(OX+(x-X0+0.5)*f); sy=int(OY+(y-Y0+0.5)*f)
        if 0<=sx<64 and 0<=sy<64: cells[(sy,sx)].append((y,x))
o=np.zeros((64,64),int)
for (sy,sx),px in cells.items():
    n=len(px); nb=sum(bg[p] for p in px)
    if nb*2>n: continue
    fg=[p for p in px if not bg[p]]
    if any(blk[p] for p in fg): o[sy,sx]=1; continue
    cnt={'t':sum(teal[p] for p in fg),'p':sum(purp[p] for p in fg),'b':sum(body[p] for p in fg)}
    g=max(['t','p','b'],key=lambda k:(cnt[k],{'t':2,'p':1,'b':0}[k]))
    sel=[p for p in fg if {'t':teal,'p':purp,'b':body}[g][p]]
    m=np.mean([a[p] for p in sel],0)
    o[sy,sx]=min(GROUP[g],key=lambda i:((m-np.array(TGT[i]))**2).sum())
np.save('kaal.npy',o)
p=Image.fromarray(o.astype('uint8'),'P'); pal=[v for c in PAL for v in c]; p.putpalette(pal+[0]*(768-len(pal))); p.save('kaal.png',transparency=0)
ys,xs=np.where(o>0); print('bbox x',xs.min(),xs.max(),'y',ys.min(),ys.max(),'w',xs.max()-xs.min()+1,'h',ys.max()-ys.min()+1)
CH=".#DPpWwlmTt"
for y in range(64):
    print('%2d '%y+''.join(CH[v] for v in o[y]))
