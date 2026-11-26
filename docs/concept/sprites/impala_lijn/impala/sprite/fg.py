# Voorgrondmasker van model_r5: achtergrond = wit gebied verbonden met de rand (floodfill),
# zodat het witte borst/buikvlak binnen de zwarte lijn voorgrond blijft. Ingesloten witte gaten tussen
# onderdelen worden gelijst (gaten.npy, gaten_viz.png); gat 1 (tussen de poten) is achtergrond, de rest (witte borst, glans) voorgrond. Uit: witlab.npz
import numpy as np
from PIL import Image, ImageDraw
a=np.asarray(Image.open('../referenties/model_r5.png').convert('RGB')).astype(int)
wit=(a.min(2)>=232)
m=Image.fromarray((wit*255).astype('uint8'),'L')
M=np.where(wit,255,0).astype('uint8')
# ingesloten witte componenten (BFS)
from collections import deque
E=(M==255); seen=np.zeros(E.shape,bool); comps=[]; PTS=[]; H,W=E.shape
for y0,x0 in zip(*np.nonzero(E)):
    if seen[y0,x0]: continue
    q=deque([(y0,x0)]); seen[y0,x0]=True; pts=[]
    while q:
        y,x=q.popleft(); pts.append((y,x))
        for dy,dx in((1,0),(-1,0),(0,1),(0,-1)):
            ny,nx=y+dy,x+dx
            if 0<=ny<H and 0<=nx<W and E[ny,nx] and not seen[ny,nx]: seen[ny,nx]=True; q.append((ny,nx))
    P=np.array(pts); PTS.append(P);comps.append((len(pts),P[:,1].min(),P[:,0].min(),P[:,1].max(),P[:,0].max(),int(P[:,1].mean()),int(P[:,0].mean())))
order=sorted(range(len(comps)),key=lambda i:-comps[i][0]); comps=[comps[i] for i in order]; PTS=[PTS[i] for i in order]
for c in comps[:25]: print(c)
rand=[c for c in comps if c[1]==0 or c[2]==0 or c[3]==1023 or c[4]==1023]
binnen=[c for c in comps if c not in rand and c[0]>=50]
for i,c in enumerate(binnen): print('gat',i,c)
np.save('gaten.npy',np.array([c[:5] for c in binnen]))


lab=np.full(E.shape,-1)
for i,c in enumerate(comps):
    if c in rand: lab[PTS[i][:,0],PTS[i][:,1]]=-2
    elif c[0]>=50: lab[PTS[i][:,0],PTS[i][:,1]]=binnen.index(c)
np.savez_compressed('witlab.npz',a=lab.astype('int16'))
viz=a.copy().astype('uint8'); 
cols=[(255,0,0),(0,180,0),(0,0,255),(255,150,0),(200,0,200),(0,200,200),(120,120,0),(255,0,120),(0,90,160),(160,90,0),(90,0,160),(0,160,90),(255,90,90),(90,255,90),(90,90,255),(200,200,0)]
for i in range(len(binnen)): viz[lab==i]=cols[i%len(cols)]
from PIL import ImageDraw
V=Image.fromarray(viz); d=ImageDraw.Draw(V)
for i,c in enumerate(binnen): d.text((c[1],c[2]),str(i),fill=(0,0,0))
V.save('gaten_viz.png')
