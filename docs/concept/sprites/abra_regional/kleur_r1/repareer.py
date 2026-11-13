# onderlaag.png (half2.py, offset oy=0 ox=1) -> abra_r1.png. Alleen Gen 3-reparaties, elke pixel gelogd.
# Regel: lichte tint (index >= 8, helderheid >= 161) op de buitenrand -> omlijning (index 1); Gen 3: geen lichte kleur op de buitenrand.
# Middentinten op de rand (bovenkant staart, waar het model zelf een gekleurde rand heeft) blijven: gekleurde selout aan de lichtkant.
from PIL import Image; import numpy as np
im=Image.open('onderlaag.png'); a=np.array(im); pal=im.getpalette()
b=a.copy(); p=np.pad(a,1); log=[]
for y,x in zip(*np.where(a>=8)):
    if 0 in (p[y,x+1],p[y+2,x+1],p[y+1,x],p[y+1,x+2]):
        b[y,x]=1; log.append((int(x),int(y),int(a[y,x]),1,'lichte tint op de buitenrand -> omlijning'))
# gesloten ogen: in het model 1-px streepjes die door de 2x2-reductie half wegvallen (elk blok bevat maar 1 zwarte modelpixel)
# rechteroog model = natief (42,59)(43,58)(44,56)(45,56)(46,55) -> spriteblokken (28,29)(29,28)(30,28); (29,28) stond er al
# linkeroog model = natief (47,44)(47,45) -> spriteblok (30,22) (werd donkergrijs 2)
for (y,x) in ((28,29),(30,28),(30,22)):
    log.append((x,y,int(b[y,x]),1,'gesloten oog: modellijn terug die de reductie liet wegvallen')); b[y,x]=1
o=Image.fromarray(b.astype('uint8'),'P'); o.putpalette(pal); o.save('abra_r1.png',transparency=0)
for r in log: print('x=%d y=%d: %d -> %d (%s)'%r)
print(len(log),'pixels; kleuren',len(set(b.ravel()))-1,'; px',(b>0).sum())
