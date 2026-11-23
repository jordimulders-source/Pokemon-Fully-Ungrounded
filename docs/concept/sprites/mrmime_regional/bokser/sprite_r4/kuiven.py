# Bokser r4: r3 + haar vervangen door de twee kuiven van de Gen 3-Mr. Mime (1-op-1, omgekleurd), kale kop ertussen (Mr. Mime-schedel).
# Gebruik: KANTEL=0|0.25|0.5 UIT=naam python3 kuiven.py   (kanteling = kuifpunten naar achteren/rechts, per rij boven de voet)
import os, json, numpy as np
from PIL import Image
from palet import PAL
K=float(os.environ.get('KANTEL','0.25')); UIT=os.environ.get('UIT','bokser')
r3=np.load('../sprite_r3/bokser.npy'); f=np.zeros((64,64),int); f[0:63,10:53]=r3; r3f=f.copy()
mm=np.asarray(Image.open('../../../../../../graphics/pokemon/mr_mime/anim_front_gba.png'))[0:64]
DX,DY=8,-8          # MM-oog (24,19) -> sprite-oog (32,10/11); MM-schedeltop rij 13 -> rij 5
# 1. haar van het model weg (r1-haarzone + alles boven rij 6), ook het stuk haar tussen de kuiven
Z=json.load(open('../sprite_r1/zones.json'))
weg=set((y,x+10) for y,x in Z['haar'])
for y in range(0,6):
    for x in range(64):
        if f[y,x]: weg.add((y,x))
for y,x in weg: f[y,x]=0
# 2. Mr. Mime-schedel (huid) + omtrek uit MM rij 13-17, alleen waar nu leeg (gezicht van r3 blijft)
HUID={0x9:8,0xa:8,0xb:7,0xf:8,0x1:7,0xc:1,0xe:1,0x5:7}
for y in range(13,18):
    for x in range(22,42):
        v=int(mm[y,x]); yy,xx=y+DY,x+DX
        if v in HUID and f[yy,xx]==0: f[yy,xx]=HUID[v]
# 3. de twee kuiven (MM-index 2/3/4/e in de haarvlakken), omgekleurd: 2->4 licht, 3->2 vulling, 4/e->1 omlijning
HAAR={2:4,3:2,4:1,0xe:1}
def kuif(y0,y1,x0,x1,voet):
    for y in range(y0,y1):
        for x in range(x0,x1):
            v=int(mm[y,x])
            if v in HAAR:
                sh=int(round((voet-y)*K))
                f[y+DY,x+DX+sh]=HAAR[v]
kuif(8,16,14,27,15)     # linkerkuif (MM kol 14-26, rij 8-15)
kuif(11,19,34,50,17)    # rechterkuif (MM kol 34-49, rij 11-18)
# 4. kop-omtrek waar de kuiven aansluiten: weggehaalde r3-omlijning naast huid terug, open huidrand bovenop dicht
for y,x in weg:
    if r3f[y,x]==1 and f[y,x]==0 and any(f[yy,xx] in (6,7,8) for yy,xx in ((y-1,x),(y+1,x),(y,x-1),(y,x+1))): f[y,x]=1
for y in range(0,12):
    for x in range(64):
        if f[y,x] in (5,6,7,8) and any(f[yy,xx]==0 for yy,xx in ((y-1,x),(y+1,x),(y,x-1),(y,x+1))): f[y,x]=1
for x in (43,44,45): f[11,x]=1
f[12:,:]=r3f[12:,:]   # vanaf rij 12 geen haar: alles terug naar r3 (wang, bol, nek)     # bovenrand achterhoofd (oude haarrand r3 rij 11)
np.save(UIT+'.npy',f)
p=Image.fromarray(f.astype('uint8'),'P'); pal=[v for c in PAL for v in c]; p.putpalette(pal+[0]*(768-len(pal))); p.save(UIT+'.png',transparency=0)
d=(f!=r3f); hz=np.zeros_like(d); hz[0:18,:]=1
print(UIT,'KANTEL',K,'afwijkend van r3:',int(d.sum()),' buiten rij 0-17:',int((d&~hz.astype(bool)).sum()))
