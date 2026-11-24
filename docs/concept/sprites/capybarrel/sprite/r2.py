# Ronde 2: bouwt verder op r1 (grid_X.json). Silhouet bevroren (alpha-diff 0 met r1).
import json, sys, numpy as np
from PIL import Image
from collections import Counter
R='/home/user/Pokemon-Fully-Ungrounded/docs/concept/sprites/capybarrel/'
PAL={'.':(0,0,0),'0':(32,20,28),'s':(104,52,40),'C':(226,146,112),'A':(196,114,90),'5':(150,82,70),
     '9':(132,126,132),'3':(90,78,84),'n':(56,44,52),'B':(222,140,72),'7':(182,98,48),'4':(142,68,36),
     'D':(208,208,216),'W':(255,255,255),'h':(66,66,78)}
ORDER=list(PAL)
var=sys.argv[1]
d=json.load(open(R+f'sprite/r1/grid_{var}.json'))
g=[list(r) for r in d['grid']]; r1=[r[:] for r in g]; kaal=d['kaal']
H,Wd=len(g),len(g[0]); log=[]
def put(z,x,y,c,why):
    if g[y][x]!=c: log.append((z,x,y,g[y][x],c,why)); g[y][x]=c
op=lambda x,y: 0<=x<Wd and 0<=y<H and g[y][x]!='.'
# ---- 3a. hoepels: kern exact op de gemeten modelpixels (donker/licht grijs), schaduwkant (rechts) zwart ----
HOEP={6:[(23,'h'),(24,'h'),(33,'h')],7:[(24,'9'),(25,'9'),(33,'h'),(34,'h')],8:[(24,'h'),(25,'9'),(34,'h'),(35,'h')],
      9:[(25,'9'),(26,'9'),(34,'9'),(35,'9')],10:[(25,'9'),(26,'9'),(34,'h'),(35,'9')],11:[(25,'9'),(26,'9'),(35,'h'),(36,'h')]}
for y in range(12,18): HOEP[y]=[(26,'h'),(27,'h'),(35,'h'),(36,'h')]
for y in (18,19): HOEP[y]=[(25,'h'),(26,'h'),(35,'h'),(36,'h')]
HOEP[20]=[(25,'h'),(26,'h'),(35,'h')]; HOEP[21]=[(25,'h'),(26,'h'),(34,'h'),(35,'h')]
HOEP[22]=[(24,'h'),(25,'h'),(34,'h')]; HOEP[23]=[(34,'h')]; HOEP[24]=[(33,'h'),(34,'h')]
HOEP[25]=[(32,'h'),(33,'h')]; HOEP[26]=[(31,'h'),(32,'h')]
hoep=set()
for y,lst in HOEP.items():
    for x,c in lst: put('hoepel',x,y,c,'hoepelkern gemeten op model'); hoep.add((x,y))
for y,lst in HOEP.items():
    xs=sorted(x for x,_ in lst)
    for run_end in [x for x in xs if (x+1,y) not in hoep]:
        if op(run_end+1,y) and g[y][run_end+1] in 'B74s39': put('hoepel',run_end+1,y,'0','zwarte rand schaduwkant hoepel (model)')
# oude hoepelgrijs/zwart dat niet meer bij een hoepel hoort -> hout uit de buurt
for y in range(5,28):
    for x in range(19,40):
        if (x,y) in hoep: continue
        if g[y][x] in '39':
            nb=Counter(g[y+dy][x+dx] for dx,dy in((1,0),(-1,0),(0,1),(0,-1)) if op(x+dx,y+dy) and g[y+dy][x+dx] in 'B74')
            put('hoepel',x,y,nb.most_common(1)[0][0] if nb else '0','oud hoepelgrijs buiten gemeten hoepel')
# ---- 3b. duiglijnen op gemeten donkere modelpixels ----
L=np.load(R+'sprite/r2/lijnfrac.npy')
for y in range(5,28):
    for x in range(19,40):
        if g[y][x] not in 'B74' : continue
        f=L[y,x]; pair=max(L[y-1,x] if y>0 else 0, L[y+1,x] if y+1<H else 0)
        if f>=0.45 or (f>=0.2 and f+pair>=0.55 and f>=pair):
            put('duig',x,y,'s','duiglijn: modelaandeel donkerbruin %.2f'%f)
# ---- 2. verre oor: binnenkant donker zoals het nabije oor ----
put('oor',11,2,'s','oorbinnenkant donker (model donker, zoals nabije oor)'); put('oor',12,2,'s','idem')
# ---- 4. volume achterlijf: ronde dij, hooglicht op de bolling linksboven, sikkel rechtsonder ----
for y in range(13,25):
    for x in range(37,45):
        if g[y][x] not in 'CA5': continue
        e=((x-40.3)/3.0)**2+((y-18.5)/5.2)**2
        t='C' if ((x-39.3)/1.4)**2+((y-16.0)/1.8)**2<=1 else ('A' if e<=1 else '5')
        if y<=14 and g[y][x]=='C': continue   # rug-hooglicht laten staan
        put('volume',x,y,t,'Gen 3-volume dij')
for (x,y) in [(39,26),(39,27),(39,28),(40,26)]:
    if g[y][x]=='5': put('volume',x,y,'A','lichtkant onderpoot achter')
# verre voorpoot: schaduwtint, alleen klein middentint-hooglicht op de bolling linksboven
for (x,y) in [(13,25),(14,25),(13,26)]:
    if g[y][x]=='5': put('volume',x,y,'A','bolling verre voorpoot')
# ---- reparaties na meting: losse restjes en 1-2 px vlakjes ----
for (x,y,c,w) in [(25,12,'B','los hoepelzwart buiten gemeten hoepel'),(24,9,'B','idem'),(24,7,'h','hoepeleinde doorlopend (3+ px)'),
                  (34,10,'9','hoepel 2: lichte band doorlopend'),(1,9,'9','neus-hooglicht aaneen'),(14,24,'A','bolling verre voorpoot aaneen'),
                  (42,14,'A','dij-volume aaneen'),(23,11,'B','los duigstipje terug (lijn te zwak gemeten)'),(30,11,'B','idem'),
                  (28,7,'s','duiglijn rij 7 doorlopend (model 0.33)'),(22,13,'4','geen dubbele rand naast buitenlijn'),(22,14,'4','idem'),(22,15,'4','idem'),(22,16,'4','idem'),(43,14,'5','sikkel rand dij doorlopend'),(37,9,'s','2px houtrest aan tonrand'),(37,10,'s','idem')]:
    put('fix',x,y,c,w)
def comps(sym):
    seen=set(); res=[]
    for y in range(H):
        for x in range(Wd):
            if (x,y) in seen or g[y][x] not in sym: continue
            v=g[y][x]; st=[(x,y)]; seen.add((x,y)); c=[]
            while st:
                cx,cy=st.pop(); c.append((cx,cy))
                for dx,dy in((1,0),(-1,0),(0,1),(0,-1)):
                    nx,ny=cx+dx,cy+dy
                    if op(nx,ny) and (nx,ny) not in seen and g[ny][nx]==v: seen.add((nx,ny)); st.append((nx,ny))
            res.append((v,c))
    return res
for v,c in comps('B74'):
    if len(c)<3:
        same=[1 for x,y in c for dx,dy in((1,0),(-1,0),(0,1),(0,-1)) if op(x+dx,y+dy) and g[y+dy][x+dx] in 'B74' and g[y+dy][x+dx]!=v]
        nb=Counter(g[y+dy][x+dx] for x,y in c for dx,dy in((1,0),(-1,0),(0,1),(0,-1)) if op(x+dx,y+dy) and g[y+dy][x+dx] in 'B74' and g[y+dy][x+dx]!=v)
        for x,y in c: put('fix',x,y,nb.most_common(1)[0][0] if nb else 's','houtvlakje <3 px')
# ---- 1. buitenlijn: lichtkant (lege buur boven/links) selout, onderkant/rechts zwart ----
def edge(x,y): return [(dx,dy) for dx,dy in((1,0),(-1,0),(0,1),(0,-1)) if not op(x+dx,y+dy)]
for y in range(H):
    for x in range(Wd):
        if g[y][x] not in '0sn': continue
        e=edge(x,y)
        if not e: continue
        if (0,1) in e: c='0'
        elif (0,-1) in e or (-1,0) in e: c='s'
        else: c='0'
        if c=='s' and x<=8 and 7<=y<=18: c='n'   # neus: grijze selout
        put('lijn',x,y,c,'selout lichtkant / zwart schaduwkant')
# om-en-om opruimen langs de rand
for _ in range(2):
    for y in range(H):
        for x in range(Wd):
            if g[y][x] not in '0sn' or not edge(x,y): continue
            nb=[g[y+dy][x+dx] for dx in(-1,0,1) for dy in(-1,0,1) if (dx or dy) and op(x+dx,y+dy) and g[y+dy][x+dx] in '0sn' and edge(x+dx,y+dy)]
            if len(nb)>=2 and all(c!=g[y][x] for c in nb) and len(set(nb))==1:
                put('lijn',x,y,nb[0],'om-en-om weg')
# ---- uitvoer ----
assert all((g[y][x]=='.')==(r1[y][x]=='.') for y in range(H) for x in range(Wd)), 'silhouet gewijzigd'
OX,OY=d['OX'],d['OY']
img=np.zeros((64,64),'uint8')
for y in range(H):
    for x in range(Wd): img[OY+y,OX+x]=ORDER.index(g[y][x])
pal=sum((list(PAL[k]) for k in ORDER),[])+[0]*3*(256-len(ORDER))
im=Image.fromarray(img,'P'); im.putpalette(pal); im.save(R+f'sprite/r2/capybarrel_{var}.png',transparency=0)
json.dump({'OX':OX,'OY':OY,'grid':[''.join(r) for r in g],'kaal':kaal},open(R+f'sprite/r2/grid_{var}.json','w'))
km={'.':'.'}
dz=Counter(z for z,*_ in log)
vsk=sum(1 for y in range(H) for x in range(Wd) if g[y][x]!=kaal[y][x])
print(var,'t.o.v. r1 per zone',dict(dz),'| totaal t.o.v. kale reductie',vsk,'van',sum(c!='.' for r in g for c in r))
open(R+f'sprite/r2/log_{var}.txt','w').write(''.join('%s (%d,%d) %s->%s  %s\n'%e for e in log))
