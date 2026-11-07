"""Ronde 4 (driekwart naar links-voor, grof): zelfde vogel als ronde 3 gedraaid. Kop/snavel/muil bewust grof (Jordi tekent erover).
Opbouw: vormen (kop, borst, verre vleugel, nabije vleugel, staart) als vlakken, daarna schaduw, lijnen en details met de hand."""
import sys, math
W=64; G=[['.']*W for _ in range(W)]; Z=[[0]*W for _ in range(W)]   # Z = laag (hoger = voor)
def ell(cx,cy,rx,ry,x,y): return ((x-cx)/rx)**2+((y-cy)/ry)**2<=1
def put(test,c,z):
    for y in range(W):
        for x in range(W):
            if test(x,y) and z>=Z[y][x]: G[y][x]=c; Z[y][x]=z
# staart (achter): breed, plat, iets rechts achter het lijf
put(lambda x,y: 48<=y<=62 and 28-(y-48)*0.12 <= x <= 40+(y-48)*0.1,'S',1)
# verre vleugel: smal links achter de borst
put(lambda x,y: ell(22,36,5,14,x,y) and x<=23,'V',2)
# borst/lijf: peer, schouders breed
put(lambda x,y: ell(31,33,12,13,x,y) or (ell(32,45,9,9,x,y)),'B',3)
# nabije vleugel rechts langs de flank tot de punt op de staart
def nw(x,y):
    if y<20 or y>58: return False
    xl=38-min(y-20,6)*0.5 if y<40 else 35+(y-40)*0.35
    top=max(0,26-y); xr=47-top*0.9 if y<44 else 47-(y-44)*0.55
    return xl<=x<=xr
put(nw,'W',4)
# kop: bol, iets naar links
put(lambda x,y: ell(29,12,11,11,x,y),'K',5)
# muil: brede open bek onder de ogen, naar links-voor
def muil(x,y):
    if y<15 or y>30: return False
    t=(y-15)/15.0
    xl=17+ 8*t**1.8          # verre kaakrand: van onder de haak naar de punt
    xr=37- 11*t**0.7          # nabije kaakrand: van de mondhoek naar de punt
    return xl<=x<=xr
put(muil,'M',6)
# ---------- kleuren per vlak ----------
SH={'B':('6','5','4','3'),'K':('6','5','4','3'),'V':('4','3','F','F'),'W':('4','3','F','F'),'S':('5','4','3','3')}
cent={'B':(25,28,13),'K':(24,7,11),'V':(19,30,6),'W':(39,30,8),'S':(30,50,7)}
out=[['.']*W for _ in range(W)]
for y in range(W):
    for x in range(W):
        c=G[y][x]
        if c in SH:
            cx,cy,r=cent[c]; d=math.hypot(x-cx,y-cy)/r
            t=SH[c][0 if d<0.55 else 1 if d<1.0 else 2 if d<1.35 else 3]
            out[y][x]=t
        elif c=='M': out[y][x]='A'
# muil: binnenkant donker achterin, licht onderin, tong; lichte kaakrand
for y in range(W):
    for x in range(W):
        if G[y][x]!='M': continue
        nb=[G[y+dy][x+dx] for dx,dy in ((1,0),(-1,0),(0,1),(0,-1))]
        if any(n!='M' for n in nb):
            out[y][x]='D'
        elif y<=17: out[y][x]='9'
        elif y>=26: out[y][x]='C'
        elif y>=22: out[y][x]='B'
# ---------- buitenlijn + binnenlijnen ----------
def at(x,y): return G[y][x] if 0<=x<W and 0<=y<W else '.'
res=[r[:] for r in out]
for y in range(W):
    for x in range(W):
        if G[y][x]=='.': continue
        nb=[at(x+dx,y+dy) for dx,dy in ((1,0),(-1,0),(0,1),(0,-1))]
        if '.' in nb:
            res[y][x]='2' if (x<30 and y<40) else '1'
        elif any(Z[y+dy][x+dx]<Z[y][x] and G[y+dy][x+dx]!='M' and G[y][x]!='M' for dx,dy in ((1,0),(-1,0),(0,1),(0,-1)) if 0<=y+dy<W and 0<=x+dx<W):
            res[y][x]='2'
        elif G[y][x]=='M' and any(G[y+dy][x+dx]!='M' for dx,dy in ((1,0),(-1,0),(0,1),(0,-1))):
            res[y][x]='D'
out=res
def P(pts,c):
    for x,y in pts: out[y][x]=c
# mondlijn boven (snijrand) en bovensnavel met haak, grof
for x in range(16,38): 
    if G[15][x]=='M': out[15][x]='1'
P([(17,14),(18,14),(19,14),(20,14)],'1'); P([(18,13),(19,13),(20,13),(21,13),(22,13)],'7'); P([(17,13),(18,12),(19,12),(20,12),(21,12),(22,12),(23,12)],'1')
P([(16,14),(16,15),(16,16),(17,17)],'1'); P([(17,15),(17,16)],'E'); P([(17,14)],'7')
# kaakpunt
for y in range(16,31):
    for x in range(W):
        if G[y][x]!='M' and G[y][x]!='.' and any(at(x+dx,y+dy)=='M' for dx,dy in ((1,0),(-1,0),(0,-1),(1,-1),(-1,-1))): out[y][x]='2' if y<27 else '1'
for x,y in [(24,28),(25,28),(26,28),(25,29),(26,29),(25,30)]:
    if G[y][x]=='M': out[y][x]='E'
# ogen: nabij groot (puur zwart), ver half
for y in range(5,12):
    for x in range(29,36):
        if ell(32,8.3,3.3,3.3,x,y): out[y][x]='8'
for y in range(6,11):
    for x in range(16,21):
        if ell(21.3,8.6,1.4,2.6,x,y) and G[y][x]=='K': out[y][x]='8'
# borstelveertjes tussen de ogen
P([(24,9),(24,10),(25,10),(26,11),(26,12),(27,12),(22,10),(22,11),(23,11)],'3')
# vleugel: pennen, dekveren, schorsstreepjes
for x0 in (40,43):
    for y in range(38,56):
        if G[y][x0+ (y-38)//8]=='W': out[y][x0+(y-38)//8]='2'
for y,xs in ((28,range(38,46)),(33,range(38,46))):
    for x in xs:
        if G[y-(x-38)//3][x]=='W': out[y-(x-38)//3][x]='2'
for x,y in [(40,24),(43,26),(41,30),(44,35),(39,42),(42,46)]:
    for d in range(3):
        if out[y+d][x] in '34': out[y+d][x]='7'
# staart: middenlijn, banden, veerpunten
for y in (53,57):
    for x in range(29,34):
        if out[y][x] in '45': out[y][x]='3'
for x,y in [(31,62),(32,62),(36,62),(37,62)]: out[y][x]='.'
P([(31,61),(32,61),(36,61),(37,61)],'1')
# borst: een paar streepjes en schorsvlekjes
for x,y in [(24,32),(29,36),(26,40),(32,31),(31,43)]:
    for d in range(3):
        if out[y+d][x] in '56': out[y+d][x]='4'
for x,y in [(35,26),(22,26)]:
    for d in range(2):
        if out[y][x+d] in '456': out[y][x+d]='7'
for x,y in [(29,1),(40,12),(17,36),(22,50)]: out[y][x]='.'
for (x,y),c in {(29,2):'2',(39,12):'1',(18,36):'2',(22,49):'1'}.items(): out[y][x]=c
open(sys.argv[1] if len(sys.argv)>1 else 'raster.txt','w').write('\n'.join(''.join(r) for r in out)+'\n')
