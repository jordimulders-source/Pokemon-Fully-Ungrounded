"""Eisenlijst-controle voor een party-icoon (zie EISEN_ICOON.md).
python3 icoon_check.py icon.png front.png      (front = onze goedgekeurde frontsprite, frame 1 boven)
Normen = p10–p90 van de 385 originele Gen 1–3-iconen (icon_gba.png)."""
import sys,numpy as np
from PIL import Image
def pal(p):
    L=open(p).read().split('\n'); return np.array([[int(v) for v in L[3+k].split()[:3]] for k in range(16)])
ic=Image.open(sys.argv[1]); ix=np.array(ic); out=[]
def chk(naam,ok,info): out.append((naam,ok,info))
chk('formaat 32x64, modus P',ic.size==(32,64) and ic.mode=='P',f'{ic.size} {ic.mode}')
P=np.array(ic.getpalette()[:48]).reshape(16,3)
pk=[k for k in range(6) if (pal(f'graphics/pokemon/icon_palettes/pal{k}.pal')[1:]==P[1:]).all()]
chk('palet = een icoonpalet (pal0-5)',bool(pk),f'pal{pk}' if pk else 'geen match')
lum=P.mean(1); f1=ix[:32]; f2=ix[32:64]; m=f1>0; ys,xs=np.nonzero(m)
h=ys.max()-ys.min()+1; w=xs.max()-xs.min()+1
fr=np.array(Image.open(sys.argv[2]))[:64]; fy,fx=np.nonzero(fr>0); fh=fy.max()-fy.min()+1
T=[(25,15),(35,18),(45,21),(54,22),(61,24),(64,25)]; doel=np.interp(fh,[t[0] for t in T],[t[1] for t in T])
chk('hoogte past bij fronthoogte (±3)',abs(h-doel)<=3,f'{h} (doel ±{doel:.0f}, front {fh})')
chk('breedte 16-27',16<=w<=27,str(w))
chk('onderkant y 27-30',27<=ys.max()<=30,str(ys.max()))
chk('midden x 14.5-16.5',14.5<=(xs.min()+xs.max())/2<=16.5,str((xs.min()+xs.max())/2))
nc=len(np.unique(ix[ix>0])); chk('kleuren 6-10',6<=nc<=10,str(nc))
pad=np.pad(m,1); edge=m&~(pad[:-2,1:-1]&pad[2:,1:-1]&pad[1:-1,:-2]&pad[1:-1,2:])
dk=lum[f1]<110; chk('omlijning dicht (>=95% randpixels donker)',(dk&edge).sum()/edge.sum()>=.95,f'{(dk&edge).sum()/edge.sum():.2f}')
mid=(ys.min()+ys.max())/2; ey,ex=np.nonzero(edge)
top=lum[f1[ey[ey<mid],ex[ey<mid]]].mean(); bot=lum[f1[ey[ey>=mid],ex[ey>=mid]]].mean()
chk('omlijning boven donkerder dan onder',top<bot,f'boven {top:.0f}, onder {bot:.0f}')
r=(dk&m&~edge).sum()/m.sum(); chk('binnenlijnen/oppervlak 0.10-0.26 (Gen 3 mediaan 0.18)',.10<=r<=.26,f'{r:.3f}')
m2=f2>0; y2,x2=np.nonzero(m2)
chk('frame 2: voeten op dezelfde rij',abs(y2.max()-ys.max())<=1,f'{ys.max()} -> {y2.max()}')
chk('frame 2: bovenkant hooguit 2 px verschoven',abs(y2.min()-ys.min())<=2,f'{y2.min()-ys.min()}')
best=min(((np.roll(np.roll(f1,dy,0),dx,1)!=f2).sum() for dy in range(-2,3) for dx in range(-2,3)))/m.sum()
chk('frame 2: 10-50% anders (kleine handeling)',.10<=best<=.50,f'{best:.2f}')
fc=(fr[fy.min():fy.max()+1,fx.min():fx.max()+1]>0).astype(np.uint8)*255
s=np.array(Image.fromarray(fc).resize((w,h),Image.BOX))>110; c=m[ys.min():ys.max()+1,xs.min():xs.max()+1]
iou=(s&c).sum()/(s|c).sum(); chk('pose = front (silhouet-IoU >= 0.55)',iou>=.55,f'{iou:.2f}')
for n,ok,i in out: print(('OK  ' if ok else 'NEE '),n,'|',i)
print(f"{sum(o for _,o,_ in out)}/{len(out)} automatisch; handmatig: zie EISEN_ICOON.md punt 2")
