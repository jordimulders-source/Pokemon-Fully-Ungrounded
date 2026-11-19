# Pixelreparaties op schoon0 per zone (patches_basis.txt), daarna automatische buitenlijnpass (gelogd). Uitvoer basis.npy.
import numpy as np, json
from txt import CH, dump
I={c:i for i,c in enumerate(CH)}
PATCH=[]
def P(zone, spec, why):
    for t in spec.split():
        rc,v=t.split('='); r,c=map(int,rc.split(',')); PATCH.append((zone,r,c,v,why))
exec(open('patches_basis.txt').read())
a=np.load('schoon0.npy').copy(); H,W=a.shape; LOG=[]
for z,r,c,v,w in PATCH:
    if a[r,c]!=I[v]: LOG.append((z,r,c,CH[a[r,c]],v))
    a[r,c]=I[v]
# ontkorrel 2: tintvlakjes < 3 px (4-verbonden) -> meest voorkomende vlakkleur in de 4-buurt (eerst zelfde kleurgroep);
# uitgezonderd: ogen/glans, gele lont, vingertoppen links, stompje onder de staart, vlamkern, magentastreep onderaan de pijl
from collections import deque, Counter
KEEP={(27,14),(27,15),(14,7),(16,6),(17,6),(16,7),(17,7),(16,10),(17,11),(49,10),(50,10),(56,9),(56,10),(38,10),(39,10)}
GR={**{I[c]:'roze' for c in 'sml'},**{I[c]:'paars' for c in 'Mp'},**{I[c]:'geel' for c in 'Yt'},**{I[c]:'creme' for c in 'ck'}}
for _ in range(2):
    seen=np.zeros_like(a,bool); todo=[]
    for y in range(H):
        for x in range(W):
            if a[y,x]==0 or seen[y,x]: continue
            c=a[y,x]; q=deque([(y,x)]); seen[y,x]=1; comp=[]
            while q:
                cy,cx=q.popleft(); comp.append((cy,cx))
                for dy,dx in ((1,0),(-1,0),(0,1),(0,-1)):
                    ny,nx=cy+dy,cx+dx
                    if 0<=ny<H and 0<=nx<W and not seen[ny,nx] and a[ny,nx]==c: seen[ny,nx]=1; q.append((ny,nx))
            if len(comp)<3 and c in GR and not (set(comp)&KEEP): todo.append((comp,c))
    for comp,c in todo:
        nb=Counter()
        for y,x in comp:
            for dy,dx in ((1,0),(-1,0),(0,1),(0,-1)):
                ny,nx=y+dy,x+dx
                if 0<=ny<H and 0<=nx<W and a[ny,nx] in GR and a[ny,nx]!=c and (ny,nx) not in comp: nb[a[ny,nx]]+=1
        if not nb: continue
        same=[k for k in nb if GR[k]==GR[c]]
        new=max(same,key=lambda k:nb[k]) if same else nb.most_common(1)[0][0]
        for y,x in comp: LOG.append(('ontkorrel2',y,x,CH[a[y,x]],CH[new])); a[y,x]=new
# buitenlijnpass
G={**{I[c]:'roze' for c in 'smlL'},**{I[c]:'paars' for c in 'Mp'},**{I[c]:'geel' for c in 'Yt'},**{I[c]:'creme' for c in 'ckw'}}
ch=[]
for y in range(H):
    for x in range(W):
        v=a[y,x]
        if v==0 or CH[v] in '#dbE': continue
        nb={(dy,dx) for dy,dx in ((1,0),(-1,0),(0,1),(0,-1)) if not(0<=y+dy<H and 0<=x+dx<W) or a[y+dy,x+dx]==0}
        if not nb: continue
        g=G.get(v)
        if g=='creme': new='b'
        elif ((-1,0) in nb or (0,-1) in nb) and not ((1,0) in nb or (0,1) in nb): new='d'
        else: new='#' if (1,0) in nb else 'd'
        if CH[v]=='w' and False: continue
        ch.append((y,x,new))
for y,x,v in ch:
    LOG.append(('buitenlijn',y,x,CH[a[y,x]],v)); a[y,x]=I[v]
# r3: handreparaties uit het model (patches_r3.txt), NA de buitenlijnpass zodat ze definitief zijn
R3=[]
def B(zone,r0,c0,rows,why):
    for j,row in enumerate(rows.split()):
        for i,ch in enumerate(row):
            if ch!='?': R3.append((zone,r0+j,c0+i,ch,why))
def P(zone,spec,why):
    for t in spec.split():
        rc,v=t.split('='); r,c=map(int,rc.split(',')); R3.append((zone,r,c,v,why))
exec(open('patches_r3.txt').read())
exec(open('patches_r4.txt').read())
exec(open('patches_r5.txt').read())
exec(open('patches_r6.txt').read())
for z,r,c,v,w in R3:
    if a[r,c]!=I[v]: LOG.append(('r3 '+z,r,c,CH[a[r,c]],v))
    a[r,c]=I[v]
exec(open('patches_r7.txt').read())   # r7: kleurindex-ronde NA alle vormreparaties
np.save('basis.npy',a); json.dump(LOG,open('log_patch.json','w'),default=int)
if __name__=='__main__': dump(a)
