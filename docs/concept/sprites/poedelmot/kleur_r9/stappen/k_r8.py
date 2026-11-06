# r8: vleugelvlak licht crème, krullen als dunne 1 px tan boogjes op de modelplekken, buik als losse plaatjes
import math
Z=set(tuple(map(int,l.split(','))) for l in open('spriet_zone.txt'))
DIAG={y:36+round((y-29)*6/17) for y in range(30,48)}
def vleugel(x,y): return r[y][x] not in '.1234' and (x,y) not in Z and x>DIAG.get(y,37)+1 and y<=45
# 1) vlak terug naar licht crème; wit bovenaan en 2 px langs de rechterrand; tan voet
for y in range(19,46):
    xs=[x for x in range(40,64) if r[y][x]!='.']; e=max(xs) if xs else 0
    for x in range(40,64):
        if not vleugel(x,y): continue
        c='9'
        if y<=22 or x>=e-2: c='A'
        if math.hypot(x-40,y-35)<3.5 or math.hypot(x-41,y-40)<2.5: c='6'
        if x==DIAG.get(y,0)+2 and y<46: c='A'          # wit randje langs de kop
        r[y][x]=c
# 2) krullen: brede ondiepe schubbogen, bol naar de vleugelrand (weg van de voet), 1 px, één tint
BOG=[(55,22),(58,27),(56,32),(49,24),(52,29),(50,33),(46,30),(53,39),(55,43),(48,40),(50,44)]
lijn=set()
for px,py in BOG:
    bx,by=(41,39) if py>=37 else (40,35)
    t0=math.atan2(py-by,px-bx); R=4.5
    cx=px-R*math.cos(t0); cy=py-R*math.sin(t0)
    prev=None
    for i in range(41):
        t=t0+math.radians(-45+90*i/40)
        x=round(cx+R*math.cos(t)); y=round(cy+R*math.sin(t))
        if (x,y)==prev: continue
        prev=(x,y)
        if 0<=x<64 and 0<=y<64 and vleugel(x,y): r[y][x]='6'; lijn.add((x,y))
open('krul_lijnen.txt','w').write('\n'.join(f'{x},{y}' for x,y in sorted(lijn))+'\n')
# 3) buik: 2-3 losse tan plaatjes met een lichte naad ertussen
for y in range(47,57):
    for x in range(30,42):
        if r[y][x] in '56789A' and r[y][x]!='8':
            naad=y in (50+round(((x-36)/4.0)**2), 53+round(((x-36)/4.0)**2))
            r[y][x]='9' if naad else ('6' if (x-31)+(y-47)>2 else '7')
