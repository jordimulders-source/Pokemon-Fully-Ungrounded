# Capykart r1: kale reductie (kaal_lab.npy) -> per zone paletmapping (fur/hout/hoepel/blokken) -> ruis -> gezicht
# uit capybarrel/af (pixelkopie) + toegestane toevoegingen -> buitenlijn. Elke afwijking van de gemapte kale reductie wordt gelogd.
import numpy as np, sys, json
from collections import Counter
from PIL import Image
R='/home/user/Pokemon-Fully-Ungrounded/docs/concept/sprites/capykart/sprite/'
CB='/home/user/Pokemon-Fully-Ungrounded/docs/concept/sprites/capybarrel/af/capybarrel.png'
VAR=sys.argv[1] if len(sys.argv)>1 else 'A'
FUR={'A':[(238,212,170),(208,174,130),(166,128,94)],   # beige (Jordi's idee)
     'B':[(216,158,116),(180,122,88),(140,90,66)]}[VAR]  # dieper/warmer (voorstel Claude)
PAL={'.':(0,0,0),'0':(32,20,28),'s':(130,62,54),
     'C':FUR[0],'A':FUR[1],'F':FUR[2],
     'B':(246,170,102),'7':(214,128,76),                      # hout = Capybarrel ton (donker/nerf = s)
     '9':(132,126,132),'3':(86,84,98),'W':(255,255,255),      # grijs = Capybarrel neus/hoepels
     'b':(100,156,232),'u':(64,104,184),'r':(240,92,84),'y':(248,212,72),'g':(88,172,80)}
ORDER=list(PAL)
L=np.load(R+'kaal_lab.npy'); H,W=L.shape
# ---- zones ----
LINE={0,1,2,3}; DARK={4,5}; HOOP={6,13,25}
BLUE={21}; RED={7,18,24}; YEL={27,12}; GREEN={14}
def inblock(x,y): return x>=41 and y<=31 and not (y>=29 and x<=45)
fur=np.zeros((H,W),bool); st=[(30,15)]
while st:
    x,y=st.pop()
    if not(0<=x<W and 0<=y<H) or fur[y,x] or L[y,x] in LINE|HOOP|{-1}: continue
    if x>45 or inblock(x,y): continue
    if y in(31,32) and x<=28: continue          # hoodschaduw onder de kin = hout (model)
    if y>=33 and x<=29+(y-33)//2: continue     # links van de nek-diagonaal (model: zwarte lijn)
    if y>=38 and x>=40: continue                # onder de nek-onderlijn
    if y>=40: continue
    fur[y,x]=1; st+=[(x+1,y),(x-1,y),(x,y+1),(x,y-1)]
# blokken: per spritecel meerderheid over modelpixels, geclassificeerd op referentiekleuren gemeten in het model
M=np.asarray(Image.open(R+'../referenties/model_r5.png').convert('RGB')).astype(float)
REF=[('y',(241,207,84)),('ys',(195,132,86)),('r',(244,99,92)),('rs',(205,61,66)),('b',(107,158,214)),('bs',(76,109,168)),
     ('g',(90,163,89)),('gs',(74,135,82)),('gh',(130,200,120)),('ey',(174,139,42)),('er',(153,39,48)),('k',(25,18,27)),
     ('h',(103,101,107)),('w',(160,92,58)),('W',(255,255,255))]
BMAP=json.load(open(R+'blokmap.json'))[sys.argv[3] if len(sys.argv)>3 else 'std']
RC=np.array([c for _,c in REF]); x0,y0,p=133,860-62*12.064516129032258,12.064516129032258
BLK=[[None]*W for _ in range(H)]
for y in range(H):
    for x in range(W):
        if L[y,x]<0 or not inblock(x,y) or (L[y,x] in HOOP and y>=24): continue
        blk=M[int(round(y0+y*p)):int(round(y0+(y+1)*p)),int(round(x0+x*p)):int(round(x0+(x+1)*p))].reshape(-1,3)
        lab=((blk[:,None,:]-RC[None])**2).sum(2).argmin(1)
        cnt=np.bincount(lab,minlength=len(REF)); cnt[-1]=0
        BLK[y][x]=BMAP[REF[cnt.argmax()][0]]
FT={26:'C',22:'C',23:'A',20:'A',19:'A',16:'F',15:'F',11:'F',8:'F',9:'F',10:'F',17:'F'}
WT={26:'B',23:'B',22:'B',20:'7',19:'7',16:'7',15:'7',11:'7',10:'s',8:'s',9:'s',17:'s'}
g=[['.']*W for _ in range(H)]
for y in range(H):
    for x in range(W):
        v=L[y,x]
        if v<0: continue
        if v in LINE: c='0'
        elif BLK[y][x] is not None: c=BLK[y][x]
        elif v in HOOP: c={25:'9',13:'9',6:'3'}[v]
        elif v in DARK and fur[y,x]: c='s'
        elif v in DARK: c='s'
        elif fur[y,x]: c=FT.get(v,'A')
        else: c=WT.get(v,'7')
        g[y][x]=c
kaal=[r[:] for r in g]
log=[]
def put(zone,x,y,c,why):
    old=g[y][x]
    if old!=c: g[y][x]=c; log.append((zone,x,y,old,c,why))
extra=json.load(open(R+'extra.json')) if len(sys.argv)>2 else []
for zone,x,y,c,why in extra: put(zone,x,y,c,why)
# ---- ruis: tintvlakjes <3 px -> meest voorkomende buurtint uit dezelfde kleurgroep ----
GROUPS=['CAF','B7','93','bu','r','y','g']
def comps():
    seen=set(); res=[]
    for y in range(H):
        for x in range(W):
            if (x,y) in seen or g[y][x] in '.0sW': continue
            v=g[y][x]; st=[(x,y)]; seen.add((x,y)); c=[]
            while st:
                cx,cy=st.pop(); c.append((cx,cy))
                for dx,dy in((1,0),(-1,0),(0,1),(0,-1)):
                    nx,ny=cx+dx,cy+dy
                    if 0<=nx<W and 0<=ny<H and (nx,ny) not in seen and g[ny][nx]==v: seen.add((nx,ny)); st.append((nx,ny))
            res.append((v,c))
    return res
PROT=set()
def ruis(zone):
  for _ in range(3):
    for v,c in comps():
        if len(c)>=3 or any(p in PROT for p in c): continue
        grp=[G for G in GROUPS if v in G][0]
        nb=Counter(g[y+dy][x+dx] for x,y in c for dx,dy in((1,0),(-1,0),(0,1),(0,-1))
                   if 0<=x+dx<W and 0<=y+dy<H and g[y+dy][x+dx] in grp and g[y+dy][x+dx]!=v)
        if nb:
            for x,y in c: put(zone,x,y,nb.most_common(1)[0][0],'tintvlakje <3 px naar buurtint')
ruis('ruis')
# ---- gezicht: pixelkopie uit capybarrel/af (neus+tanden, oog) ----
cb=np.array(Image.open(CB))
CBMAP={1:'0',2:'s',3:'C',4:'A',5:'F',6:'9',7:'3',8:'0',13:'W'}
FACE=json.load(open(R+'gezicht.json'))
for y in range(17,22):
    for x in range(27,32):
        if fur[y,x] and g[y][x] in '09s': put('oog',x,y,'A','modeloog weg (wordt Capybarrel-oog)')
for naam,(sx0,sy0,sx1,sy1,dx,dy,keep) in FACE.items():
    for y in range(sy0,sy1+1):
        for x in range(sx0,sx1+1):
            v=int(cb[y,x])
            if v not in keep: continue
            put(naam,x+dx,y+dy,CBMAP[v],'pixelkopie Capybarrel (%d,%d)'%(x,y))
TL=int(sys.argv[4]) if len(sys.argv)>4 else 1   # tanden langer (px)
for k in range(1,TL+1):
    for x in range(11,16):
        v=int(cb[45,x])
        if v in (1,6,13): put('tanden',x+5,45-14+k,CBMAP[v],'tand %d px doorgetrokken (Capybarrel rij 45)'%k)
for x in range(12,16): put('tanden',x+5,46-14+TL,'0','onderlijn tanden (Capybarrel rij 46) %d px lager'%TL)
for zone,x,y,c,why in json.load(open(R+'toevoeging.json')): put(zone,x,y,c,why)
PROT|={(x,y) for z,x,y,*_ in log if z in('neus','tanden','oog','morrillo','wenkbrauw')}
GROUPS[:]=['CAF','B7','93','bu','r','y','g']
ruis('ruis2')
for v,c in comps():
    if v=='7' and len(c)==1 and c[0] not in PROT:
        put('ruis2',c[0][0],c[0][1],'s','losse houtpixel zonder houtbuur naar donkerste houttint')
# ---- buitenlijn ----
def opaque(x,y): return 0<=x<W and 0<=y<H and g[y][x]!='.'
for y in range(H):
    for x in range(W):
        if g[y][x] in '.W': continue
        if any(not opaque(x+dx,y+dy) for dx,dy in ((1,0),(-1,0),(0,1),(0,-1))) and g[y][x] not in '0s':
            put('lijn',x,y,'0','buitenlijn dicht')
for y in range(H):
    for x in range(W):
        if g[y][x]!='0': continue
        ups=[(dx,dy) for dx,dy in ((0,-1),(-1,0)) if not opaque(x+dx,y+dy)]
        if not ups: continue
        dx,dy=ups[0]; ix,iy=x-dx,y-dy
        if opaque(ix,iy) and g[iy][ix] in 'CAB7':
            put('lijn',x,y,'s','selout lichtkant')
for y in range(H):
    for x in range(W):
        if g[y][x]=='s' and not opaque(x,y+1): put('lijn',x,y,'0','onderrand zwart')
        if g[y][x]=='s' and not opaque(x+1,y) : put('lijn',x,y,'0','rechterrand zwart')
# ---- naar 64x64 ----
OX=(64-W)//2; OY=62-H
img=np.zeros((64,64),'uint8')
for y in range(H):
    for x in range(W): img[OY+y,OX+x]=ORDER.index(g[y][x])
pal=[]
for k in ORDER: pal+=PAL[k]
pal+=[0,0,0]*(256-len(ORDER))
im=Image.fromarray(img,'P'); im.putpalette(pal)
out=R+f'r1/capykart_{VAR}.png'; im.save(out,transparency=0)
Image.open(out).convert('RGBA').resize((512,512),Image.NEAREST).save(R+f'r1/capykart_{VAR}_8x.png')
json.dump({'OX':OX,'OY':OY,'grid':[''.join(r) for r in g],'kaal':[''.join(r) for r in kaal]},open(R+f'r1/grid_{VAR}.json','w'))
cnt=Counter(z for z,*_ in log)
print(VAR,'afwijkingen per zone:',dict(cnt),'totaal',len(log),'van',sum(c!='.' for r in g for c in r),'px; kleuren',len(set(c for r in g for c in r))+0)
with open(R+f'r1/log_{VAR}.txt','w') as f:
    for e in log: f.write('%s (%d,%d) %s->%s  %s\n'%e)
