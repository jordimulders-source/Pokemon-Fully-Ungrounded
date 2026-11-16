# r7 (na Jordi 16 nov: "zorg dat alles in verhouding blijft, dus ook de grootte van de rechterarm"):
# hele kleine geest met één schaal t.o.v. het natieve model: 1 rij en 2 kolommen dupliceren die door de héle geest lopen
# (rij r12 = net onder de ogen, kolommen i15 = wang rechts van de mond, i23 = arm) -> 34x15 wordt 36x16 (x1,06 / y1,07).
# Daarna alleen de kop: egaal kopvlak, ogen op modelplek met glimp linksboven, rij lichaamsgroen (= de gedupliceerde
# rij), mond = D van het model 1-op-1 (natief x35-42, r12-16) met gesloten rand. A: binnenkant licht (model), B: Weepinbell.
from PIL import Image; import numpy as np
rows=[l.rstrip('\n') for l in open('sprite_r6/geest_schoon.txt')]; R0=6
DUPR=[12]; DUPC=[15,23]; DROPR=[21]; DX=14
g=[]
for r,line in enumerate(rows):
    if r+R0 in DROPR: continue
    row=[]
    for i,ch in enumerate(line):
        row.append(ch)
        if i in DUPC: row.append(ch)
    g.append(row)
    if r+R0 in DUPR: g.append(row[:])
im=Image.open('sprite_r6/sprite.png'); pal=im.getpalette(); r6=np.array(im)
IDX={'6':6,'5':5,'2':2,'W':13}; GROEN={2,3,4,5,6,13}
def X(i): return i+DX+sum(1 for d in DUPC if d<i)       # natieve kolom i -> spritekolom (eerste kopie)
def Yr(r): return r-R0+sum(1 for d in DUPR if d<r)
def maak(var):
    a=r6.copy()
    for y in range(0,15):
        for x in range(0,44):
            if a[y,x] in GROEN: a[y,x]=0                  # r6-geest weg
    for y,row in enumerate(g):
        for i,ch in enumerate(row):
            if ch in IDX: a[y,i+DX]=IDX[ch]
    a[14,15]=12 if a[14,15]==0 else a[14,15]               # schoorsteen-achterrand doorlopen (als r6)
    # onderkant (rij 15 = natief r20): lijn, en rechts omhoog gebogen zoals r6
    for x in range(16,40):
        if a[15,x] in (2,5): a[15,x]=6
    for x in range(X(12),X(17)+1): a[15,x]=0 if a[15,x] in GROEN else a[15,x]
    for x in range(X(12),X(17)): a[14,x]=6
    # --- kop ---
    M,D,L,K,W=5,6,2,1,13
    for y in range(Yr(9),Yr(17)+1):
        for x in range(X(6),X(14)+1): a[y,x]=M
    for (i0,i1) in ((7,9),(11,13)):                       # ogen: natief x36-38 en x40-42, r9-11
        for y in range(Yr(9),Yr(11)+1):
            for i in range(i0,i1+1): a[y,X(i)]=D
        a[Yr(9),X(i0)]=W
    yt=Yr(12)+1                                          # mond begint op de kopie van r12; origineel r12 = lichaamsrij
    rand=[(X(i),yt) for i in range(6,14)]+[(X(7),yt+k) for k in (1,2,3)]+[(X(13),yt+1),(X(13),yt+2),(X(12),yt+3)] \
        +[(X(i),yt+4) for i in range(7,12)]
    binnen=[(X(i),yt+1) for i in range(8,13)]+[(X(i),yt+2) for i in range(8,13)]+[(X(i),yt+3) for i in range(8,12)]
    rs=set(rand)
    for x,y in rand: a[y,x]=D
    for x,y in binnen:
        a[y,x]=L if var=='A' or any((x+dx,y+dy) in rs for dx,dy in((1,0),(-1,0),(0,1),(0,-1))) else K
    o=Image.fromarray(a.astype('uint8'),'P'); o.putpalette(pal); o.save('sprite_r7/sprite_%s.png'%var,transparency=0)
    Yg,Xg=np.mgrid[0:64,0:64]; geest=(Yg<=15)&(Xg<=52)
    print(var,'diff t.o.v. r6 buiten geestzone (y0-15, x<=52):',int(((a!=r6)&~geest).sum()))
    print('\n'.join('%2d '%y+''.join('.' if v==0 else '%X'%v for v in a[y,12:52]) for y in range(0,17)))
    return a
for v in 'AB': maak(v)
# metingen (natief model vs r7): breedtes in kolommen
nat={'kop (x29-46)':18,'arm (x47-59)':13,'mond (x36-42)':7,'oog l (x36-38)':3,'oog r (x40-42)':3,'geest hoog (r6-20)':15}
r7={'kop (x29-46)':X(17)-X(0)+1,'arm (x47-59)':X(30)-X(18)+1,'mond (x36-42)':X(13)-X(7)+1,'oog l (x36-38)':3,'oog r (x40-42)':3,'geest hoog (r6-20)':16}
for k in nat: print('%-20s natief %2d  r7 %2d  x%.2f'%(k,nat[k],r7[k],r7[k]/nat[k]))
for k in ('arm (x47-59)','mond (x36-42)','oog l (x36-38)'):
    print('verhouding %s/kop: natief %.2f  r7 %.2f'%(k,nat[k]/18,r7[k]/r7['kop (x29-46)']))
