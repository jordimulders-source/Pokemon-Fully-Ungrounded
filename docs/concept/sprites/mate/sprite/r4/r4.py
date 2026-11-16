# Ronde 4 (Jordi's punten op r3). Basis = r3; lijfvulling opnieuw uit de gemeten modelhelderheid (toon.py, laagdoorlaat),
# daarna per zone pixels naar gemeten modelvormen (frac.py/zij.py). Elke zone logt het aantal pixels t.o.v. r3.
import sys; sys.path.insert(0,'r4')
import numpy as np; from PIL import Image
im=Image.open('r3/mate.png'); PAL=im.getpalette(); r3=np.asarray(im).astype(int)
a=np.load(sys.argv[1]).astype(int)   # toon.py-uitvoer (stap A)
L={'.':0,'#':1,'a':2,'b':3,'c':4,'d':5,'G':6,'H':7,'I':8,'s':9,'t':10,'u':11}
H_,W_=a.shape
def clusters(a,v):
    seen=np.zeros(a.shape,bool); out=[]
    for y in range(H_):
        for x in range(W_):
            if a[y,x]!=v or seen[y,x]: continue
            st=[(y,x)]; seen[y,x]=True; c=[]
            while st:
                q=st.pop(); c.append(q)
                for dy,dx in ((1,0),(-1,0),(0,1),(0,-1)):
                    yy,xx=q[0]+dy,q[1]+dx
                    if 0<=yy<H_ and 0<=xx<W_ and not seen[yy,xx] and a[yy,xx]==v: seen[yy,xx]=True; st.append((yy,xx))
            out.append(c)
    return out
# stap B: tintvlakjes < 3 px in de vulling (b/c/d) opgaan in de meest voorkomende vulbuur
for rnd in range(3):
    b=a.copy()
    for v in (3,4,5):
        for c in clusters(a,v):
            if len(c)>=3: continue
            cnt={}
            for y,x in c:
                for dy,dx in ((1,0),(-1,0),(0,1),(0,-1)):
                    w=a[y+dy,x+dx]
                    if w in (3,4,5) and w!=v: cnt[w]=cnt.get(w,0)+1
            if cnt:
                for y,x in c: b[y,x]=max(cnt,key=cnt.get)
    a=b
basis=a.copy()
# stap C: zones (x0, y0, rijen); '?' = laten staan
Z={}
def blok(naam,x0,y0,rows):
    for j,r in enumerate(rows):
        for i,ch in enumerate(r):
            if ch!='?': Z.setdefault(naam,[]).append((x0+i,y0+j,L[ch]))
# opening: zilveren ring als schone ellips, yerba als twee lichte bladplekken op donkergroen (gemeten N=2 op het model)
blok('rand+yerba',23,24,[
 "?suusIIHHttts",          # y24 x23-35
 "sutsGIIHHHIIs",          # y25
 "sutsGGIGGGIIs",          # y26
 "?tuusGG",                # y27 x23-29
 "?stuuuuuuuuttttss"])     # y28 x23-39
# linkeroog: gat x18-22 y34-39 (model), groen met licht blad rechtsboven, lichte lip eronder
blok('oog_l',18,34,[
 "?###?","#####","##II#","#HIH#","#HHH#","?###?","?ddd?"])
# rechteroog: gat x28-34 y35-41, ovaal (gemeten randen 29/28/28/28/28/29/29 - 32/33/33/34/34/34/33), lip y42
blok('oog_r',28,35,[
 "??###??","?#####?","#GHHH#?","#GIIHH#","#GHIIH#","?#HHHH#","??####?","??ddd??"])
# neus: bol x20-27 y41-46; zwart alleen schaduwkant (rechts/onder), links een donkere tint, licht linksboven
blok('neus',19,40,[
 "?????????",
 "??cddcca#",
 "?adddccb#",
 "caddccbb#",
 "c#cccbbb#",
 "c#bbbbb#c",
 "?c#####cc"])           # y47: gat tussen neus en mond (model c, schaduw links b)
# mond: ronde D x19-29 y48-52 (model 47-52,9), holte a, lichte lip y53
MOND=sys.argv[3] if len(sys.argv)>3 else 'A'
if MOND=='A':   # rechte bovenlip
    blok('mond',18,47,[
     "bbccccccccc",
     "bb#########c",
     "?#aaaaaaaaa#",
     "?#aaaaaaaaa#",
     "??#aaaaaaa#",
     "???#######",
     "???bdddddc"])
else:           # mondhoeken 1 px omhoog zoals het model (y47), 2 px breed, geen losse punt
    blok('mond',18,47,[
     "b##ccccccc##",
     "b#a#######a#",
     "?#aaaaaaaaa#",
     "?#aaaaaaaaa#",
     "??#aaaaaaa#",
     "???#######",
     "???bdddddc"])
# rechterhand (want): bovenrand lichtkant donkerbruin, linkerrand rond (model x38-41)
blok('hand_r',38,42,[
 "??????aaa",               # y42 x44-46
 "???#aa",                  # y43 x41-43
 "??#",                     # y44 x40
 "c#",                      # y45 x38-39
 "?","?",
 "c"])                      # y48 x38
# rechtervoet: platte onderkant x36-40 op y62, staat zoals het model (x34-42, y58-62)
blok('voet_r',34,58,[
 "???bbbbb#",
 "#ccccccb#",
 "#cddccbb#",
 "?#dcccc#",
 "??#####"])
# losse vlakjes in het gezicht/de hand (check.py): lichte tint laten aansluiten
blok('rand+yerba',39,26,["t"])  # rechterring doorlopend lichtgrijs (zwart tussen ring en stroken weg)
blok('vlakjes',18,34,["d"]); blok('vlakjes2',41,44,["d"])
for n,ps in Z.items():
    for x,y,v in ps: a[y,x]=v
p=Image.fromarray(a.astype('uint8'),'P'); p.putpalette(PAL); p.save(sys.argv[2],transparency=0); np.save(sys.argv[2]+'.npy',a)
def zone_of(x,y):
    for n,ps in Z.items():
        xs=[q[0] for q in ps]; ys=[q[1] for q in ps]
        if min(xs)<=x<=max(xs) and min(ys)<=y<=max(ys): return n
    return 'lijf (toon/ruis)'
per={}
for y,x in zip(*np.where(a!=r3)): k=zone_of(x,y); per[k]=per.get(k,0)+1
print('afwijking t.o.v. r3 per zone:',per,'totaal',int((a!=r3).sum()))
print('kleuren',len(set(a.ravel()))-1)
