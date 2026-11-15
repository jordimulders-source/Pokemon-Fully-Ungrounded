# r8: twee varianten van de bolinhoud op basis van raster_af.txt (alleen binnen de bol; barst, glasrand en glans blijven).
# A = dichte sneeuwjacht (vlokken + schuine veegjes, met de klok mee rond het midden, dichter aan de buitenkant van de wervel)
# B = als fase 1: plusvlokken van 5 px + losse witte pixels + 2 gebogen wervelbanen.
# Vanuit sneeuwbolslak_fase2/: python3 sprite/maker/r8_bouw.py
import math
O=[l.rstrip('\n') for l in open('sprite/maker/raster_af.txt')]
CX,CY=31.5,31.0
BARST={(36,25),(35,26),(35,27),(35,28),(34,29),(33,30),(32,30),(31,31),(30,32),(30,33),(36,29),(36,30),(37,31),(37,32),(37,33),(36,34),(36,35),(36,36),(37,37)}
GLANS={(x,y) for x in range(23,29) for y in range(25,29) if math.hypot(x-25.3,y-26.5)<=2.6}
def vrij(x,y):  # doorkijkvlak: binnen de glasrand, geen barst, geen glans
    return 22<=x<=41 and 23<=y<=38 and O[y][x] not in '#.' and math.hypot(x-CX,y-CY)<=8.3 and (x,y) not in BARST and (x,y) not in GLANS
def basis():
    R=[list(r) for r in O]
    for y in range(23,39):
        for x in range(22,42):
            if vrij(x,y): R[y][x]='b'
    return R
def zet(R,ch,pts):
    for x,y in pts:
        if vrij(x,y): R[y][x]=ch
def schrijf(R,f):
    for y in range(64):
        for x in range(64):
            if R[y][x]!=O[y][x] and not (22<=x<=41 and 23<=y<=38): raise SystemExit(f'buiten bol {x},{y}')
    open(f,'w').write('\n'.join(''.join(r) for r in R)+'\n')
# ---- A: sneeuwjacht. Twee spiraalarmen (met de klok mee) van schuine veegjes langs de draairichting; vlokken dichter buiten, kern rustig.
import random
rnd=random.Random(7)
A=basis()
def raak(x,y): return any(A[y+dy][x+dx] in 'w' for dx in (-1,0,1) for dy in (-1,0,1) if (dx,dy)!=(0,0))
for arm in (0,180):
    for i in range(10):
        t=i/9; h=math.radians(arm+40+t*250); r=3.2+t*4.6          # spiraal naar buiten
        x0,y0=CX+r*math.cos(h),CY+r*math.sin(h)
        tx,ty=-math.sin(h),math.cos(h)                              # raaklijn, met de klok mee
        n=2 if t<0.5 else 3
        pts=[(int(round(x0+k*tx)),int(round(y0+k*ty))) for k in range(n)]
        if any(not vrij(*q) for q in pts): continue
        zet(A,'w' if t>0.35 else 'e',pts[:1]); zet(A,'e' if n==2 else 'w',pts[1:2]); zet(A,'e',pts[2:])
for _ in range(400):                                                 # losse vlokken, dichter buiten
    x,y=rnd.randint(22,41),rnd.randint(23,38)
    if not vrij(x,y) or A[y][x]!='b': continue
    r=math.hypot(x-CX,y-CY)
    if rnd.random()< (0.05 if r<4 else 0.22 if r<6.5 else 0.38) and not raak(x,y):
        A[y][x]='w' if rnd.random()<0.65 else 'e'
schrijf(A,'sprite/maker/raster_r8A.txt')
# ---- B: als fase 1
B=basis()
def plus(x,y): return [(x,y),(x-1,y),(x+1,y),(x,y-1),(x,y+1)]
baan1=[(26,24),(27,24),(28,23),(29,23),(30,24),(31,24),(32,25)]                        # boven, buigt naar de barst
baan2=[(24,30),(24,31),(25,32),(26,33),(27,34),(28,34),(29,35),(30,35),(31,36),(32,36),(33,35)]  # links omlaag en onderlangs
zet(B,'e',baan1+baan2)
for p in [(29,27),(38,29),(33,33),(26,36)]: zet(B,'w',plus(*p))
zet(B,'w',[(33,24),(39,33),(28,31),(31,29),(37,36),(23,33),(34,37)])
schrijf(B,'sprite/maker/raster_r8B.txt')
print('ok')
