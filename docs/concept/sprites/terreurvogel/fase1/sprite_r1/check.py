# Controle: maat, alpha-diff t.o.v. kale reductie, kleuren, lichte kleur op de buitenrand, tintclusters <3, afwijkingen per zone
import numpy as np; from PIL import Image
from lib import GROEPIDX
S=np.array(Image.open('kuiken_r1.png')); K=np.load('kaal.npy')
yy,xx=np.where(S>0); print('maat',xx.max()-xx.min()+1,'x',yy.max()-yy.min()+1,'bbox x',xx.min(),xx.max(),'y',yy.min(),yy.max(),'px',(S>0).sum())
print('alpha-diff t.o.v. kale reductie',int(((S>0)!=(K>0)).sum()))
print('gebruikte indices',sorted(set(S.ravel())-{0}),'aantal kleuren',len(set(S.ravel())-{0}))
IDXG={i:g for g,ids in GROEPIDX.items() for i in ids}
rand=[]; 
for y in range(64):
    for x in range(64):
        if S[y,x]==0: continue
        if any(not(0<=y+dy<64 and 0<=x+dx<64) or S[y+dy,x+dx]==0 for dy,dx in ((-1,0),(1,0),(0,-1),(0,1))):
            if S[y,x] not in (1,2,5,11): rand.append((x,y,int(S[y,x])))
print('randpixels die geen lijn/selout zijn',rand)
seen=np.zeros((64,64),bool); klein=[]
for y in range(64):
    for x in range(64):
        if seen[y,x] or S[y,x]<=1: continue
        v=S[y,x]; st=[(y,x)]; seen[y,x]=True; cl=[]
        while st:
            cy,cx=st.pop(); cl.append((cx,cy))
            for dy,dx in ((-1,0),(1,0),(0,-1),(0,1)):
                ny,nx=cy+dy,cx+dx
                if 0<=ny<64 and 0<=nx<64 and not seen[ny,nx] and S[ny,nx]==v: seen[ny,nx]=True; st.append((ny,nx))
        if len(cl)<3: klein.append((int(v),cl))
print('tintclusters <3 px:',len(klein)); 
for v,cl in klein: print('  ',v,IDXG.get(v),cl)
D=(S!=K)
zones={'snavel':(10,25,18,41),'kop':(18,41,17,40),'oog':(27,33,25,30),'borst/lijf':(14,56,40,55),'poten':(18,44,55,63)}
for z,(x0,x1,y0,y1) in zones.items():
    print('afwijkend t.o.v. kaal in %s: %d'%(z,int(D[y0:y1,x0:x1].sum())))
print('totaal afwijkend t.o.v. kaal',int(D.sum()))
