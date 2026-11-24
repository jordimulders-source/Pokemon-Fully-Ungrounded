# Palet inkorten tot de gebruikte kleuren (index 0 transparant), volgorde: omlijning, lijf, paars, paneel, iris
import numpy as np, sys; from PIL import Image
im=Image.open(sys.argv[1]); o=np.array(im); pal=np.array(im.getpalette()[:48]).reshape(16,3)
volg=[1,2,3,4,5,6,7,8,9,10,15,11,12,13,14]
used=[v for v in volg if (o==v).any()]
m={0:0}; [m.__setitem__(v,n+1) for n,v in enumerate(used)]
o2=np.vectorize(m.get)(o).astype('uint8'); P=[(255,0,255)]+[tuple(pal[v]) for v in used]
out=Image.fromarray(o2,'P'); out.putpalette([c for p in P for c in p]+[0]*(768-3*len(P))); out.save(sys.argv[2],transparency=0)
print('kleuren incl. transparant:',len(P)); [print(n,'#%02x%02x%02x'%p) for n,p in enumerate(P)]
