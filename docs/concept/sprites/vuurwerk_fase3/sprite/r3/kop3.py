# r3: alleen kop + gezicht, op r2_basis.npy (lijf, lijnen, pijl, twinkels, lijfspikkels bevroren).
#  2. kopvulling: binnenpixels van de kop roze vlam (7) waar de lijnkaart (lijnkaart.py) een modelstreep heeft, anders creme
#     (r2-tint, of bij een r2-roze pixel zonder streep de creme naar de modelhelderheid).
#  3. koprand linksboven (x<20, y<19): creme randpixels -> 1 px selout donker goud/tan 14 (gemeten modelrand [176,141,91]).
#  1. gezicht: variant V (standaard) en W, per pixel gemeten (dark%-tabel en overlay op 36x, zie rapport).
import sys, json, numpy as np; from PIL import Image
PAL=json.load(open('palet_r2.json'))
a0=np.load('r2_basis.npy'); a=a0.copy(); H,W=a.shape
roze=np.load('kaart_roze.npy'); RZ=int(sys.argv[1]) if len(sys.argv)>1 else 2   # min. natieve streeppixels per spritepixel
m=np.asarray(Image.open('../../referenties/model_v14.png').convert('RGB')).astype(float)@[0.299,0.587,0.114]
def med(x,y): return np.median(m[120+y*12:132+y*12,106+x*12:118+x*12])
def creme(x,y):
    L=med(x,y); return 3 if L<205 else (4 if L<226 else 5)
Y,X=np.mgrid[:64,:64]; KZ=(X<26)&(Y<31)&~((X>=22)&(Y>=24))
TW=set()
for cx,cy in [(8,6),(5,9),(29,18),(20,26),(16,29)]:
    for dx,dy in ((0,0),(1,0),(-1,0),(0,1),(0,-1)): TW.add((cx+dx,cy+dy))
# kop = deel van het grote lijf binnen KZ
def comp(mask,start):
    seen={start}; st=[start]
    while st:
        y,x=st.pop()
        for dy in (-1,0,1):
            for dx in (-1,0,1):
                q=(y+dy,x+dx)
                if 0<=q[0]<H and 0<=q[1]<W and mask[q] and q not in seen: seen.add(q); st.append(q)
    return seen
lijf=comp(a0>0,(20,40)); kop={p for p in lijf if KZ[p] and (p[1],p[0]) not in TW}
def rand(y,x): return any(not(0<=y+dy<H and 0<=x+dx<W) or a0[y+dy,x+dx]==0 for dy,dx in ((1,0),(-1,0),(0,1),(0,-1)))
FACE=lambda x,y: 5<=x<=17 and 15<=y<=26
for (y,x) in kop:
    v=a0[y,x]
    if rand(y,x):
        if x<20 and y<19 and v in (3,4,5): a[y,x]=14
        continue
    if FACE(x,y) and x<=17 and y>=18: continue
    if v in (3,4,5,7):
        if roze[y,x]>=RZ: a[y,x]=7
        elif v==7: a[y,x]=creme(x,y)
GEZ=json.load(open('gezicht_r3.json'))
for naam,g in GEZ.items():
    b=a.copy()
    for (y,x) in kop:
        if not(6<=x<=17 and 15<=y<=26) or rand(y,x): continue
        k='%d,%d'%(x,y)
        b[y,x]=g['px'][k] if k in g['px'] else creme(x,y)
    np.save('r3_kop_%s.npy'%naam,b)
    print(naam,'kop+gezicht t.o.v. r2:',int((b!=a0).sum()),'px')
