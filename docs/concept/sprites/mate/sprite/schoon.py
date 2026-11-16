# Technisch opschonen van de kale reductie. Elke stap logt hoeveel pixels hij verandert t.o.v. de kale reductie.
# Indexen: 1 zwart, 2 donkerbruin (lijn/selout/mondholte), 3-5 bruin donker/mid/licht, 6-8 groen, 9-11 zilver.
import sys, numpy as np; from PIL import Image
IN,OUT=sys.argv[1],sys.argv[2]
im=Image.open(IN); PAL=im.getpalette()[:36]; k0=np.asarray(im).astype(int); a=k0.copy()
log=[]
ZL={}
def stap(naam,b):
    global a
    n=(b!=a).sum(); log.append((naam,int(n)))
    for y,x in zip(*np.where(b!=a)): ZL.setdefault(zone_of(x,y),{}).setdefault(naam[:4],0); ZL[zone_of(x,y)][naam[:4]]+=1
    a=b
BR={2,3,4,5}; GR={6,7,8}; SI={9,10,11}
Z={ # zones (x0,y0,x1,y1) inclusief, canvascoördinaten
 'bombilla':(38,14,47,23),'rand':(22,22,41,30),'oog_l':(16,34,23,40),'oog_r':(27,34,35,41),
 'neus':(18,40,26,47),'mond':(16,46,31,54),'hand_l':(10,41,17,51),'hand_r':(38,39,50,51),
 'voet':(18,56,44,63),'hoorn_l':(17,21,23,30),'hoorn_r':(43,21,48,31)}
def inz(n,x,y): x0,y0,x1,y1=Z[n]; return x0<=x<=x1 and y0<=y<=y1
def zone_of(x,y):
    for n in Z:
        if inz(n,x,y): return n
    return 'lijf'
# 1. bruin-tinten: 'a' (2) alleen in de mondholte en als lijn; vlekken van tint 2 in het lijf -> 3 (donkerste lijftint)
b=a.copy(); H,W=a.shape
VLEK=len(sys.argv)>4 and sys.argv[4]=='vlek'   # variant B: grote a-vlekken (>=6 px) blijven als 4e bruintint
def cl2(a):
    seen=np.zeros(a.shape,bool); grote=set()
    for y in range(H):
        for x in range(W):
            if a[y,x]!=2 or seen[y,x]: continue
            st=[(y,x)]; seen[y,x]=True; c=[]
            while st:
                q=st.pop(); c.append(q)
                for dy,dx in ((1,0),(-1,0),(0,1),(0,-1)):
                    yy,xx=q[0]+dy,q[1]+dx
                    if 0<=yy<H and 0<=xx<W and not seen[yy,xx] and a[yy,xx]==2: seen[yy,xx]=True; st.append((yy,xx))
            if len(c)>=6: grote|=set(c)
    return grote
G2=cl2(a) if VLEK else set()
for y in range(H):
    for x in range(W):
        if a[y,x]==2 and not inz('mond',x,y) and (y,x) not in G2: b[y,x]=3
stap('vlek2->3',b)
# 2. silhouetrand: elke ondoorzichtige pixel naast transparant wordt omlijning; lichtkant (alleen boven/links open) = selout
op=a>0; b=a.copy()
for y in range(H):
    for x in range(W):
        if not op[y,x]: continue
        nb={(0,-1):op[y-1,x],(0,1):op[y+1,x],(-1,0):op[y,x-1],(1,0):op[y,x+1]}
        open_=[d for d,v in nb.items() if not v]
        if not open_: continue
        licht=all(d in ((0,-1),(-1,0)) for d in open_) and y<=46   # onderste derde = schaduwkant: zwart
        if a[y,x] in SI and not licht and set(open_)&{(0,-1),(-1,0)}: licht=False
        if a[y,x]==1: 
            if licht: b[y,x]=9 if a[y,x] in SI else 2
            continue
        if licht: b[y,x]=9 if a[y,x] in SI else 2
        else: b[y,x]=1
stap('buitenlijn',b)
# 3. ruis: clusters (4-samenhangend) van <= KLEIN px van een bruintint -> meest voorkomende bruinbuur
KLEIN=int(sys.argv[3]) if len(sys.argv)>3 else 2
def clusters(a,v):
    seen=np.zeros(a.shape,bool); out=[]
    for y in range(H):
        for x in range(W):
            if a[y,x]!=v or seen[y,x]: continue
            st=[(y,x)]; seen[y,x]=True; c=[]
            while st:
                q=st.pop(); c.append(q)
                for dy,dx in ((1,0),(-1,0),(0,1),(0,-1)):
                    yy,xx=q[0]+dy,q[1]+dx
                    if 0<=yy<H and 0<=xx<W and not seen[yy,xx] and a[yy,xx]==v: seen[yy,xx]=True; st.append((yy,xx))
            out.append(c)
    return out
for rnd in range(3):
    b=a.copy()
    for v in (3,4,5):
        for c in clusters(a,v):
            if len(c)>KLEIN: continue
            if any(inz('mond',x,y) or inz('neus',x,y) for y,x in c): continue
            cnt={}
            for y,x in c:
                for dy,dx in ((1,0),(-1,0),(0,1),(0,-1)):
                    yy,xx=y+dy,x+dx
                    if 0<=yy<H and 0<=xx<W and a[yy,xx] in (3,4,5) and a[yy,xx]!=v: cnt[a[yy,xx]]=cnt.get(a[yy,xx],0)+1
            if cnt:
                nv=max(cnt,key=cnt.get)
                for y,x in c: b[y,x]=nv
    stap('ruis%d'%rnd,b)
# 4. reparaties per pixel naar het model (x, y, index, reden); letters: # a b c d G H I s t u
L={'.':0,'#':1,'a':2,'b':3,'c':4,'d':5,'G':6,'H':7,'I':8,'s':9,'t':10,'u':11}
REP=[
 # bombilla: lichtkant (boven/links) selout donkergrijs, midden licht, schaduwkant zwart; klem = donkergrijs (model r18-19)
 (44,15,'s','mondstuk bovenrand donkergrijs (model)'),(45,15,'s','mondstuk bovenrand'),
 (42,16,'s','lichtkant selout'),(43,16,'s','buitenrand mondstuk: geen licht op de rand'),(44,16,'u','glans mondstuk'),
 (41,17,'s','lichtkant selout'),(42,17,'u','glans'),(43,17,'#','onderrand mondstuk zwart (model)'),(44,17,'#','onderrand mondstuk'),
 (40,18,'s','lichtkant'),(41,18,'s','klem (model donkere ring)'),(43,18,'#','schaduwkant'),
 (39,19,'s','lichtkant'),(40,19,'s','klem'),(41,19,'t','buis'),(42,19,'#','schaduwkant'),(43,19,0,'los zwart buiten de buis (model wit)'),
 (40,20,'t','buis'),
 (37,21,'s','lichtkant selout (model donkergrijs op 37,5)'),(38,21,'u','glans buis'),(39,21,'t','buis'),
 (38,22,'u','glans buis'),(40,22,0,'model wit naast buis'),
 (37,23,'u','glans buis'),(38,23,'t','buis'),
 (36,24,'u','glans buis in de rand'),(37,24,'t','buis'),
 # rand
 (25,25,'t','modelrand lichtgrijs, geen zwart'),(23,26,'s','linkerrand kalebasrand ontbrak (bruin)'),(26,26,'G','bruin binnen de rand -> donker groen (model)'),
 (23,27,'s','linkerrand'),(24,28,'s','linkerrand onder'),
 (26,29,'t','onderband grijs (model)'),(27,29,'t','onderband'),(28,29,'t','onderband'),(29,29,'t','onderband'),
 (26,30,'#','onderlijn rand (model zwart)'),(27,30,'#','onderlijn'),(28,30,'#','onderlijn'),(37,30,'#','onderlijn'),(38,30,'#','onderlijn'),
 # hoorns
 (17,26,'a','selout doorlopend (geen zwart/bruin om en om)'),(18,29,'a','selout'),(20,29,'c','model donkerbruin, geen zwart (als c: geen losse pixel)'),
 (45,23,'a','hoornpunt rechts: was bruin op de rand'),
 # oog rechts
 (27,37,'c','model bruin, geen zwart'),(27,38,'c','model bruin'),
 # neus
 (27,44,'c','model 31% zwart: lijn loopt diagonaal 27,43-26,44-25,45'),(26,43,'b','schaduwboog neus (model a/b)'),(25,43,'b','schaduwboog'),(25,44,'b','schaduw neus'),
 (21,45,'b','binnenschaduw neus'),(24,45,'b','binnenschaduw'),(24,46,'#','onderlijn neus (haak)'),
 (25,42,'c','model c'),(26,42,'b','schaduwboog doorlopend'),(27,42,'c','model c'),
 (19,40,'d','onderlip linkeroog (dambord weg)'),(21,40,'c','dambord weg'),(22,40,'c','dambord weg'),
 (22,45,'b','dambord in de neusschaduw weg'),
 (22,30,'c','kam onder de rand weg'),(24,30,'c','kam onder de rand weg'),
 # ooggaten: groen waar het model groen heeft (meerderheid), onderrand donkerbruin + lichte lip zoals het model
 (21,37,'H','groen (model I, 21% zwart)'),(20,39,'a','donkere onderrand gat (model a)'),
 (33,40,'H','groen (model)'),(34,40,'c','model c, geen zwart (24%)'),(31,41,'a','onderrand gat (model a)'),(32,41,'a','onderrand gat'),(33,41,'d','lip (model d)'),
 (30,42,'d','lip onder het oog (model d)'),(31,42,'d','lip'),(32,42,'d','lip'),
 # mond
 (23,52,'#','onderlijn mond (model zwart)'),(25,52,'#','onderlijn'),(26,52,'#','onderlijn'),(27,52,'#','onderlijn'),
]
b=a.copy(); PER={}
for x,y,v,r in REP:
    v=L[v] if isinstance(v,str) else v
    if b[y,x]!=v: b[y,x]=v; PER[zone_of(x,y)]=PER.get(zone_of(x,y),0)+1
stap('reparaties',b); print('reparaties per zone',PER)
np.save(OUT+'.npy',a)
p=Image.fromarray(a.astype('uint8'),'P'); p.putpalette(PAL+[0]*(768-len(PAL))); p.save(OUT,transparency=0)
d=(a!=k0); per={}
for y,x in zip(*np.where(d)): per[zone_of(x,y)]=per.get(zone_of(x,y),0)+1
print(log); print('per zone per stap',ZL); print('afwijking per zone',per,'totaal',int(d.sum()),'kleuren',len(set(a.ravel()))-1)
