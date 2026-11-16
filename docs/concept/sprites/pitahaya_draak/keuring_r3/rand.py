from PIL import Image; import numpy as np
S=np.array(Image.open('sprite_r3/pitahaya_r3.png')); H=S>0
def tr(y,x): return not(0<=y<64 and 0<=x<64) or not H[y,x]
E={}
for y in range(64):
  for x in range(64):
    if H[y,x]:
      dirs=[(dy,dx) for dy,dx in((1,0),(-1,0),(0,1),(0,-1)) if tr(y+dy,x+dx)]
      if dirs: E[(x,y)]=dirs
lit=[];sh=[]
for (x,y),dirs in E.items():
    ny=sum(d[0] for d in dirs); nx=sum(d[1] for d in dirs)
    s=-ny-nx  # >0 = boven/links (licht)
    (lit if s>0 else sh if s<0 else []).append((x,y))
SEL={2,8}
print('randpixels',len(E),'licht',len(lit),'schaduw',len(sh))
print('licht: zwart',sum(S[y,x]==1 for x,y in lit),'selout',sum(S[y,x] in SEL for x,y in lit),'anders',[(x,y,S[y,x]) for x,y in lit if S[y,x] not in SEL|{1}])
print('schaduw: zwart',sum(S[y,x]==1 for x,y in sh),'selout',sum(S[y,x] in SEL for x,y in sh),'anders',[(x,y,S[y,x]) for x,y in sh if S[y,x] not in SEL|{1}])
print('zwart aan lichtkant:',sorted([(x,y) for x,y in lit if S[y,x]==1],key=lambda p:(p[1],p[0])))
# om-en-om: randpixel waarvan de 2 rand-buren (8-conn) beide van de andere soort zijn
alt=[]
for (x,y) in E:
    k=S[y,x]==1
    nb=[(x+dx,y+dy) for dy in(-1,0,1) for dx in(-1,0,1) if (dx or dy) and (x+dx,y+dy) in E]
    if len(nb)==2 and all((S[b[1],b[0]]==1)!=k for b in nb) and all(S[b[1],b[0]] in SEL|{1} for b in nb) and S[y,x] in SEL|{1}: alt.append((x,y,int(S[y,x])))
print('om-en-om:',sorted(alt,key=lambda p:(p[1],p[0])))
d=np.load('keuring_r2/model_per_px.npz'); mzw=d['mzw']
dub=[]
for (x,y),dirs in E.items():
    if S[y,x] not in SEL|{1}: continue
    for dy,dx in dirs:
        yy,xx=y-dy,x-dx
        if 0<=yy<64 and 0<=xx<64 and H[yy,xx] and (xx,yy) not in E and S[yy,xx] in SEL|{1}:
            dub.append((x,y,'->',xx,yy,int(S[yy,xx]),'mzw',int(mzw[yy,xx])))
print('buitenlijn 2 dik (randpixel + binnenbuur ook lijn):',len(dub))
for t in sorted(dub,key=lambda p:(p[1],p[0])): print(t)
print('mzw lichtkant-zwart:',[(x,y,int(mzw[y,x])) for x,y in [(23,49),(23,50),(20,52),(19,22),(19,23),(19,24),(18,25)]])
