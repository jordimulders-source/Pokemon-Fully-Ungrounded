# r6.py A|B: vanaf r5. Riem als één doorlopende boog met het laagste punt onder de gesp; gesp A trapezium, B afgeronde hoeken; gat 2x3.
# glansrij = alleen de bovenste bandrij links (14), geen gespikkelde overgangen; boog iets vlakker zodat de trappen langer worden.
# (2) gesp in driekwart: naar links verschoven (buikmidden bij x~21, onder de neus/snor-as), ingekort (6 breed x 7 hoog),
# voorkant 4 px (gat 1x3, staand) + rechterkolom donker als zijkant (dikte); proef met 1 px lagere rechterhelft las rommelig. Kleuren crème op bruin zoals r4.
# Alleen pixels in lijf/broek/riem veranderen (assert); roze/blauw dat vrijkomt of verdwijnt krijgt dezelfde belichting als r1 (maak.py).
import sys, numpy as np; from PIL import Image
sys.path.insert(0,'../sprite_r1'); from gemeen import opslaan
R1='../sprite_r1/'
zone=np.load(R1+'zone_af.npy'); L=np.load(R1+'lijn.npy'); riem1=np.load(R1+'riem.npy')
zone[43,26]=5; L[43,26]=False
r5i=Image.open('../sprite_r5/gnomad.png'); pal=[tuple(r5i.getpalette()[3*k:3*k+3]) for k in range(16)]
r5=np.asarray(r5i).astype(int); o=r5.copy()
body=(np.isin(zone,(5,8))|riem1)&~L
cx,cy,rx,ry=27.0,45.5,14.0,8.5
l=np.array([-0.55,-0.6,0.58]); l/=np.linalg.norm(l)
def I(X,Y):
    nx=(X+0.5-cx)/rx; ny=(Y+0.5-cy)/ry; r2=nx*nx+ny*ny
    n=np.array([nx,ny,np.sqrt(max(0.04,1-min(r2,0.96)))]); n/=np.linalg.norm(n); return float(n@l)
# r6: riem als één doorlopende boog. In driekwart ligt de voorkant van de bol bij de gesp (x21); vanaf de linkerflank tot voorbij de gesp
# loopt de riem vlak (bovenrand rij 44, links en rechts van de gesp op één lijn, zelfde dikte), daarna buigt hij naar de rechterflank omhoog.
# (Proef met een steile boog links gaf het stuk links van de gesp 1 rij hoger dan rechts = het sprongetje dat Jordi zag.)
def top(X):
    if X<=29: return 44.0
    u=(X-29)/12.0; return 44.0-2.6*u*u
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
import sys as _s
VAR=_s.argv[1]
G={'A':["kkkkk.",     # trapezium: rechterkant 2 px korter (wijkt terug), bovenrand volgt de boog
        "kHCCOk",
        "kCbbOk",
        "kCbbOk",
        "kCbbOk",
        "kCCOOk",
        "kkkkk."],
   'B':[".kkkk.",     # afgeronde hoeken
        "kHCCOk",
        "kCbbOk",
        "kCbbOk",
        "kCbbOk",
        "kCCOOk",
        ".kkkk."]}[VAR]
M={'k':1,'C':12,'H':13,'O':14,'b':15}
# buitenlijn links naast de riem: roze selout boven de riem, zwart langs de riem (was blauwe selout van de oude broekgrens)
for x,y,k in [(14,43,6),(14,44,1),(14,45,1),(15,46,1)]: o[y,x]=k
X0=18; T0=int(round(top(21)))-1
gesp=np.zeros((64,64),bool)
for j,r in enumerate(G):
    for i,c in enumerate(r):
        if c=='.': continue
        o[T0+j,X0+i]=M[c]; gesp[T0+j,X0+i]=True
d=o!=r5; zm=body|gesp|riem1|np.isin(zone,(5,8))
assert not (d&~zm).any(), np.argwhere(d&~zm)
opslaan(o,'gnomad_%s.png'%VAR,pal)
print(VAR,'diff t.o.v. r5: lijf/broek/riem %d px, gesp %d px, elders 0'%((d&~gesp).sum(),(d&gesp).sum()))
