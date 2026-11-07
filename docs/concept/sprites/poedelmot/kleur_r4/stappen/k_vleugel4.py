# vleugels: licht crème, witte geschulpte buitenrand, tan schubbogen als golvende 'wolkjes'
# (ketting van kleine boogjes per ring) die naar de vleugelvoet dichter en donkerder worden
import math
Z=set(tuple(map(int,l.split(','))) for l in open('spriet_zone.txt'))
DIAG={30:37,31:37,32:38,33:38,34:38,35:38,36:39,37:39,38:39,39:39,40:40,41:40,42:40,43:40,44:41,45:41,46:41,47:41}
def binnen(x,y): return r[y][x]!='.' and (x,y) not in Z and x>DIAG.get(y,36)+1
def zoom(x): return 36 + (0 if (x-41)%4 in (0,3) else 1) - (1 if x>=53 else 0)
FORE=lambda x,y: y<zoom(x)
def wolk(x,y,bx,by,R,amp=0.9,dik=0.75):
    d=math.hypot(x-bx,y-by); t=math.atan2(y-by,x-bx)
    return abs(d-(R+amp*abs(math.sin(t*R*0.785))))<dik
for y in range(19,37):
    for x in range(40,64):
        if not binnen(x,y) or not FORE(x,y): continue
        d=math.hypot(x-40,y-35); c='7'
        if d>18: c='A'
        for R,col in ((7,'5'),(11.5,'6'),(16,'6')):
            if wolk(x,y,40,35,R): c=col
        if d<2.8: c='5'
        elif d<4.8 and c=='7': c='6'
        r[y][x]=c
for x in range(41,59):
    y=zoom(x)
    if r[y][x]!='.': r[y][x]='3'
    if r[y-1][x] not in '.': r[y-1][x]='A'
    if x<58 and zoom(x+1)!=y and r[zoom(x+1)][x]!='.': r[zoom(x+1)][x]='3'
for y in range(35,47):
    for x in range(40,64):
        if not binnen(x,y) or FORE(x,y) or y==zoom(x): continue
        d=math.hypot(x-41,y-39); c='7'
        if d>12.5: c='A'
        for R,col in ((5.5,'6'),(9.5,'6')):
            if wolk(x,y,41,39,R): c=col
        if d<3.8 and c in '75': c='6'
        if y==zoom(x)+1: c='A'
        r[y][x]=c
ond=lambda x: 46-(1 if (x-43)%4 in (1,2) else 0)
for x in range(43,54):
    y=ond(x)
    if r[y][x]!='.': r[y][x]='3'
    if x<53 and ond(x+1)!=y and r[ond(x+1)][x]!='.': r[ond(x+1)][x]='3'

# lichte lobboogjes in de witte buitenrand (geschulpt, geen band)
for cx,cy in [(59,21),(60,26),(59,31),(54,39),(54,43)]:
    for y in range(cy-2,cy+3):
        x=cx-2+(1 if abs(y-cy)==2 else 0)
        if r[y][x]=='A': r[y][x]='7'
