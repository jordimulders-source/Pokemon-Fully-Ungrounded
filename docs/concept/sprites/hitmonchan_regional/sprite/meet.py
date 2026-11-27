# meet.py: per spritepixel het modelgebied (zelfde stuksgewijze afbeelding als r1b) -> M_donker (donkerste natieve index met >=15% oppervlak),
# M_licht (lichtste), M_gem (dichtstbijzijnde paletkleur bij het oppervlaktegewogen gemiddelde RGB). Opgeslagen als .npy (64x40).
import numpy as np, sys
from PIL import Image
D='docs/concept/sprites/hitmonchan_regional/sprite/'
sys.path.insert(0,D); from toon import lab
q=np.load(D+'natief_q.npy'); pal=eval(open(D+'pal.txt').read()); nat=np.asarray(Image.open(D+'natief.png').convert('RGB')).astype(float)
PL=lab(np.array(pal[1:],float))
def randen(N,a,b,A,uit):
    k1=a/A; B=A+(b-a); k2=(N-b)/(uit-B); return [i*k1 if i<=A else (a+(i-A) if i<=B else b+(i-B)*k2) for i in range(uit+1)]
def ov(e,i):
    lo,hi=e[i],e[i+1]; return [(n,min(hi,n+1)-max(lo,n)) for n in range(int(np.floor(lo)),int(np.ceil(hi))) if min(hi,n+1)-max(lo,n)>1e-6]
ry=randen(81,24,32,18,64); cx=randen(50,28,38,21,40)
Dk=np.zeros((64,40),int); Li=Dk.copy(); G=Dk.copy()
for y in range(64):
    for x in range(40):
        cel=[(q[n,m],wy*wx,nat[n,m]) for n,wy in ov(ry,y) for m,wx in ov(cx,x) if n<81 and m<50]
        tot=sum(w for _,w,_ in cel); f=[(i,w/tot) for i,w,_ in cel if i>0 and w/tot>=0.15]
        Dk[y,x]=min(i for i,_ in f) if f else 0; Li[y,x]=max(i for i,_ in f) if f else 0
        fg=[(c,w) for i,w,c in cel if i>0]
        if fg:
            c=sum(c*w for c,w in fg)/sum(w for _,w in fg); G[y,x]=int(((PL-lab(c))**2).sum(1).argmin())+1
np.save(D+'M_donker.npy',Dk); np.save(D+'M_licht.npy',Li); np.save(D+'M_gem.npy',G)
