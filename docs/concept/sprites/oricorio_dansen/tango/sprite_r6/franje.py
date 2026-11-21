# r6 punt 2: franje als doorlopende veerstroken. Per franjepixel de modelhelderheid gemeten LANGS de strookrichting van het model
# (structuurtensor op het natieve raster, venster ±6 natieve px): gemiddelde van 5 monsters op -4..+4 natieve px langs de strook.
# Daarna 3 tinten (naad R3 bij L<58 / strook R2 / licht R1) en korrel van 1 px weg (meest voorkomende rode buur). Silhouet onveranderd.
import numpy as np, json
from collections import Counter
from PIL import Image
from modeltoon import r,c,DY,DX
o=np.load('na_vleugels.npy').copy(); vo=o.copy(); H,W=o.shape
R1,R2,R3=7,8,9; ROOD=(R1,R2,R3)
nat=np.asarray(Image.open('natief.png')).astype(float)@[.299,.587,.114]
gy,gx=np.gradient(nat)
def box(a,k=6):
    from numpy.lib.stride_tricks import sliding_window_view as sw
    p=np.pad(a,k,mode='edge'); return sw(p,(2*k+1,2*k+1)).mean((2,3))
Jxx,Jyy,Jxy=box(gx*gx),box(gy*gy),box(gx*gy)
th=0.5*np.arctan2(2*Jxy,Jxx-Jyy)          # richting van de sterkste gradiënt; strook loopt loodrecht daarop
def samp(yy,xx):
    yy=int(round(yy)); xx=int(round(xx))
    return nat[yy:yy+2,xx:xx+2].mean()
log={}
def tel(k): log[k]=log.get(k,0)+1
M=np.zeros((H,W)); hoek=np.zeros((H,W))
for y in range(40,H):
    for x in range(W):
        if o[y,x] not in ROOD: continue
        ny,nx=r[y-DY],c[x-DX]; t=th[ny,nx]+np.pi/2
        dy,dx=np.sin(t),np.cos(t)
        M[y,x]=np.mean([samp(ny+k*dy,nx+k*dx) for k in (-4,-2,0,2,4)]); hoek[y,x]=np.degrees(t)%180
for y in range(40,H):
    for x in range(W):
        if o[y,x] in ROOD:
            v=R3 if M[y,x]<58 else (R1 if M[y,x]>=78 else R2)
            if v!=o[y,x]: o[y,x]=v; tel('1_strooktint')
def nb(y,x): return [(y+a,x+b) for a,b in((-1,0),(1,0),(0,-1),(0,1)) if 0<=y+a<H and 0<=x+b<W]
for it in range(2):
    for y in range(40,H):
        for x in range(W):
            k=o[y,x]
            if k not in ROOD: continue
            if any(o[a,b]==k for a,b in nb(y,x)): continue
            c_=Counter(o[a,b] for a,b in nb(y,x) if o[a,b] in ROOD)
            if c_: o[y,x]=c_.most_common(1)[0][0]; tel('2_korrel_1px_weg')
assert ((o>0)==(vo>0)).all()
np.save('na_franje.npy',o); np.save('franje_M.npy',M)
log['px_veranderd']=int((o!=vo).sum()); json.dump(log,open('log_franje.json','w'),indent=0); print(log)
print('mediaan hoek strook (graden, 0=horizontaal):',np.median(hoek[M>0]))
