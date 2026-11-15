# r9: (1) mondlijn op het modelpad (kop), (2) sterkere sneeuwstorm in de bol; plusvlokken van r8C blijven exact staan.
# Basis raster_af.txt (= r8C). Vanuit sneeuwbolslak_fase2/: python3 sprite/maker/r9_bouw.py
import math, random, sys
sys.argv=[sys.argv[0]]
exec(open('sprite/maker/r8_bouw.py').read().split('# ---- A:')[0])   # O, vrij(), basis(), zet(), schrijf()
R=[list(r) for r in O]
# ---- 1. mond. Model (px.py p15): snuithoek (9,47) 69, (8,48) 60, (7,49) 85; kaaklijn y50 x8-13 L 122-142 (a);
#         onder de wang (15-18,51) p15 50-59, omhoog (19,50)(20,49)(20,48). Oude losse diagonaal (9,47)(8,48)(7,49) wordt deel van de lijn.
MOND=[((9,47),'a'),((8,48),'d'),((7,49),'d'),((8,50),'d'),((9,50),'d'),((10,50),'a'),((11,50),'a'),((12,50),'a'),((13,50),'a')]
# daarna loopt hij via de bestaande (14-15,51) a en (16-18,51) d onder de wang door en via (19,50)(20,49)(20,48) omhoog (staat al in r8C).
for (x,y),ch in MOND:
    assert R[y][x] not in '.#', (x,y); R[y][x]=ch
# ---- 2. bol: plusvlokken exact uit r8C, met 1 px vrije rand; storm eromheen sterker
PLUS=[(29,27),(38,29),(33,33),(26,36)]
pl=lambda x,y:[(x,y),(x-1,y),(x+1,y),(x,y-1),(x,y+1)]
VRIJ=set()
for p in PLUS:
    for q in pl(*p):
        for dx in (-1,0,1):
            for dy in (-1,0,1): VRIJ.add((q[0]+dx,q[1]+dy))
for y in range(23,39):
    for x in range(22,42):
        if vrij(x,y): R[y][x]='b'
def mag(x,y): return vrij(x,y) and (x,y) not in VRIJ
rnd=random.Random(11)
for arm in (0,120,240):                                   # drie spiraalarmen, met de klok mee, naar buiten toe langer
    for i in range(12):
        t=i/11; h=math.radians(arm+20+t*230); r=2.6+t*5.4
        x0,y0=CX+r*math.cos(h),CY+r*math.sin(h); tx,ty=-math.sin(h),math.cos(h)
        n=2 if t<0.3 else 3 if t<0.7 else 4
        pts=[(int(round(x0+k*tx)),int(round(y0+k*ty))) for k in range(n)]
        for k,(x,y) in enumerate(pts):
            if mag(x,y): R[y][x]='w' if k<n-1 else 'e'
def buur_w(x,y): return any(R[y+dy][x+dx]=='w' for dx in (-1,0,1) for dy in (-1,0,1) if (dx,dy)!=(0,0))
for _ in range(600):                                      # losse vlokken, dichter buiten
    x,y=rnd.randint(22,41),rnd.randint(23,38)
    if not mag(x,y) or R[y][x]!='b' or buur_w(x,y): continue
    r=math.hypot(x-CX,y-CY)
    if rnd.random()<(0.08 if r<3.5 else 0.3 if r<6 else 0.5): R[y][x]='w' if rnd.random()<0.7 else 'e'
for p in PLUS:
    for x,y in pl(*p): R[y][x]='w'
open('sprite/maker/raster_r9.txt','w').write('\n'.join(''.join(r) for r in R)+'\n')
A=[l.rstrip('\n') for l in open('sprite/maker/raster_af.txt')]
ch=[(x,y) for y in range(64) for x in range(64) if A[y][x]!=R[y][x]]
print('gewijzigd',len(ch),'buiten kop+bol',[p for p in ch if not ((22<=p[0]<=41 and 23<=p[1]<=38) or (p[0]<=21 and 40<=p[1]<=52))])
print('plus ok', all(R[y][x]=='w' for p in PLUS for x,y in pl(*p)))
