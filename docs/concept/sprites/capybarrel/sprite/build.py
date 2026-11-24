# Bouwt r1: kale reductie (kaal_lab.npy) -> paletmapping -> benoemde reparaties per zone -> oog uit Gen 3-bron -> buitenlijn.
# Elke afwijking van de (gemapte) kale reductie wordt per zone geteld en gelogd.
import numpy as np, sys, json
from PIL import Image
R='/home/user/Pokemon-Fully-Ungrounded/docs/concept/sprites/capybarrel/sprite/'
PAL={'.':(0,0,0),'0':(32,20,28),'s':(104,52,40),'C':(226,146,112),'A':(196,114,90),'5':(150,82,70),
     '9':(132,126,132),'3':(90,78,84),'n':(56,44,52),'B':(222,140,72),'7':(182,98,48),'4':(142,68,36),
     'D':(208,208,216),'W':(255,255,255)}
ORDER=list(PAL)
MAP={0:'0',1:'s',2:'s',3:'3',4:'4',5:'5',6:'5',7:'7',8:'A',9:'9',10:'A',11:'B',12:'C',13:'D'}
L=np.load(R+'kaal_lab.npy'); H,Wd=L.shape
g=[['.' if v<0 else MAP[v] for v in row] for row in L]
kaal=[r[:] for r in g]
log=[]
def put(zone,x,y,c,why):
    old=g[y][x]
    if old!=c: g[y][x]=c; log.append((zone,x,y,old,c,why))
# --- mond/tanden (model: twee snijtanden onder de neus, voorste wit, achterste in schaduw) ---
for (x,y,c) in [(3,17,'W'),(4,17,'0'),(1,18,'.'),(2,18,'0'),(3,18,'W'),(4,18,'D'),(5,18,'0'),
                (2,19,'.'),(3,19,'0'),(4,19,'D'),(5,19,'0'),(4,20,'0'),(3,20,'.')]:
    put('mond',x,y,c,'tanden naar model')
# --- neus: philtrumlijn uit model (kolom 2, rij 13-16), lichte bovenkant, schaduw onderrand ---
for y in range(13,17): put('neus',2,y,'n','philtrumlijn model')
# --- oog: modeloog weg (wordt vervangen door Gen 3-oog) ---
for y in range(7,11):
    for x in range(12,17):
        if g[y][x] in '0D.89s35': put('oog',x,y,'A','modeloog weg')
# --- voorpoot nabij: tenen naar model ---
for (x,y,c) in [(22,31,'A'),(21,32,'A'),(22,32,'A'),(23,32,'s'),(25,33,'0')]:
    put('poten',x,y,c,'tenen naar model')
# --- achterpoot nabij: tenen + onderlijn (dunne modellijn viel weg) ---
for (x,y,c) in [(38,31,'A'),(39,31,'A'),(41,31,'A'),(42,32,'A'),(43,32,'0'),(39,33,'0'),(40,33,'0'),(41,33,'0'),(42,33,'0')]:
    put('poten',x,y,c,'tenen/onderlijn naar model')
extra=json.load(open(R+'extra.json')) if len(sys.argv)>2 else []
for zone,x,y,c,why in extra: put(zone,x,y,c,why)
# --- ogen (1-op-1 uit Gen 3, omgekleurd; '-' = huid van de bron = laat vacht staan) ---
EYES={
 'A':('hypno x22-28 y25-27',[ '--5n s--'.replace(' ',''), '-5 0WWs-'.replace(' ',''), '5s W0WWs'.replace(' ','')]),
}
EYES={
 'A':('hypno (x22-28,y25-27)',['--50s--','-50WWs-','5sW0WWs']),
 'B':('drowzee (x24-30,y19-22)',['-5----5','5-sss-5','5sWWWs-','sW0W---']),
 'C':('camerupt (x18-22,y39-43)',['s-ssD','ss0DD','sWWWD','-sWWs','--ss-']),
 'N':('numel (x21-24,y32-34)',['0DDs','0WWs','5Ws5']),
 'R':('rhyhorn (x17-21,y39-43)',['----0','---0W','-00sW','0W0sW','s555-']),
}
var=sys.argv[1]; naam,blk=EYES[var]
ax,ay={'A':(12,8),'B':(12,7),'C':(12,7),'N':(13,8),'R':(12,7)}[var]
for j,row in enumerate(blk):
    for i,c in enumerate(row):
        if c!='-': put('oog',ax+i,ay+j,c,'oog uit '+naam)

# --- ontkorrelen: tintvlakjes <3 px nemen de meest voorkomende buurtint uit dezelfde kleurgroep (oog/tand/neus-hooglicht uitgezonderd) ---
GROUPS=['CA5','B74','93n']
def comps():
    seen=set(); res=[]
    for y in range(H):
        for x in range(Wd):
            if (x,y) in seen or g[y][x] in '.0sWD': continue
            v=g[y][x]; st=[(x,y)]; seen.add((x,y)); c=[]
            while st:
                cx,cy=st.pop(); c.append((cx,cy))
                for dx,dy in((1,0),(-1,0),(0,1),(0,-1)):
                    nx,ny=cx+dx,cy+dy
                    if 0<=nx<Wd and 0<=ny<H and (nx,ny) not in seen and g[ny][nx]==v: seen.add((nx,ny)); st.append((nx,ny))
            res.append((v,c))
    return res
for _ in range(3):
    for v,c in comps():
        if len(c)>=3: continue
        if any(11<=x<=18 and 6<=y<=12 for x,y in c): continue   # oog
        if any(x<=3 and 9<=y<=10 for x,y in c): continue        # neus-hooglicht
        grp=[G for G in GROUPS if v in G][0]
        from collections import Counter
        nb=Counter(g[y+dy][x+dx] for x,y in c for dx,dy in((1,0),(-1,0),(0,1),(0,-1))
                   if 0<=x+dx<Wd and 0<=y+dy<H and g[y+dy][x+dx] in grp and g[y+dy][x+dx]!=v)
        if nb:
            for x,y in c: put('ontkorrel',x,y,nb.most_common(1)[0][0],'tintvlakje <3 px naar buurtint')
        elif v in 'B74' and len(c)==1:
            for x,y in c: put('ontkorrel',x,y,'s','losse houtpixel naar donkerste houttint')
# --- buitenlijn: elke rand-pixel donker; gekleurde selout waar de binnenbuur licht is ---
def opaque(x,y): return 0<=x<Wd and 0<=y<H and g[y][x]!='.'
for y in range(H):
    for x in range(Wd):
        if g[y][x]=='.' or g[y][x] in 'WD': continue
        edge=[(dx,dy) for dx,dy in ((1,0),(-1,0),(0,1),(0,-1)) if not opaque(x+dx,y+dy)]
        if not edge: continue
        if g[y][x] not in '0s': put('lijn',x,y,'0','buitenlijn dicht')
for y in range(H):
    for x in range(Wd):
        if g[y][x]!='0': continue
        ups=[(dx,dy) for dx,dy in ((0,-1),(-1,0)) if not opaque(x+dx,y+dy)]
        if not ups: continue
        dx,dy=ups[0]; ix,iy=x-dx,y-dy
        if opaque(ix,iy) and (g[iy][ix] in 'CAB' or (dy==-1 and g[iy][ix] in '57')):
            put('lijn',x,y,'s','selout lichtkant')
# onderrand altijd zwart
for y in range(H):
    for x in range(Wd):
        if g[y][x]=='s' and not opaque(x,y+1): put('lijn',x,y,'0','onderrand zwart')
# --- naar 64x64, onderaan gecentreerd (onderrand op y=56 zoals Zigzagoon/Numel 48-52 + figuurhoogte) ---
OX=(64-Wd)//2; OY=60-H
img=np.zeros((64,64),'uint8')
for y in range(H):
    for x in range(Wd):
        img[OY+y,OX+x]=ORDER.index(g[y][x])
pal=[]
for k in ORDER: pal+=PAL[k]
pal+= [0,0,0]*(256-len(ORDER))
im=Image.fromarray(img,'P'); im.putpalette(pal)
out=R+f'r1/capybarrel_{var}.png'; im.save(out,transparency=0)
json.dump({'OX':OX,'OY':OY,'grid':[''.join(r) for r in g],'kaal':[''.join(r) for r in kaal]},open(R+f'r1/grid_{var}.json','w'))
from collections import Counter
cnt=Counter(z for z,*_ in log)
print(var,naam,'afwijkingen per zone:',dict(cnt),'totaal',len(log),'van',sum(c!='.' for r in g for c in r),'px; kleuren',len(set(c for r in g for c in r)))
with open(R+f'r1/log_{var}.txt','w') as f:
    for e in log: f.write('%s (%d,%d) %s->%s  %s\n'%e)
