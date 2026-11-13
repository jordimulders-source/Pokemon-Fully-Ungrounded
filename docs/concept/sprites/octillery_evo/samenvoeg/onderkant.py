# Model = r16. Rechter rupsband uitknippen en als tweede (linker) rupsband achter het lijf plakken; zuignappen geel; wratten op de 2 lage tentakels.
# Gebruik: python3 onderkant.py DX DY
import sys; from PIL import Image, ImageDraw, ImageFilter; import numpy as np
from collections import deque
DX,DY=int(sys.argv[1]),int(sys.argv[2])
S='/tmp/claude-0/-home-user-Pokemon-Fully-Ungrounded/edb145cf-71a4-55a5-8012-167050278397/scratchpad/'
A=np.asarray(Image.open('gemini/r16_P4.png').convert('RGB')).copy(); H,W=A.shape[:2]; bg=A[5,5].copy()
nonbg=A.min(axis=2)<235
# 1. rechter rupsband: floodfill binnen de donkere omlijning
dark=(A.max(axis=2)<75)|~nonbg
seen=np.zeros((H,W),bool); q=deque()
for x,y in [(560,760),(640,780),(700,790),(780,790),(840,760),(600,720),(820,730),(700,735)]:
    if not dark[y,x]: seen[y,x]=True; q.append((y,x))
while q:
    y,x=q.popleft()
    for dy,dx in ((1,0),(-1,0),(0,1),(0,-1)):
        ny,nx=y+dy,x+dx
        if 690<=ny<H and 505<=nx<W and not seen[ny,nx] and not dark[ny,nx]:
            seen[ny,nx]=True; q.append((ny,nx))
m=Image.fromarray((seen*255).astype('uint8')).filter(ImageFilter.MaxFilter(15))
f=m.copy(); ImageDraw.floodfill(f,(0,0),128); M=(np.asarray(f)!=128)&nonbg
M[:690]=False; M[:, :505]=False
Image.fromarray(np.where(M[...,None],A,255).astype('uint8')).crop((480,660,900,860)).save(S+'tread.png')
# 2. samenstellen: kopie links (achter), dan het model zonder de oude linker rupsband erbovenop
out=np.empty_like(A); out[:]=bg
ys,xs=np.where(M); out[ys+DY,xs+DX]=A[ys,xs]
Y,X=np.mgrid[0:H,0:W]
# oude linker rupsband: zelfde floodfill, daarna weg
seen2=np.zeros((H,W),bool); q=deque()
for x,y in [(200,740),(300,765),(400,765),(170,780),(450,750),(260,725),(430,790)]:
    if not dark[y,x]: seen2[y,x]=True; q.append((y,x))
while q:
    y,x=q.popleft()
    for dy,dx in ((1,0),(-1,0),(0,1),(0,-1)):
        ny,nx=y+dy,x+dx
        if 688<=ny<H and 120<=nx<525 and not seen2[ny,nx] and not dark[ny,nx]:
            seen2[ny,nx]=True; q.append((ny,nx))
m2=Image.fromarray((seen2*255).astype('uint8')).filter(ImageFilter.MaxFilter(15))
f2=m2.copy(); ImageDraw.floodfill(f2,(0,0),128); M2=(np.asarray(f2)!=128)&nonbg; M2[:688]=False; M2[:,525:]=False
Image.fromarray(np.where(M2[...,None],A,255).astype('uint8')).crop((100,660,560,860)).save(S+'oud.png')
keep=nonbg&~M2
out[keep]=A[keep]
# 3. zuignappen op beide rupsbanden geel
r,g,b=out[...,0].astype(int),out[...,1].astype(int),out[...,2].astype(int)
ring=(r>180)&(g>95)&(g<175)&(b>100)&(Y>=700)
out[ring]=(226,186,84)
# 4. wratten op de twee lage tentakels: bestaande wrat kopieren (verkleind)
wb=A[584:632,682:732].astype(int); wm=(wb[...,0]>170)&(wb[...,1]>125)&(wb[...,0]-wb[...,2]>45)
w=Image.fromarray(np.dstack([wb,wm*255]).astype('uint8'),'RGBA')
bb=w.getbbox(); w=w.crop(bb); w=w.resize((round(w.width*0.62),round(w.height*0.62)),Image.NEAREST)
o=Image.fromarray(out).convert('RGBA')
WARTS=[(178,650),(222,636),(266,640),(792,652),(832,640),(852,598)]
import json,os
if os.path.exists('samenvoeg/warts.json'): WARTS=json.load(open('samenvoeg/warts.json'))
for cx,cy in WARTS: o.alpha_composite(w,(cx-w.width//2,cy-w.height//2))
out=np.asarray(o.convert('RGB')).copy()
Image.fromarray(out).save('samenvoeg/model_v4.png')
Image.fromarray(out).crop((120,540,520,720)).resize((1200,540),Image.NEAREST).save(S+'wl.png')
Image.fromarray(out).crop((640,520,900,720)).resize((780,600),Image.NEAREST).save(S+'wr.png')
Image.fromarray(out).crop((100,560,900,860)).save(S+'v4.png')
