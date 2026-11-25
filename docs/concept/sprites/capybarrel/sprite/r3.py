# Ronde 3: één basis (uit r2 A) + oogvarianten 1-3. Alle reparaties naar het model (metingen in r2/*.npy en hieronder).
import json, sys, numpy as np
from PIL import Image
from collections import Counter
R='/home/user/Pokemon-Fully-Ungrounded/docs/concept/sprites/capybarrel/'
PAL={'.':(0,0,0),'0':(32,20,28),'s':(104,52,40),'C':(226,146,112),'A':(196,114,90),'5':(150,82,70),
     '9':(132,126,132),'3':(90,78,84),'n':(56,44,52),'B':(222,140,72),'7':(182,98,48),'4':(142,68,36),
     'D':(208,208,216),'W':(255,255,255),'h':(86,86,98)}
ORDER=list(PAL)
var=sys.argv[1]
d=json.load(open(R+'sprite/r2/grid_A.json'))
g=[list(r) for r in d['grid']]; r2=[r[:] for r in g]; kaal=d['kaal']
H,Wd=len(g),len(g[0]); log=[]
def put(z,x,y,c,why):
    if g[y][x]!=c: log.append((z,x,y,g[y][x],c,why)); g[y][x]=c
op=lambda x,y: 0<=x<Wd and 0<=y<H and g[y][x]!='.'
def edge(x,y): return [(dx,dy) for dx,dy in((1,0),(-1,0),(0,1),(0,-1)) if not op(x+dx,y+dy)]
M=np.load(R+'sprite/r2/furlum.npy')
# ---- 7. kopvolume: bolling (licht voorhoofd + boven het oog), middentint wang, donker waar het model donker is ----
for y in range(2,18):
    for x in range(3,22):
        c=g[y][x]
        ineye = 11<=x<=18 and 6<=y<=11 and c in 'CA5sW0'
        if c not in 'CA5' and not ineye: continue
        if ineye and c in '0s' and not (12<=x<=18 and 7<=y<=10): continue
        if (x,y) in [(18,3),(19,3),(18,4),(19,4),(19,2),(11,1),(11,2),(12,2)]: continue   # oorschaduw
        m=M[y,x] if not (12<=x<=17 and 7<=y<=10) else np.nan   # modeloog zelf telt niet mee
        if not np.isnan(m) and m<115: t='5'
        elif ((x-10.0)/5.6)**2+((y-5.6)/2.9)**2<=1: t='C'
        else: t='A'
        put('kop',x,y,t,'kopvolume: bolling (model-lum %s)'%('-' if np.isnan(m) else int(m)))
# ---- oog (Gen 3-bron 1-op-1, omgekleurd; '-' = huid van de bron, vacht blijft) ----
EYES={'1':('sealeo (x21-22,y14-17): 5 zwart->0, donkere lid 1->s, schaduw 3->5, witte glans (linksboven) -> zwart',['5s','00','00','55'],(14,7)),
      '2':('igglybuff (x24-27,y28-31): 15 zwart->0, donkerrode rand 13->s, huidschaduw 4->5, witte glans (linksboven) -> zwart',['-ss-','s005','s005','-ss-'],(13,7)),
      '3':('flareon (x15-18,y27-30): 10 zwart->0, donkere rand 15->s, witte glans (boven) -> zwart',['-ss-','s000','ss00','s-00'],(13,7))}
naam,blk,(ax,ay)=EYES[var]
for j,row in enumerate(blk):
    for i,c in enumerate(row):
        if c!='-': put('oog',ax+i,ay+j,c,'oog uit '+naam)
# ---- 1. tanden (model: twee witte tanden rij 18-19 onder de neus, lichtgrijze scheiding, zwart eronder) ----
for (x,y,c) in [(3,17,'0'),(4,17,'0'),(2,18,'0'),(3,18,'W'),(4,18,'D'),(5,18,'W'),(6,18,'0'),
                (2,19,'0'),(3,19,'W'),(4,19,'D'),(5,19,'D'),(3,20,'0'),(4,20,'0'),(5,20,'0')]:
    put('tanden',x,y,c,'tanden naar model')
# ---- 2. oren + deuk (model, spritecelraster) ----
for (x,y,c) in [(10,0,'s'),(11,0,'s'),(10,1,'s'),(11,1,'5'),(12,1,'0'),(10,2,'s'),(11,2,'5'),(12,2,'5'),
                (16,2,'.'),(16,3,'s'),
                (18,0,'s'),(19,0,'s'),(17,1,'s'),(18,1,'C'),(19,1,'A'),(20,1,'0'),(17,2,'s'),(18,2,'A'),(19,2,'5'),(20,2,'0')]:
    put('oren',x,y,c,'oorvorm/binnenoor/deuk naar model')
# ---- 3. hoepels: 2 px kern op de gemeten modelhoepel (subpixel-midden), zwart aan beide kanten zoals het model ----
H1={6:23,7:24,8:24,9:25,10:25,11:25,12:26,13:26,14:26,15:26,16:26,17:26,18:25,19:25,20:25,21:25,22:24}
H2={6:33,7:33,8:34,9:34,10:34,11:35,12:35,13:35,14:35,15:35,16:35,17:35,18:35,19:35,20:34,21:34,22:34,23:33,24:33,25:32}
LICHT={1:range(6,12),2:range(8,11)}
newh=set()
for k,HH in ((1,H1),(2,H2)):
    for y,c0 in HH.items():
        for x in (c0,c0+1): newh.add((x,y))
# oude hoepelpixels die niet in de nieuwe hoepel vallen -> hout uit de rij
for y in range(6,27):
    for x in range(22,38):
        if (x,y) in newh: continue
        if g[y][x] in 'h9':
            nb=Counter(g[y][xx] for xx in range(x-3,x+4) if 0<=xx<Wd and g[y][xx] in 'B74')
            put('hoepel',x,y,nb.most_common(1)[0][0] if nb else '4','oude hoepelpixel buiten modelhoepel')
for k,HH in ((1,H1),(2,H2)):
    for y,c0 in HH.items():
        put('hoepel',c0,y,'9' if y in LICHT[k] else 'h','hoepelkern (model)')
        put('hoepel',c0+1,y,'9' if y in LICHT[k] else 'h','hoepelkern (model)')
        for xb in (c0-1,c0+2):
            if op(xb,y) and g[y][xb] in 'B74hs9': put('hoepel',xb,y,'0','hoepelrand zwart (model)')
# losse zwarte restjes van de oude hoepelranden: zwart in de ton dat niet tegen een hoepel/rand ligt -> hout
def nearh(x,y): return any((x+dx,y+dy) in newh for dx in(-1,0,1) for dy in(-1,0,1))
for y in range(6,26):
    for x in range(23,37):
        if g[y][x]=='0' and not nearh(x,y):
            nbs=[g[y+dy][x+dx] for dx,dy in((1,0),(-1,0),(0,1),(0,-1)) if op(x+dx,y+dy)]
            if all(c in 'B74s' for c in nbs):
                nb=Counter(c for c in nbs if c in 'B74')
                put('hoepel',x,y,nb.most_common(1)[0][0] if nb else '4','los oud hoepelzwart')
# ---- 4. planklijnen op de gemeten rijen per segment, in 4 (op licht hout) of s (op donker hout) ----
for y in range(6,27):
    for x in range(21,39):
        if g[y][x]=='s' and kaal[y][x] not in '012' and not nearh(x,y): pass
LIJN={'L':[11,20],'M':[7,11,17,22,25],'R':[8,12,17,21]}
for y in range(5,28):
    for x in range(20,40):
        c=g[y][x]
        if c not in 'B74s': continue
        seg='L' if y in H1 and x<H1[y]-1 else ('R' if y in H2 and x>H2[y]+2 else ('M' if y in H1 and y in H2 and H1[y]+2<x<H2[y]-1 else None))
        if seg is None: continue
        if y in LIJN[seg]:
            put('plank',x,y,'4' if y<=12 else 's','planklijn op gemeten modelrij %d (%s)'%(y,seg))
        elif c=='s' and r2[y][x]=='s' and not edge(x,y) and not any(op(x+dx,y+dy) and g[y+dy][x+dx] in 'CA5' for dx,dy in((1,0),(-1,0),(0,1),(0,-1))):
            nb=Counter(g[y][xx] for xx in range(x-2,x+3) if 0<=xx<Wd and g[y][xx] in 'B74')
            put('plank',x,y,nb.most_common(1)[0][0] if nb else '4','oude lijn niet op gemeten modelrij')
# ---- 8. staartbultje (model): deuk links, rond bovenhoekje rechts ----
for (x,y,c) in [(41,10,'0'),(41,11,'s'),(42,10,'s'),(43,10,'s'),(44,10,'.'),(44,11,'0'),(45,11,'.'),
                (42,11,'C'),(43,11,'C'),(42,12,'A'),(43,12,'5'),(44,12,'5'),(45,12,'0')]:
    put('staart',x,y,c,'staartbultje naar model')
# ---- restjes: oor/staart-tinten aaneen, houtvlakjes <3 px ----
for (x,y,c,w) in [(18,1,'A','oorvulling aaneen (model licht)'),(17,3,'5','binnenoor aaneen'),(17,4,'5','binnenoor aaneen (los lijnpixel weg)'),(42,11,'C','bultje licht aaneen'),(43,11,'C','idem'),(42,12,'C','idem'),
                  (23,17,'7','geen planklijn op deze rij in het model (links)'),(24,17,'7','idem')]:
    put('fix',x,y,c,w)
def comps(sym):
    seen=set(); res=[]
    for y in range(H):
        for x in range(Wd):
            if (x,y) in seen or g[y][x] not in sym: continue
            v=g[y][x]; st=[(x,y)]; seen.add((x,y)); cc=[]
            while st:
                cx,cy=st.pop(); cc.append((cx,cy))
                for dx,dy in((1,0),(-1,0),(0,1),(0,-1)):
                    nx,ny=cx+dx,cy+dy
                    if op(nx,ny) and (nx,ny) not in seen and g[ny][nx]==v: seen.add((nx,ny)); st.append((nx,ny))
            res.append((v,cc))
    return res
for v,cc in comps('B74'):
    if len(cc)<3:
        nb=Counter(g[y+dy][x+dx] for x,y in cc for dx,dy in((1,0),(-1,0),(0,1),(0,-1)) if op(x+dx,y+dy) and g[y+dy][x+dx] in 'B74' and g[y+dy][x+dx]!=v)
        for x,y in cc: put('fix',x,y,'s' if edge(x,y) else (nb.most_common(1)[0][0] if nb else 's'),'houtvlakje <3 px')
for (x,y) in [(37,9),(37,10)]: put('fix',x,y,'s','smal tonrandje tussen hoepelzwart en buitenlijn: lijn (zoals r2)')
for y in range(H):
    for x in range(Wd):
        if g[y][x] in 'B74' and edge(x,y): put('fix',x,y,'s','hout op de rand -> lijn')
# ---- 5. buitenlijn: één kleur per randstuk ----
for y in range(H):
    for x in range(Wd):
        if g[y][x] not in '0sn' or not edge(x,y): continue
        e=edge(x,y)
        if (0,1) in e or y>=28: c='0'
        elif (0,-1) in e or (-1,0) in e: c='s'
        else: c='0'
        if c=='s' and x<=8 and 7<=y<=18: c='n'
        put('lijn',x,y,c,'buitenlijn lichtkant selout / schaduwkant zwart')
for _ in range(3):
    for y in range(H):
        for x in range(Wd):
            if g[y][x] not in '0sn' or not edge(x,y): continue
            nb=[g[y+dy][x+dx] for dx in(-1,0,1) for dy in(-1,0,1) if (dx or dy) and op(x+dx,y+dy) and g[y+dy][x+dx] in '0sn' and edge(x+dx,y+dy)]
            if len(nb)>=2 and nb.count(g[y][x])==0:
                put('lijn',x,y,Counter(nb).most_common(1)[0][0],'om-en-om weg')
# ---- uitvoer ----
OX,OY=d['OX'],d['OY']
img=np.zeros((64,64),'uint8')
for y in range(H):
    for x in range(Wd): img[OY+y,OX+x]=ORDER.index(g[y][x])
pal=sum((list(PAL[k]) for k in ORDER),[])+[0]*3*(256-len(ORDER))
im=Image.fromarray(img,'P'); im.putpalette(pal); im.save(R+f'sprite/r3/capybarrel_{var}.png',transparency=0)
json.dump({'OX':OX,'OY':OY,'grid':[''.join(r) for r in g],'kaal':kaal},open(R+f'sprite/r3/grid_{var}.json','w'))
ad=[(x,y,r2[y][x],g[y][x]) for y in range(H) for x in range(Wd) if (g[y][x]=='.')!=(r2[y][x]=='.')]
print(var,'zones t.o.v. r2',dict(Counter(z for z,*_ in log)),'| alpha-diff t.o.v. r2:',ad)
open(R+f'sprite/r3/log_{var}.txt','w').write(''.join('%s (%d,%d) %s->%s  %s\n'%e for e in log))
