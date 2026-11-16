# r8 = r7-A (zelfde schaal: rij r12 en kolommen i15, i23 gedupliceerd door de hele geest), maar ogen+mond zijn
# letterlijk de pixels van het natieve model: geen gesloten rand, geen mondvlak. Opschoonregels van r6 (schoon.py)
# zonder de twee "mond dicht"-pixels (i7,r13) en (i13,r12): die blijven zoals het model (midden).
import sys; from PIL import Image; import numpy as np
q=[list(l.rstrip('\n')) for l in open('sprite_r6/geest_kwant.txt')]; R0=6
def s(i,r,c): q[r-R0][i]=c
for i,r,c in [(2,17,'5'),(3,19,'5'),(10,18,'5'),(17,20,'6')]: s(i,r,c)    # ruis buiten het gezicht (als r6)
H=len(q); Wd=len(q[0]); g0=[r[:] for r in q]
for y in range(H-1):                                                       # donkergroene buitenlijn (als r6)
    for x in range(Wd):
        if g0[y][x] in '52W' and any(not(0<=x+dx<Wd and 0<=y+dy<H) or g0[y+dy][x+dx]=='.' for dx,dy in((1,0),(-1,0),(0,1),(0,-1))):
            q[y][x]='6'
for i,r,c in [(33-29+29-29+4,2+6-6+0,'5')]: pass
DUPR=[12]; DUPC=[15,23]; DROPR=[21]; DX=14
g=[]
for r,line in enumerate(q):
    if r+R0 in DROPR: continue
    row=[]
    for i,ch in enumerate(line):
        row.append(ch)
        if i in DUPC: row.append(ch)
    g.append(row)
    if r+R0 in DUPR: g.append(row[:])
open('sprite_r8/geest_groot.txt','w').write('\n'.join(''.join(r) for r in g)+'\n')
im=Image.open('sprite_r6/sprite.png'); pal=im.getpalette(); r6=np.array(im)
IDX={'6':6,'5':5,'2':2,'W':13}; GROEN={2,3,4,5,6,13}
def X(i): return i+DX+sum(1 for d in DUPC if d<i)
a=r6.copy()
for y in range(0,15):
    for x in range(0,44):
        if a[y,x] in GROEN: a[y,x]=0
for y,row in enumerate(g):
    for i,ch in enumerate(row):
        if ch in IDX: a[y,i+DX]=IDX[ch]
if a[14,15]==0: a[14,15]=12
for x in range(16,40):
    if a[15,x] in (2,5): a[15,x]=6
for x in range(X(12),X(17)+1):
    if a[15,x] in GROEN: a[15,x]=0
for x in range(X(12),X(17)): a[14,x]=6
# losse ruispixels buiten ogen+mond (als r6 fix.py): pluim en linkerkwab
for (x,y,v) in [(X(4)+0,0,None)]: pass
o=Image.fromarray(a.astype('uint8'),'P'); o.putpalette(pal); o.save('sprite_r8/sprite.png',transparency=0)
r7=np.array(Image.open('sprite_r7/sprite_A.png'))
Yg,Xg=np.mgrid[0:64,0:64]; geest=(Yg<=15)&(Xg<=52)
print('diff t.o.v. r6/r7 buiten geestzone:',int(((a!=r6)&~geest).sum()),int(((a!=r7)&~geest).sum()))
print('diff t.o.v. r7-A binnen geest buiten kop (x<%d of x>%d):'%(X(6),X(14)),int(((a!=r7)&geest&((Xg<X(6))|(Xg>X(14)))).sum()))
for y in range(0,16): print('%2d '%y+''.join('.' if v==0 else '%X'%v for v in a[y,12:52]))
