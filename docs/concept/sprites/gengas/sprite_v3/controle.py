# Controles: kleuren, losse pixels, omlijning, cirkelfit, afwijking t.o.v. de dichtstbijzijnde modeltint.
# gebruik: controle.py raster.txt
import sys
from gemeen import *
from pal import PAL,CH
R=[l.rstrip('\n') for l in open(sys.argv[1])][:64]
I=np.array([[CH.index(c) for c in r] for r in R])
a=model(); bg=achtergrond(a)
q,_=dichtst(a,PAL[1:]); q=q+1; q[bg]=0
print('kleuren gebruikt:',len(set(I.flat)-{0}),'+ transparant')
sil_m=~bg; sil_s=I>0
print('silhouet: pixels anders dan model:',int((sil_m!=sil_s).sum()),[tuple(map(int,p)) for p in np.argwhere(sil_m!=sil_s)])
d=(I!=q)&sil_s
print('pixels afwijkend van de dichtstbijzijnde modeltint op dezelfde plek:',int(d.sum()))
# gezichtsblok: vergelijk met het model op de NIEUWE plek (blok rij 28-45 kol 8-27 verschoven +1/+5)
qs=q.copy(); qs[29:47,13:33]=q[28:46,8:28]
ds=(I!=qs)&sil_s
print('  idem, met het gezichtsblok vergeleken met het verschoven model:',int(ds.sum()),
      '(waarvan in de vrijgekomen strook kol 8-12 rij 28-46:',int(ds[28:47,8:13].sum()),')')
# losse pixels: eiland van 1 px (4-samenhang) in een vulkleur
VUL=set('abmlvwgGhH')
los=[]
for y in range(64):
    for x in range(64):
        c=R[y][x]
        if c not in VUL: continue
        if not any(0<=y+dy<64 and 0<=x+dx<64 and R[y+dy][x+dx]==c for dy,dx in ((1,0),(-1,0),(0,1),(0,-1))): los.append((y,x,c))
print('losse 1-px vulpixels:',len(los),los)
# omlijningspixels zonder enige omlijningsbuur (8-buren) en niet aan transparant
Kl=[]
for y in range(64):
    for x in range(64):
        if R[y][x]!='K': continue
        nb=[R[y+dy][x+dx] if 0<=y+dy<64 and 0<=x+dx<64 else '.' for dy in(-1,0,1) for dx in(-1,0,1) if dy or dx]
        if 'K' not in nb and 'g' not in nb and 'r' not in nb: Kl.append((y,x))
print('omlijningspixels die nergens aan grenzen:',Kl)
# randpixels die licht zijn (geen K/r/a/g en niet de gaswolkjes boven rij 20 of de rookpluim rechts)
rl=[]
for y in range(64):
    for x in range(64):
        c=R[y][x]
        if c=='.' or c in 'Krabg': continue
        if any(not(0<=y+dy<64 and 0<=x+dx<64) or R[y+dy][x+dx]=='.' for dy,dx in ((1,0),(-1,0),(0,1),(0,-1))): rl.append((y,x,c))
print('lichte pixels op de buitenrand (gas-oorpunten en rookslierten horen er bewust bij):',rl)
# cirkelfit van de bol: buitenrand van het lijf rij 22-58, alleen randpunten die aan transparant grenzen,
# zonder manen (grijs) en zonder de rookarm rechtsboven (x>=46, y<30)
pts=[]
for y in range(22,59):
    for x in range(64):
        if R[y][x] in '.gGhHW' : continue
        if x>=46 and y<30: continue
        nb8=[R[y+dy][x+dx] for dy in(-1,0,1) for dx in(-1,0,1) if 0<=y+dy<64 and 0<=x+dx<64]
        if not any(c in 'abrmlvw' for c in nb8): continue  # omlijning van een maan, niet van de bol
        if any(R[y+dy][x+dx]=='.' for dy,dx in ((1,0),(-1,0),(0,1),(0,-1)) if 0<=y+dy<64 and 0<=x+dx<64): pts.append((x+.5,y+.5))
P=np.array(pts); A=np.c_[2*P,np.ones(len(P))]; b=(P**2).sum(1)
cx,cy,c=np.linalg.lstsq(A,b,rcond=None)[0]; r=np.sqrt(c+cx*cx+cy*cy)
res=np.hypot(P[:,0]-cx,P[:,1]-cy)-r
print(f'cirkelfit bol: middelpunt ({cx:.1f},{cy:.1f}) straal {r:.1f}, {len(P)} randpunten, afwijking rms {np.sqrt((res**2).mean()):.2f} px, max {np.abs(res).max():.2f} px')
