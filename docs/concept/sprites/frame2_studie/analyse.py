import glob,os,numpy as np
from PIL import Image
res=[]
for p in sorted(glob.glob('graphics/pokemon/*/anim_front_gba.png')):
    im=np.array(Image.open(p))
    if im.shape!=(128,64): continue
    a,b=im[:64],im[64:]
    A=a!=0;B=b!=0
    n=(A|B).sum()
    if n==0 or not B.any() or not A.any(): continue
    same=((a==b)&(A|B)).sum()/n  # identiek op zelfde plek
    # lokaal verschoven: pixel in b komt overeen met a binnen ±R, per 4x4 blok beste offset
    R=4; expl=np.zeros_like(B)
    pa=np.pad(a,R,constant_values=0)
    for y in range(0,64,4):
        for x in range(0,64,4):
            blk=b[y:y+4,x:x+4]
            if not (blk!=0).any() and not (a[y:y+4,x:x+4]!=0).any(): continue
            best=None
            for dy in range(-R,R+1):
                for dx in range(-R,R+1):
                    s=pa[y+R+dy:y+R+dy+4,x+R+dx:x+R+dx+4]
                    m=(s==blk)
                    sc=m.sum()
                    if best is None or sc>best[0]: best=(sc,m)
            expl[y:y+4,x:x+4]=best[1]
    new=((~expl)&B).sum()/max(B.sum(),1)
    ys=np.where(A.any(1))[0]; yb=np.where(B.any(1))[0]
    res.append((os.path.basename(os.path.dirname(p)),same,new,ys.max()-yb.max()))
res.sort(key=lambda r:r[2])
import statistics as st
news=[r[2] for r in res]; sames=[r[1] for r in res]
print(len(res),'identiek mediaan %.2f'%st.median(sames),'nieuw mediaan %.3f'%st.median(news))
for q in (10,25,50,75,90): print(q, '%.3f'%np.percentile(news,q))
print('klasse <5%',sum(n<.05 for n in news),'5-15%',sum(.05<=n<.15 for n in news),'15-30%',sum(.15<=n<.3 for n in news),'>30%',sum(n>=.3 for n in news))
print('voeten zelfde rij',sum(r[3]==0 for r in res))
print('laag:',[ (r[0],round(r[2],2)) for r in res[:12]])
print('hoog:',[ (r[0],round(r[2],2)) for r in res[-15:]])
import json; json.dump([(r[0],float(r[1]),float(r[2]),int(r[3])) for r in res],open(os.environ['OUT']+'/res.json','w'))
