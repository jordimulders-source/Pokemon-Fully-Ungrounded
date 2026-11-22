# r5.py: r4 -> r5. (1) riem rustiger: vaste opbouw per kolom (zwarte lijn, 3 rijen band, zwarte lijn), band = 1 hoofdtint (15),
# glansrij = alleen de bovenste bandrij links (14), geen gespikkelde overgangen; boog iets vlakker zodat de trappen langer worden.
# (2) gesp in driekwart: naar links verschoven (buikmidden bij x~21, onder de neus/snor-as), ingekort (6 breed x 7 hoog),
# voorkant 4 px (gat 1x3, staand) + rechterkolom donker als zijkant (dikte); proef met 1 px lagere rechterhelft las rommelig. Kleuren crème op bruin zoals r4.
# Alleen pixels in lijf/broek/riem veranderen (assert); roze/blauw dat vrijkomt of verdwijnt krijgt dezelfde belichting als r1 (maak.py).
import sys, numpy as np; from PIL import Image
sys.path.insert(0,'../sprite_r1'); from gemeen import opslaan
R1='../sprite_r1/'
zone=np.load(R1+'zone_af.npy'); L=np.load(R1+'lijn.npy'); riem1=np.load(R1+'riem.npy')
zone[43,26]=5; L[43,26]=False
r4i=Image.open('../sprite_r4/gnomad.png'); pal=[tuple(r4i.getpalette()[3*k:3*k+3]) for k in range(16)]
r4=np.asarray(r4i).astype(int); o=r4.copy()
body=(np.isin(zone,(5,8))|riem1)&~L
cx,cy,rx,ry=27.0,45.5,14.0,8.5
l=np.array([-0.55,-0.6,0.58]); l/=np.linalg.norm(l)
def I(X,Y):
    nx=(X+0.5-cx)/rx; ny=(Y+0.5-cy)/ry; r2=nx*nx+ny*ny
    n=np.array([nx,ny,np.sqrt(max(0.04,1-min(r2,0.96)))]); n/=np.linalg.norm(n); return float(n@l)
def top(X): u=(X-25.0)/14.0; return 41.3+2.6*(1-u*u)+0.7*u
B=3
for Y,X in zip(*np.where(body)):
    t=int(round(top(X)))
    if Y==t or Y==t+B+1: o[Y,X]=1
    elif t<Y<=t+B: o[Y,X]=14 if (Y==t+1 and 15<=X<=21) else 15
    elif Y<t:
        o[Y,X]=8 if I(X,Y)>=0.30 else 7
        if zone[Y-1,X] in (1,2,3,4) or (L[Y-1,X] and zone[Y-2,X] in (1,2,3,4)): o[Y,X]=7
    elif Y==t+B+2: o[Y,X]=10 if X<30 else 9
    else:
        i=I(X,Y); o[Y,X]=11 if i>=0.25 else (10 if i>=-0.25 else 9)
# r4: pixels die buiten 'body' vielen maar riem/gesp waren (bijv. gesprij boven de band) -> uit r3-B/r2 terugzetten waar nodig
r2=np.asarray(Image.open('../sprite_r2/gnomad_A.png')).astype(int)
nb=~body
o[nb]=r2[nb]
# gesp: 6x7, x18-23; linkerhelft begint 1 rij boven de band, rechterhelft 1 px lager
G=["kkkkkk",
   "kHCCOk",
   "kCbCOk",
   "kCbCOk",
   "kCbCOk",
   "kCCCOk",
   "kkkkkk"]
M={'k':1,'C':12,'H':13,'O':14,'b':15}
X0=18; T0=int(round(top(20)))-1
gesp=np.zeros((64,64),bool)
for j,r in enumerate(G):
    for i,c in enumerate(r):
        if c=='.': continue
        o[T0+j,X0+i]=M[c]; gesp[T0+j,X0+i]=True
d=o!=r4; zm=body|gesp|riem1|np.isin(zone,(5,8))
assert not (d&~zm).any(), np.argwhere(d&~zm)
opslaan(o,'gnomad.png',pal)
print('diff t.o.v. r4: lijf/broek/riem %d px, gesp %d px, elders 0'%((d&~gesp).sum(),(d&gesp).sum()))
