import math
Z=set(tuple(map(int,l.split(','))) for l in open('spriet_zone.txt'))
DIAG={30:37,31:37,32:38,33:38,34:38,35:38,36:39,37:39,38:39,39:39,40:40,41:40,42:40,43:40,44:41,45:41,46:41,47:41}
def binnen(x,y): return r[y][x]!='.' and (x,y) not in Z and x>DIAG.get(y,36)+1
# scheiding voor/achtervleugel: geschulpte zoom (golft tussen y35 en y37), van x41 tot de rand
def zoom(x): return 36 + (0 if (x-41)%4 in (0,3) else 1) - (1 if x>=53 else 0)
FORE=lambda x,y: y<zoom(x)
# ---- voorvleugel
for y in range(19,37):
    for x in range(40,64):
        if not binnen(x,y) or not FORE(x,y): continue
        d=math.hypot(x-40,y-34)
        c='7'
        if d>17.5: c='A'
        if abs(d-9.5)<0.6 and y<=33: c='6'          # boog 1
        if abs(d-15)<0.6 and y<=33: c='6'           # boog 2
        if d<4.5: c='6'
        r[y][x]=c
for x in range(41,59):
    y=zoom(x)
    if r[y][x]!='.': r[y][x]='3'
    if r[y-1][x] not in '.': r[y-1][x]='A'          # witte zoom van de voorvleugel
    if x<58 and zoom(x+1)!=y and r[zoom(x+1)][x]!='.': r[zoom(x+1)][x]='3'   # doorlopende golflijn
# lobboogjes langs de geschulpte buitenrand (geen band)
for cx,cy in [(60,21),(61,26),(60,31)]:
    for y in range(cy-2,cy+3):
        x=cx-2+(1 if abs(y-cy)==2 else 0)
        if binnen(x,y) and FORE(x,y): r[y][x]='6'
# ---- achtervleugel
for y in range(35,47):
    for x in range(40,64):
        if not binnen(x,y) or FORE(x,y) or y==zoom(x): continue
        d=math.hypot(x-41,y-40); e=math.hypot(x-35,y-33)
        c='7'
        if d>12.5: c='A'
        if abs(e-11)<0.6 and x>42: c='6'
        if abs(e-16)<0.6 and x>42: c='6'
        if d<3.2: c='6'
        if y==zoom(x)+1: c='A'                       # witte bovenzoom
        r[y][x]=c
# onderrand achtervleugel geschulpt
ond=lambda x: 46-(1 if (x-43)%4 in (1,2) else 0)
for x in range(43,54):
    y=ond(x)
    if r[y][x]!='.': r[y][x]='3'
    if x<53 and ond(x+1)!=y and r[ond(x+1)][x]!='.': r[ond(x+1)][x]='3'
