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
# 2) krullen: halve boogjes (1 px), (cx, cy, straal, hoek_van, hoek_tot) in graden; plekken uit het model
KRUL=[(48,29,3.0,80,360),                                  # grote krul voorvleugel (open naar rechts)
      (52,22,2.5,180,360),(57,23,2.3,270,450),             # rij langs de bovenrand
      (53,28,2.5,200,380),(58,28,2.2,270,450),             # middenrij
      (52,33,2.2,180,360),(57,32,2.0,270,430),             # onderrij voorvleugel
      (46,39,2.4,60,330),(51,41,2.2,180,360),(55,39,1.8,270,450),(52,44,1.8,180,330)]   # achtervleugel
lijn=set()
for cx,cy,R,a0,a1 in KRUL:
    for i in range(0,int((a1-a0)*R/20)+2):
        t=math.radians(a0+(a1-a0)*i/max(1,int((a1-a0)*R/20)+1))
        x=round(cx+R*math.cos(t)); y=round(cy+R*math.sin(t))
        if 0<=x<64 and 0<=y<64 and vleugel(x,y):
            r[y][x]='5' if math.hypot(x-40,y-36)<9 else '6'; lijn.add((x,y))
open('krul_lijnen.txt','w').write('\n'.join(f'{x},{y}' for x,y in sorted(lijn))+'\n')
# 3) buik: 2-3 losse tan plaatjes met een lichte naad ertussen
for y in range(47,57):
    for x in range(30,42):
        if r[y][x] in '56789A' and r[y][x]!='8':
            naad=y in (50+round(((x-36)/4.0)**2), 53+round(((x-36)/4.0)**2))
            r[y][x]='9' if naad else ('6' if (x-31)+(y-47)>2 else '7')
