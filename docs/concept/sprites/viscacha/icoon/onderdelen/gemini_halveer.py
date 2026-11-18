"""Gemini-bewerking (1024, raster 16, offset 15) -> natief 64 (middenpixel per vak, front-palet) -> exact 2x met regels -> icoon 32 (pal2).
python3 gemini_halveer.py in.png naam"""
import sys,numpy as np
from PIL import Image
D='docs/concept/sprites/viscacha/'
a=np.array(Image.open(sys.argv[1]).convert('RGB')).astype(int); naam=sys.argv[2]
L=open(D+'af/normal.pal').read().split('\n'); FP=np.array([[int(v) for v in L[3+k].split()[:3]] for k in range(16)])
n=(1024-15)//16; nat=np.zeros((n,n),np.uint8)
for j in range(n):
    for i in range(n):
        px=a[15+16*j+5:15+16*j+11,15+16*i+5:15+16*i+11].reshape(-1,3); c=np.median(px,0)
        if c.min()>=225: continue
        nat[j,i]=((FP[1:]-c)**2).sum(1).argmin()+1
Image.fromarray(nat,'P').save(D+f'icoon/onderdelen/{naam}_nat.png')
DONKER={1}; GEEL={8,9,10}
IP=np.array([[int(v) for v in l.split()[:3]] for l in open('graphics/pokemon/icon_palettes/pal2.pal').read().split('\n')[3:19]])
def ic(k):
    if k in GEEL: return 9 if FP[k].mean()>170 else 8
    if k==13: return 3
    return int(((IP[1:14]-FP[k])**2).sum(1).argmin()+1)
h=n//2; o=np.zeros((h,h),np.uint8)
for j in range(h):
    for i in range(h):
        b=nat[2*j:2*j+2,2*i:2*i+2].ravel(); b=b[b>0]
        if len(b)<2: continue
        if 13 in b: o[j,i]=3; continue
        if sum(v in DONKER for v in b)>=2: o[j,i]=15; continue
        g=[v for v in b if v in GEEL]
        if len(g)>=2: o[j,i]=ic(max(set(g),key=g.count)); continue
        r=[v for v in b if v not in DONKER] or list(b)
        o[j,i]=ic(max(set(r),key=r.count))
ys,xs=np.nonzero(o); cc=o[ys.min():ys.max()+1,xs.min():xs.max()+1]; hh,ww=cc.shape
res=np.zeros((32,32),np.uint8); oy,ox=30-hh,16-ww//2
res[max(0,oy):oy+hh,max(0,ox):ox+ww]=cc[max(0,-oy):,max(0,-ox):][:32-max(0,oy),:32-max(0,ox)]
mm=res>0; pad=np.pad(mm,1); edge=mm&~(pad[:-2,1:-1]&pad[2:,1:-1]&pad[1:-1,:-2]&pad[1:-1,2:])
yy,_=np.nonzero(mm); mid=(yy.min()+yy.max())/2
for y,x in zip(*np.nonzero(edge)):
    if res[y,x] not in (8,9,3): res[y,x]=15 if y<mid else 14
im=Image.fromarray(res,'P'); im.putpalette(IP.flatten().tolist()); im.save(D+f'icoon/onderdelen/{naam}.png'); print(naam,ww,'x',hh)
