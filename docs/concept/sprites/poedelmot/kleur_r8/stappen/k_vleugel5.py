import math
Z=set(tuple(map(int,l.split(','))) for l in open('spriet_zone.txt'))
DIAG={y:36+round((y-29)*6/17) for y in range(30,48)}
def binnen(x,y): return r[y][x]!='.' and (x,y) not in Z and x>DIAG.get(y,36)+1
# geschulpte zoom: ongelijke lobjes (breedtes 5-4-6-3), hangend naar onder
SEG=[(41,5),(46,4),(50,6),(56,3)]
def zoom(x):
    for x0,w in SEG:
        if x0<=x<x0+w: return 35+round(2.4*math.sin(math.pi*(x-x0+0.5)/w))
    return 35
FORE=lambda x,y: y<zoom(x)
rechts={}
for y in range(64):
    xs=[x for x in range(64) if r[y][x]!='.']
    if xs: rechts[y]=max(xs)
# ---- voorvleugel: egaal licht crème, wit aan de lichtkant (boven), schaduwtint aan de schaduwkant (rechts)
LOB=[(48,29,2.6),(54,24,2.1),(54,31,2.0)]      # grote ronde lobben/krullen zoals het model
for y in range(19,38):
    for x in range(40,64):
        if not binnen(x,y) or not FORE(x,y): continue
        c='9'
        if y<=23 or (x>=51 and y<=27 and x<rechts[y]-2): c='A'      # witte buitenzone, lichtkant
        if x>=rechts[y]-2 and y>=26: c='7'                            # schaduwkant rechts
        dv=math.hypot(x-40,y-35)
        if dv<4.5: c='6'
        elif dv<7.5: c='7'                                            # vleugelvoet tan -> crème
        for cx,cy,R in LOB:
            d=math.hypot(x-cx,y-cy)
            if d<=R:
                c='7'
                if d>R-1.0 and (x-cx)+(y-cy)>0.3: c='6'                 # boog rechtsonder
        r[y][x]=c
# inkepingen van de geschulpte rand als korte binnenlijntjes
for pts in [[(60,24),(59,24)],[(59,29),(58,29)],[(57,33),(56,33)]]:
    for x,y in pts:
        if r[y][x]!='.': r[y][x]='3'
# zoomlijn + witte lobjes erboven (alleen links/licht), crème aan de rechterkant
prev=None
for x in range(41,59):
    y=zoom(x)
    if r[y][x]!='.': r[y][x]='3'
    if prev is not None and prev!=y:
        for yy in range(min(prev,y),max(prev,y)+1):
            if r[yy][x]!='.' and yy!=y: r[yy][x-1 if yy==prev else x]='3'
    prev=y
    if r[y-1][x] not in '.3': r[y-1][x]='A' if x<52 else '9'
# ---- achtervleugel: lichter, tan alleen bovenaan onder de voorvleugel en bij de voet
HL=[(46,40,2.0),(51,42,1.8)]
for y in range(35,46):
    for x in range(40,64):
        if not binnen(x,y) or FORE(x,y) or r[y][x]=='3': continue
        c='9'
        if y<=zoom(x)+1: c='7'
        dv=math.hypot(x-41,y-39)
        if dv<3: c='6'
        if x>=rechts[y]-3 and y<=41: c='A'                         # witte lobben rechts
        if x>=rechts[y]-2 and y>=42: c='7'
        for cx,cy,R in HL:
            d=math.hypot(x-cx,y-cy)
            if d<=R:
                c='7'
                if d>R-1 and (x-cx)+(y-cy)>0.3: c='6'
        r[y][x]=c
for pts in [[(55,40),(54,40)],[(53,44),(52,44)]]:
    for x,y in pts:
        if r[y][x]!='.': r[y][x]='3'
# onderrand achtervleugel: ongelijke lobben (4-3-5)
SEG2=[(43,4),(47,3),(50,5)]
def ond(x):
    for x0,w in SEG2:
        if x0<=x<x0+w: return 44+round(2.0*math.sin(math.pi*(x-x0+0.5)/w))
    return 45
prev=None
for x in range(43,55):
    y=ond(x)
    if r[y][x]!='.': r[y][x]='3'
    if prev is not None and abs(prev-y)>1 and r[(prev+y)//2][x]!='.': r[(prev+y)//2][x]='3'
    prev=y
