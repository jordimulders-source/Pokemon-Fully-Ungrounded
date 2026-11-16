# r22 = r21 + zwarte vlakken uit het model: spritepixel in de koeienvanger -> zwart (1) waar >= FR van de voetafdruk
# zeer donkere modelpixels heeft (lum < THR, niet groen/wit). Groen, transparant en alles buiten KV: diff 0 (assert).
# Gebruik: maak.py THR FR [uit.png]
import sys; sys.path.insert(0,'/home/user/Pokemon-Fully-Ungrounded/docs/concept/sprites/spooktrein_fase3/sprite_r18')
from kv import *
from collections import Counter
THR=float(sys.argv[1]) if len(sys.argv)>1 else 60; FR=float(sys.argv[2]) if len(sys.argv)>2 else 0.4
UIT=sys.argv[3] if len(sys.argv)>3 else D+'sprite_r22/sprite.png'
im=Image.open(D+'sprite_r21/sprite.png'); r=np.array(im).astype(int); pal=im.getpalette()
GRS=[2,3,4,5,6,13]; groen=np.isin(r,GRS)
KV=np.zeros((64,64),bool); KV[45:61,0:27]=True
DK=(LUM<THR)&~G&~WIT
def fdk(x,y):
    f=list(foot(x,y)); W=sum(w for w,_,_ in f); return sum(w for w,ny,nx in f if DK[ny,nx])/W
# band boven de V (roest tussen grijns en V) laten zoals r21; daar bepaalt de V-lijn de vorm
vcells=[c for c in dun(raster(V)) if KV[c]]; vmin={}
for (y,x) in vcells: vmin[x]=min(vmin.get(x,99),y)
band=np.zeros((64,64),bool)
for x,v in vmin.items(): band[:v,x]=True
rnd=np.array([[r[y,x]!=0 and (x==0 or 0 in nb4(r,y,x)) for x in range(64)] for y in range(64)])
zone=KV&np.isin(r,[7,8,9,10,11,12])&~band&~rnd     # selout aan de buitenrand blijft
MZ=np.zeros((64,64),bool)          # zwartkaart model
for y in range(45,61):
    for x in range(27):
        if r[y,x]!=0 and not groen[y,x]: MZ[y,x]=fdk(x,y)>=FR
a=r.copy()
for y,x in zip(*np.where(zone&MZ)): a[y,x]=1
# eilandjes van 1-2 px in de vulling die door het zwart ontstaan -> zwart als het model daar >=25% donker heeft, anders buurtint
def comp8(a,y,x):
    v=a[y,x]; st=[(y,x)]; c={(y,x)}
    while st:
        yy,xx=st.pop()
        for dy in(-1,0,1):
            for dx in(-1,0,1):
                q=(yy+dy,xx+dx)
                if ok(*q) and q not in c and a[q]==v: c.add(q); st.append(q)
    return c
for it in range(3):
    for y,x in zip(*np.where(zone&(a!=1))):
        c=comp8(a,y,x)
        if len(c)<3 and all(zone[q] for q in c):
            if a[y,x]==7 and any(a[q[0]+dy,q[1]+dx] in (10,11) for q in c for dy in(-1,0,1) for dx in(-1,0,1)): continue  # glans
            if np.mean([fdk(q[1],q[0]) for q in c])>=0.25:
                for q in c: a[q]=1
            else:
                n=Counter(a[q[0]+dy,q[1]+dx] for q in c for dy in(-1,0,1) for dx in(-1,0,1)
                          if ok(q[0]+dy,q[1]+dx) and (q[0]+dy,q[1]+dx) not in c and a[q[0]+dy,q[1]+dx] in (7,8,9,10,11,12))
                if n:
                    for q in c: a[q]=n.most_common(1)[0][0]
assert (a[groen]==r[groen]).all() and not np.isin(a[~groen],GRS).any(),'groen gewijzigd'
assert (a[~KV]==r[~KV]).all(),'buiten koeienvanger gewijzigd'
assert ((a==0)==(r==0)).all(),'silhouet gewijzigd'
if __name__=='__main__':
    d=a!=r
    print('THR',THR,'FR',FR,'gewijzigd',int(d.sum()),'buiten KV',int(d[~KV].sum()),'groen-diff',int(d[groen].sum()),'zwart erbij',int(((a==1)&(r!=1)).sum()))
    for y in range(44,60): print('%2d'%y,''.join('.' if q==0 else '%X'%q for q in a[y,:28]),' ',''.join('#' if MZ[y,x] else '.' for x in range(28)))
    o=Image.fromarray(a.astype(np.uint8),'P'); o.putpalette(pal); o.save(UIT,transparency=0)
    np.save(UIT.replace('.png','_mz.npy'),MZ)
