# Segmenteert het model in vlakken begrensd door de zwarte modellijn (max kanaal < 60), voor zonetoewijzing
# (vacht / wit / staal / kuif / hoef / oog / neus). Uit: seg.npy (-1 = lijn of achtergrond), seg_viz.png
import numpy as np
from PIL import Image, ImageDraw
from collections import deque
a=np.asarray(Image.open('../referenties/model_r5.png').convert('RGB')).astype(int)
wl=np.load('witlab.npz')['a']; bg=(wl==-2)|(wl==1)
E=(~bg)&(a.max(2)>=60); H,W=E.shape
seg=np.full(E.shape,-1); info=[]; n=0
for y0,x0 in zip(*np.nonzero(E)):
    if seg[y0,x0]>=0: continue
    q=deque([(y0,x0)]); seg[y0,x0]=n; pts=[]
    while q:
        y,x=q.popleft(); pts.append((y,x))
        for dy,dx in((1,0),(-1,0),(0,1),(0,-1)):
            ny,nx=y+dy,x+dx
            if 0<=ny<H and 0<=nx<W and E[ny,nx] and seg[ny,nx]<0: seg[ny,nx]=n; q.append((ny,nx))
    P=np.array(pts); info.append((len(pts),int(P[:,1].mean()),int(P[:,0].mean()))); n+=1
np.savez_compressed('seg.npz',a=seg.astype('int16'))
big=[i for i,c in enumerate(info) if c[0]>=150]
print(len(info),'vlakken,',len(big),'>=150 px')
rng=np.random.default_rng(1); viz=np.full((H,W,3),255,'uint8'); viz[(~bg)&(seg<0)]=0
for i in big: viz[seg==i]=rng.integers(60,255,3)
V=Image.fromarray(viz).resize((2048,2048),Image.NEAREST); d=ImageDraw.Draw(V)
for i in big: d.text((info[i][1]*2,info[i][2]*2),str(i),fill=(0,0,0))
V.save('seg_viz.png')
for i in big: print(i,info[i])
