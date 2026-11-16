# Kopzone (ijzercomponent van de kop, buitenrand, gezichtslijnen) + lijnregel DY=0; gebruikt door maak.py.
import sys; sys.path.insert(0,'sprite_r15')
from basis import *
from toon import crop, mod, rij
r=np.array(Image.open('sprite_r14/sprite.png'))
GR={2,3,4,5,6,13}; IJ={1,7,8,9,10,11,12}
L,T=lijnregel(0)
# kop = ijzercomponent vanaf (30,15), groen en transparant zijn grens, rijen 20..44
from collections import deque
kop=np.zeros((64,64),bool); q=deque([(30,15)]); kop[30,15]=True
while q:
    y,x=q.popleft()
    for dy,dx in((0,1),(1,0),(0,-1),(-1,0)):
        Y,X=y+dy,x+dx
        if 20<=Y<=44 and 0<=X<64 and not kop[Y,X] and r[Y,X] in IJ: kop[Y,X]=True; q.append((Y,X))
def buiten(a,y,x): return x==0 or any(a[y+dy,x+dx]==0 for dy,dx in((0,1),(1,0),(0,-1),(-1,0)))
groen=np.isin(r,list(GR))
gz=np.zeros((64,64),bool)   # binnen 2 px van groen
for y in range(64):
    for x in range(64):
        gz[y,x]=groen[max(0,y-2):y+3,max(0,x-2):x+3].any()
gezicht=(r==1)&gz&kop&(np.arange(64)[:,None]>=26)
rand=np.array([[kop[y,x] and buiten(r,y,x) for x in range(64)] for y in range(64)])
zone=kop&~rand&~gezicht
if __name__=='__main__':
    print('kop',kop.sum(),'rand',rand.sum(),'gezichtslijn',gezicht.sum(),'zone',zone.sum(), 'kop x-bereik',np.where(kop)[1].min(),np.where(kop)[1].max())
    for y in range(18,46): print('%2d '%y+''.join('R' if rand[y,x] else 'F' if gezicht[y,x] else ('L' if L[y,x] else 'z') if zone[y,x] else '.' for x in range(40)))

def kwant_kop(c_h,c_l,CH=45,B1=130,B2=100,G0=152,G1=112,G2=80,GL=150,SCH=109):
    chroma=c_h[0]-c_h[2]; l=0.3*c_l[0]+0.59*c_l[1]+0.11*c_l[2]
    if chroma>CH: return 7 if l>B1 else (8 if l>B2 else 9)
    return 7 if l>G0 else (10 if l>G1 else (11 if l>G2 else 12))
def maak_kop(sh,sl,sb=None,**kw):
    Gh=glad(sh); Gl=glad(sl) if sl>0 else N; Gb=glad(sb,BRUIN) if sb else None
    a=r.copy()
    for y,x in zip(*np.where(zone)):
        if L[y,x]: a[y,x]=1; continue
        ch=vul(x,y,Gh,0); cl=vul(x,y,Gl,0)
        if ch is None: continue
        a[y,x]=kwant_kop(ch,cl,**kw)
        if Gb is not None and a[y,x] in (7,8,9):
            # bruin: 7 alleen bij echte glans in het model (fijn gemiddelde), anders 8; schaduw 9 uit het grove gemiddelde (bolle schaduw)
            cb=vul(x,y,Gb,0,BRUIN); lb=0.3*cb[0]+0.59*cb[1]+0.11*cb[2] if cb is not None else 999
            ll=0.3*cl[0]+0.59*cl[1]+0.11*cl[2]
            a[y,x]=7 if ll>kw.get('GL',150) else (9 if lb<kw.get('SCH',109) else 8)
    return a
