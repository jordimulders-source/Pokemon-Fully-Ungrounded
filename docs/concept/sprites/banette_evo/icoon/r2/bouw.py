# reductie (npy, frontindexen) -> icoonframe in een gedeeld palet. Alleen: kolommen weglaten (kruisdelen),
# rijen schrappen, (optioneel arg 7: 'front:icoon'-uitzonderingen), kleur -> dichtstbijzijnde paletindex. Gebruik: python3 bouw.py red.npy x0 x1 'schraprijen' pal uit
import sys,numpy as np; from PIL import Image
R=np.load(sys.argv[1]); x0,x1=int(sys.argv[2]),int(sys.argv[3])
schrap=[int(v) for v in sys.argv[4].split(',') if v]; P=int(sys.argv[5]); UIT=sys.argv[6]
o=R[:,x0:x1+1].copy()
o=np.delete(o,schrap,axis=0)
fp=[(152,208,160),(24,24,32),(184,184,176),(144,144,136),(100,100,100),(120,184,216),(208,64,64),(144,40,48),(72,56,48),(240,216,128),(168,176,224),(128,132,184),(84,86,140),(150,156,186),(64,64,92),(240,112,100)]
L=[tuple(map(int,l.split())) for l in open('../../../../../../graphics/pokemon/icon_palettes/pal%d.pal'%P).read().split('\n')[3:19]]
def rd(a,b):
  r=(a[0]+b[0])/2; dr,dg,db=a[0]-b[0],a[1]-b[1],a[2]-b[2]
  return ((2+r/256)*dr*dr+4*dg*dg+(2+(255-r)/256)*db*db)**.5
m={0:0}
for i in range(1,16): m[i]=min(range(1,16),key=lambda j:rd(fp[i],L[j]))
for kv in (sys.argv[7].split(',') if len(sys.argv)>7 and sys.argv[7] else []):
    k,v=kv.split(':'); m[int(k)]=int(v)
q=np.vectorize(m.get)(o)
ys,xs=np.where(q>0); q=q[ys.min():ys.max()+1,xs.min():xs.max()+1]; h,w=q.shape
f=np.zeros((32,32),int); X=16-(w+1)//2; f[29-h:29,X:X+w]=q
np.save(UIT+'.npy',f)
im=Image.fromarray(f.astype('uint8'),'P'); im.putpalette([v for c in L for v in c]+[0]*(768-48)); im.save(UIT+'.png',transparency=0)
print(UIT,'b',w,'h',h,'map',m)
