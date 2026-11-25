# r12: kop = r11-kop (kopvorm naar Mr. Mime: 2 voorhoofdrijen eruit -> koepel even hoog als Mr. Mimes kop);
# romp, heupen (broek), schouderballen en armen = Mr. Mime (frame 1), omgekleurd naar het grijze palet;
# vuisten, benen en schoenen = r11 (ongewijzigd). V = r11. Pose als r11.
import numpy as np, sys
from PIL import Image
MM=np.array(Image.open('../../../../../../graphics/pokemon/mr_mime/anim_front_gba.png'))[:64,:64]
r11=np.load('../sprite_r11/bokser.npy')
DX,DY=0,4                         # Mr. Mime -> eindcoördinaten (kin op kin)
B=38                              # Mr. Mime-rij van de tailleband (broek eronder)
F=np.zeros((64,64),int)
def put(layer):
    for (x,y),v in layer.items():
        if 0<=x<64 and 0<=y<64: F[y,x]=v
# ---------- kop (r11 kop_ruw + reparaties), dan 2 voorhoofdrijen (r11-rij 18,19) eruit
kop=np.load('../sprite_r11/kop_ruw.npy'); K=np.zeros((64,64),int)
for y,x in zip(*np.where(kop)):
    if 0<=y+3<64 and 0<=x-20<64: K[y+3,x-20]=kop[y,x]
for (x,y),v in {(40,28):0,(41,28):0,(48,16):0,(49,16):0,(50,16):0,(31,12):1,(46,12):1,(32,13):1,(41,16):1,(41,18):1,
                (39,23):7,(39,24):7,(36,21):7,(38,26):7,(23,25):8}.items(): K[y,x]=v
K2=K.copy(); K2[2:20]=K[0:18]; K2[0:2]=0
KOP={(x,y):K2[y,x] for y,x in zip(*np.where(K2))}
# ---------- Mr. Mime-delen (orig. coördinaten -> omkleuren)
def mm(rows,xs,keep,cmap):
    out={}
    for y in rows:
        for x in xs:
            v=int(MM[y,x])
            if v and keep(x,y,v):
                c=cmap(x,y,v)
                if c is not None: out[(x+DX,y+DY)]=c
    return out
SKIN={9:8,10:8,11:7,5:7,12:1,14:1}
VERARM =mm(range(30,34),range(12,18),lambda x,y,v:v in SKIN,lambda x,y,v:SKIN[v])
VERSCH =mm(range(29,35),range(17,21),lambda x,y,v:v in(5,6,7,8,14),lambda x,y,v:{5:7,6:5,7:4,8:1,14:1}[v])
cirkel=lambda x,y:23<=x<=31 and 31<=y<=41
nabschouder=lambda x,y:(27<=y<=35 and x>=34 and not(y>=34 and x<=34)) and not(y<=28 and x<=36)
def romp_keep(x,y,v):
    if nabschouder(x,y) and v in(5,6,7,8,10,11): return False
    if y>=41 and x<=18 and v in(3,10,11,12): return False   # beenaanzet Mr. Mime
    if x<=20 and y<=35 and v!=4: return False                # verre schouder (eigen laag)
    if y>=43 and x>=38 and v in(10,11,12,3): return False
    return v in(15,1,2,4,14,5,6,7,8) and not(y==29 and 26<=x<=33)
def romp_c(x,y,v):
    rood=v in(5,6,7,8) and not cirkel(x,y)
    if rood:                                   # heupbollen = broek
        return {5:5,6:3,7:2,8:1}[v]
    if v==14: return 1
    if v==4: return 4 if y<B else 1
    if cirkel(x,y) and v in(5,6,7,8): v={5:15,6:15,7:1,8:1}[v]   # rode cirkel weg: buikwit
    if y<B:  return {15:8,1:7,2:6}[v]
    if y==B: return {15:7,1:6,2:6}[v]           # tailleband
    return {15:3,1:3,2:2}[v]                   # broek over de onderbuik
ROMP=mm(range(29,44),range(15,41),romp_keep,romp_c)
NABSCH=mm(range(27,36),range(34,45),lambda x,y,v:nabschouder(x,y) and v in(5,6,7,8,10,14),lambda x,y,v:{5:7,6:5,7:4,8:2,10:7,14:1}[v])
NABARM=mm(range(34,40),range(38,47),lambda x,y,v:v in(11,10,12,14) and not(y<=37 and x>=43) and x<=43,lambda x,y,v:{10:8,11:7,12:1,14:1}[v])
# ---------- r11-delen
def r11deel(rows,xs,dx=0,dy=0):
    return {(x+dx,y+dy):int(r11[y,x]) for y in rows for x in xs if r11[y,x]}
VUIST =r11deel(range(25,32),range(8,16),0,int(sys.argv[1]) if len(sys.argv)>1 else 2)
BORST ={}
for y,x0,s in [(34,32,'1111'),(35,31,'157531'),(36,30,'15525321'),(37,30,'13311111'),(38,31,'1251531'),(39,32,'11111')]:
    for i,ch in enumerate(s): BORST[(x0+i,y)]=int(ch)
V={}
for y,x0,n in [(34,26,6),(35,26,4),(36,26,3),(37,27,2),(38,28,1)]:
    for x in range(x0,x0+n): V[(x,y)]=3
BENEN=r11deel(range(50,63),range(20,45),int(sys.argv[2]) if len(sys.argv)>2 else -2,-2)
# ---------- lagen
for L in (VERARM,VERSCH,BENEN,ROMP,V,NABSCH,NABARM,KOP,BORST,VUIST): put(L)
np.save('ruw.npy',F)
ys,xs=np.where(F); print('maat',xs.max()-xs.min()+1,'x',ys.max()-ys.min()+1,'rijen',ys.min(),ys.max())
# ---------- schone rand: lichte pixel tegen achtergrond -> zwarte lijn erbuiten (geen open randen)
G=F.copy()
for y,x in zip(*np.where(F>=5)):
    for dy,dx in((1,0),(-1,0),(0,1),(0,-1)):
        if F[y+dy,x+dx]==0: G[y+dy,x+dx]=1
F=G; np.save('ruw.npy',F)
ys,xs=np.where(F); print('na rand: maat',xs.max()-xs.min()+1,'x',ys.max()-ys.min()+1)
