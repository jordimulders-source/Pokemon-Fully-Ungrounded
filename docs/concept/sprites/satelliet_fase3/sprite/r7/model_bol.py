# r7 stap 1: de 3 oogbollen met zichtbaar oog in het bevroren model (r13b) vergroten rond hun eigen middelpunt.
# Alleen modelpixels: bol+oog als geheel nearest-neighbour geschaald (geen tekenwerk). Middelpunt/straal = cirkelfit op de
# buitenrand tegen de achtergrond (zie RAPPORT). Schrijft model_bol120.png / model_bol130.png (+_8x) en bolmaskers (.npy).
import os, sys, numpy as np
from PIL import Image
H=os.path.dirname(os.path.abspath(__file__))
M=os.path.join(H,'..','..','model','model_gekozen.png')
sys.path.insert(0,os.path.join(H,'..','r4')); import kaal
a=np.array(Image.open(M).convert('RGB')); Hh,Ww,_=a.shape
w=a.min(2)>=245
# achtergrond = wit, verbonden met de rand (zelfde als common.load)
from collections import deque
bg=np.zeros((Hh,Ww),bool); q=deque()
for y in range(Hh):
    for x in (0,Ww-1):
        if w[y,x] and not bg[y,x]: bg[y,x]=1; q.append((y,x))
for x in range(Ww):
    for y in (0,Hh-1):
        if w[y,x] and not bg[y,x]: bg[y,x]=1; q.append((y,x))
while q:
    y,x=q.popleft()
    for dy,dx in ((1,0),(-1,0),(0,1),(0,-1)):
        yy,xx=y+dy,x+dx
        if 0<=yy<Hh and 0<=xx<Ww and w[yy,xx] and not bg[yy,xx]: bg[yy,xx]=1; q.append((yy,xx))
pal=np.array(kaal.PAL[1:],float)
lab=((a[:,:,None,:].astype(float)-pal[None,None])**2).sum(3).argmin(2)+1; lab[bg]=0
Y,X=np.mgrid[0:Hh,0:Ww]; PX,PY=X+0.5,Y+0.5
# cirkelfits (buitenrand tegen achtergrond, sector weg van kraag/paneel): middelpunt en straal tot de buitenkant van de omlijning
BOL={'voor':(62.16,127.95,20.62),'links':(75.01,64.28,10.75),'rechts':(188.46,91.70,11.98)}
KRAAGSET=(1,2,3,4,6,7,8)
# linkerkraag: per rij de eerste donkere/paarse pixel vanaf x=79 (kraagrand gemeten op x 79-83, rijen 54-74; x<79 is de oogring)
KSTART={y:next(x for x in range(79,110) if lab[y,x] in KRAAGSET) for y in range(54,75)}
def masker(nm):
    cx,cy,r=BOL[nm]; d=np.hypot(PX-cx,PY-cy); m=(d<=r+0.5)&~bg
    ang=np.degrees(np.arctan2(PY-cy,PX-cx))%360
    if nm=='voor':    # kraag rechtsboven ligt achter de bol: kraagpixels buiten de bolomlijning eruit
        m&=~((ang>270)&(ang<360)&(d>0.85*r)&np.isin(lab,(4,6,7,8)))
    if nm=='rechts':  # kraag links ligt achter de bol
        m&=~((ang>135)&(ang<225)&(d>0.85*r)&np.isin(lab,(4,6,7,8)))
    if nm=='links':   # in het model ligt de kraag VOOR deze bol: bol eindigt per rij bij de linkerrand van de kraag
        for y,x0 in KSTART.items(): m[y,x0:]=False
    return m
MASK={nm:masker(nm) for nm in BOL}
# kraag van de linkerbol (de pixels rechts van de bol binnen zijn kraagring) blijft bovenop, zoals in het model
KR=np.zeros_like(bg)
for y,x0 in KSTART.items(): KR[y,x0:x0+8]=~bg[y,x0:x0+8]   # kraagring is 7-8 px breed (gemeten, x 79-87)
def schaal(k):
    out=a.copy(); al=~bg; tot=np.zeros_like(bg); per={}
    for nm in ('rechts','links','voor'):   # voor laatst: ligt vooraan
        cx,cy,r=BOL[nm]; R=(r+0.5)*k+1
        sx=np.floor(cx+(PX-cx)/k).astype(int); sy=np.floor(cy+(PY-cy)/k).astype(int)
        ok=(np.hypot(PX-cx,PY-cy)<=R)&(sx>=0)&(sx<Ww)&(sy>=0)&(sy<Hh)
        ok[ok]&=MASK[nm][sy[ok],sx[ok]]
        if nm=='links': ok&=~KR
        out[ok]=a[sy[ok],sx[ok]]; al|=ok; tot|=ok; per[nm]=ok
    out[~al]=255
    return out,per,~al
if __name__=='__main__':
    for k,tag in ((1.2,'120'),(1.3,'130')):
        out,per,bgn=schaal(k)
        np.save(os.path.join(H,'model_bol%s_bg.npy'%tag),bgn)   # achtergrondmasker: ingesloten gaten (bv. tussen rechterarm en paneel PC) blijven achtergrond
        Image.fromarray(out).save(os.path.join(H,'model_bol%s.png'%tag))
        Image.fromarray(out).resize((Ww*8,Hh*8),Image.NEAREST).save(os.path.join(H,'model_bol%s_8x.png'%tag))
        ys,xs=np.where(out.min(2)<245); print(tag,'bbox',xs.min(),xs.max(),ys.min(),ys.max(),{n:int(v.sum()) for n,v in per.items()})
    print({n:int(m.sum()) for n,m in MASK.items()}, 'kraag links',int(KR.sum()))
