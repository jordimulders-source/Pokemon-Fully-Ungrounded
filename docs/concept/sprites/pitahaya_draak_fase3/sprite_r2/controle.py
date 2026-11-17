# Controles: kleuren, dambord (2x2 om-en-om van twee vultinten), losse vulpixels, witte pixels buiten oog/bek,
# zwart binnen de figuur, zwart in de buitenrand, langste rechte stuk van de buitenrand (horizontaal/verticaal).
import sys,numpy as np; from PIL import Image
o=np.asarray(Image.open(sys.argv[1])).astype(int)
fig=o>0; p=np.pad(fig,1); rand=fig&~(p[:-2,1:-1]&p[2:,1:-1]&p[1:-1,:-2]&p[1:-1,2:])
tot=fig.sum()
print('kleuren incl. transparant',len(set(o.ravel())),'| px',tot,'| breed',np.ptp(np.where(fig)[1])+1,'hoog',np.ptp(np.where(fig)[0])+1)
print('zwart binnen %.1f%%'%(100*((o==1)&~rand).sum()/tot),'| buitenrand zwart %.0f%%'%(100*((o==1)&rand).sum()/rand.sum()))
VUL=set(range(2,16))-{2,6,12}
db=[]
for y in range(63):
    for x in range(63):
        q=o[y:y+2,x:x+2]
        if q[0,0]==q[1,1] and q[0,1]==q[1,0] and q[0,0]!=q[0,1] and q[0,0] in VUL and q[0,1] in VUL: db.append((x,y))
print('dambord',len(db),db[:12])
los=[]
for y,x in zip(*np.where(fig)):
    v=o[y,x]
    if v in (1,): 
        nb=[o[y+dy,x+dx] for dy in (-1,0,1) for dx in (-1,0,1) if (dy or dx)]
        if not any(n in (1,2,6) for n in nb) and 0 not in nb: los.append(('zwart',x,y))
        continue
    nb=[o[y+dy,x+dx] for dy in (-1,0,1) for dx in (-1,0,1) if (dy or dx)]
    if v not in nb and v in VUL: los.append((v,x,y))
print('losse pixels',len(los),los[:20])
wit=[(x,y) for y,x in zip(*np.where((o==10)|(o==11))) if not (8<=x<=14 and 20<=y<=33)]
print('wit buiten oog/bek',wit)
best=(0,None)
for y in range(64):
    run=0
    for x in range(64):
        e=rand[y,x] and (y==0 or not fig[y-1,x] or y==63 or not fig[y+1,x])
        run=run+1 if e else 0
        if run>best[0]: best=(run,('rij',y,x-run+1,x))
for x in range(64):
    run=0
    for y in range(64):
        e=rand[y,x] and (x==0 or not fig[y,x-1] or x==63 or not fig[y,x+1])
        run=run+1 if e else 0
        if run>best[0]: best=(run,('kolom',x,y-run+1,y))
print('langste rechte randstuk',best)
