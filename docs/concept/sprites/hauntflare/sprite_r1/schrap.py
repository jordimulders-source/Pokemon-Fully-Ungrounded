# Stap 1: model (99x99 natief) -> 64x64 ZONDER resamplen (Gengas-methode).
# - bijsnijden tot de inhoud
# - rijen/kolommen schrappen die het meest op hun buur lijken, gespreid (>= SP uit elkaar),
#   nooit door het gezicht, en alleen als de losse delen (hand, linkerhand, staart/ring) los blijven
#   en de witte gaten (binnen de ring) blijven bestaan.
# Elke overgebleven pixel is een echte modelpixel.
# Uitvoer: model64.png (RGB, wit = leeg), schrap.json (geschrapte rijen/kolommen, natieve coordinaten)
import json, sys
from PIL import Image; import numpy as np
from scipy import ndimage as nd
D='docs/concept/sprites/hauntflare/'
a=np.asarray(Image.open(D+'model/model_claude_natief.png').convert('RGB')).astype(int)
wit=lambda img: img.min(2)>=0xf0
m=~wit(a)
ys,xs=np.where(m); X0,X1,Y0,Y1=xs.min(),xs.max(),ys.min(),ys.max()
# rechterhand: eigen component (8-verbonden). Verschuiving: zie NOTITIES (0 px mogelijk zonder te raken)
HAND_DX=int(sys.argv[1]) if len(sys.argv)>1 else 0
lab,n=nd.label(m,np.ones((3,3)))
hand=lab==lab[53,80]
if HAND_DX:
    b=a.copy(); b[hand]=255
    hy,hx=np.where(hand); b[hy,hx-HAND_DX]=a[hy,hx]; a=b; m=~wit(a)
# gezicht (natief): ogen + mond van het model, nooit schrappen
import os
PROT=os.environ.get('PROT','0')=='1'
FACE_X=range(24,47) if PROT else range(0); FACE_Y=range(33,53) if PROT else range(0)
SP=int(os.environ.get('SP','2'))
TW,TH=62,62           # doel inhoud (1 px marge links/rechts, onderrand op rij 62/63)
def ncomp(img):
    mm=~wit(img); l,k=nd.label(mm,np.ones((3,3)))
    lw,kw=nd.label(~mm)   # 4-verbonden witte gaten
    return k,kw
crop=a[Y0:Y1+1,X0:X1+1]
base=ncomp(np.pad(crop,((1,1),(1,1),(0,0)),constant_values=255))
def kies(img,n,axis,verboden):
    # gespreid: n doelposities gelijk verdeeld over de as (buiten verboden zones); per doel de goedkoopste
    # kandidaat binnen +-WIN die de losse delen los houdt en >= SP van de andere afligt.
    A=img if axis==0 else img.transpose(1,0,2)
    L=len(A)
    cost=np.array([np.abs(A[i]-A[i+1]).sum() for i in range(L-1)])
    vrij=[i for i in range(L-1) if i not in verboden and i+1 not in verboden]
    doel=[vrij[int((k+0.5)*len(vrij)/n)] for k in range(n)]
    gekozen=[]
    for d in doel:
        for i in sorted([c for c in vrij if abs(c-d)<=WIN],key=lambda c:(cost[c],abs(c-d))):
            if not all(abs(i-j)>=SP for j in gekozen): continue
            t=np.delete(img,gekozen+[i],axis)
            if ncomp(np.pad(t,((1,1),(1,1),(0,0)),constant_values=255))!=base: continue
            gekozen.append(i); break
    return sorted(gekozen)
WIN=int(os.environ.get('WIN','2'))
H,W=crop.shape[:2]
# uniform: zelfde verhouding op beide assen
f=min(TW/W,TH/H)
nW=W-int(np.floor(W*f+1e-9)); nH=H-int(np.floor(H*f+1e-9))
nW=max(nW,W-TW); nH=max(nH,H-TH)
cols=kies(crop,nW,1,{x-X0 for x in FACE_X})
rows=kies(crop,nH,0,{y-Y0 for y in FACE_Y})
assert len(cols)==nW and len(rows)==nH,(len(cols),nW,len(rows),nH)
r=np.delete(np.delete(crop,rows,0),cols,1)
h,w=r.shape[:2]
out=np.full((64,64,3),255)
ox=(64-w)//2; oy=63-h   # gecentreerd, onderkant op rij 62 (1 px boven de onderrand)
out[oy:oy+h,ox:ox+w]=r
OUTN=os.environ.get('OUTN','model64')
Image.fromarray(out.astype('uint8')).save(D+'sprite_r1/'+OUTN+'.png')
json.dump({'crop':[int(X0),int(Y0),int(X1),int(Y1)],'hand_dx':HAND_DX,
           'rijen_natief':[int(v+Y0) for v in rows],'kolommen_natief':[int(v+X0) for v in cols],
           'offset':[int(ox),int(oy)],'grootte':[int(w),int(h)]},open(D+'sprite_r1/'+('schrap' if OUTN=='model64' else OUTN)+'.json','w'),indent=1)
print('rijen',[v+Y0 for v in rows]); print('kolommen',[v+X0 for v in cols]); print('inhoud',w,h,'offset',ox,oy)
