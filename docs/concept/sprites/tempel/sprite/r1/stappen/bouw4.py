# bouw4.py [T0drempel]: kale reductie: toonklassen uit het mediaan-model (meerderheid per blok), clusters <3 px weg,
# structurele lijnen (modelskelet, 1 px), buitenlijn, mos en deur uit het model. Geen handwerk.
import numpy as np, sys
from PIL import Image
from collections import deque
D='/home/user/Pokemon-Fully-Ungrounded/docs/concept/sprites/tempel/sprite/r1/stappen/'
M='/home/user/Pokemon-Fully-Ungrounded/docs/concept/sprites/tempel/referenties/model.webp'
TOP=float(sys.argv[1]) if len(sys.argv)>1 else 162
TS=float(sys.argv[2]) if len(sys.argv)>2 else 0.35
med=np.load(D+'medL.npy'); c=np.asarray(Image.open(M).convert('RGB')).astype(float); L=c.mean(2)
lines=np.asarray(Image.open(D+'lijnen_model.png'))>0
s=(983-46)/62; X0,Y0,left,top=46,57,1,3
# klassen: 3 T0 top, 4 T1 front, 5 T2 (front schaduw), 6 T3 zijkant, 7 T4 donker, 12 deur
K=np.full(med.shape,6); K[med>=TOP]=3; K[(med>=145)&(med<TOP)]=4; K[(med>=128)&(med<145)]=5; K[(med>=95)&(med<128)]=6; K[(med>=70)&(med<95)]=7; K[med<70]=12
d=np.load(D+'red.npz'); a=d['alpha']; mean=d['mean']; lum=d['lum']
m=np.load(D+'masker.npy')
G=np.zeros((64,64),int); GR=np.zeros((64,64))
for by in range(60):
  for bx in range(62):
    ya,yb=int(Y0+by*s),int(Y0+(by+1)*s); xa,xb=int(X0+bx*s),int(X0+(bx+1)*s)
    y,x=top+by,left+bx
    if not m[y,x]: continue
    k=K[ya:yb,xa:xb]; ok=(L[ya:yb,xa:xb]<235)&~lines[ya:yb,xa:xb]
    v=k[ok] if ok.any() else k.ravel()
    G[y,x]=np.bincount(v).argmax()
    cc=c[ya:yb,xa:xb][ok] if ok.any() else c[ya:yb,xa:xb].reshape(-1,3)
    GR[y,x]=((cc[:,1]-cc[:,0])>8).mean()
# clusters < 3 px opgaan in meest voorkomende buur (ruis)
def clusters(G):
    seen=np.zeros_like(G,bool); out=[]
    for y in range(64):
      for x in range(64):
        if G[y,x] and not seen[y,x]:
          q=[(y,x)]; seen[y,x]=1; comp=[]
          while q:
            p=q.pop(); comp.append(p)
            for yy,xx in ((p[0]+1,p[1]),(p[0]-1,p[1]),(p[0],p[1]+1),(p[0],p[1]-1)):
              if 0<=yy<64 and 0<=xx<64 and not seen[yy,xx] and G[yy,xx]==G[y,x]: seen[yy,xx]=1; q.append((yy,xx))
          out.append(comp)
    return out
for it in range(3):
  for comp in clusters(G):
    if len(comp)<3 and G[comp[0]]!=12:
      nb=[G[yy,xx] for (y,x) in comp for yy,xx in ((y+1,x),(y-1,x),(y,x+1),(y,x-1)) if 0<=yy<64 and 0<=xx<64 and G[yy,xx] and (yy,xx) not in comp]
      if nb: 
        for p in comp: G[p]=np.bincount(nb).argmax()
door=G==12
# mos
moss=m&(GR>=0.3)&~door
G[moss&(lum>=110)]=8; G[moss&(lum<110)]=9
# lijnen
skS=np.load(D+'skthick.npy')
def zs(img):
    img=img.copy().astype(np.uint8)
    while True:
        ch=False
        for it in (0,1):
            P=np.pad(img,1)
            n=[P[:-2,1:-1],P[:-2,2:],P[1:-1,2:],P[2:,2:],P[2:,1:-1],P[2:,:-2],P[1:-1,:-2],P[:-2,:-2]]
            B=sum(n); A=sum(((n[i]==0)&(n[(i+1)%8]==1)).astype(int) for i in range(8))
            if it==0: c1=n[0]*n[2]*n[4]; c2=n[2]*n[4]*n[6]
            else: c1=n[0]*n[2]*n[6]; c2=n[0]*n[4]*n[6]
            dd=(img==1)&(B>=2)&(B<=6)&(A==1)&(c1==0)&(c2==0)
            if dd.any(): img[dd]=0; ch=True
        if not ch: return img.astype(bool)
pad=np.pad(m,1); edge=m&~(pad[:-2,1:-1]&pad[2:,1:-1]&pad[1:-1,:-2]&pad[1:-1,2:])
LN=zs((m&(skS>=TS*s))|edge)|edge
LN&=~door
P=np.pad(LN,1); nb=sum(np.roll(np.roll(P,dy,0),dx,1)[1:-1,1:-1] for dy in (-1,0,1) for dx in (-1,0,1) if dy or dx)
LN&=~((nb==0)&~edge)
G[LN]=2; G[edge]=1
np.save(D+'kaal4.npy',G)
