# r2 = r1 + gerichte reparaties (alle andere pixels identiek aan r1, met assert bewezen)
# 1. twee grijze/witte anti-alias-pixels naast de bladkop van het ventje (geen modelvorm, Gemini-randruis) -> transparant
# 2. verre kano-oog (natief x19-22, y58-62): kale reductie van het model (dichtstbijzijnde paletkleur) i.p.v. de gladde toonkaart
from PIL import Image; import numpy as np
D='docs/concept/sprites/mate_fase2/sprite/'
im=Image.open(D+'r1/mate2.png'); s=np.asarray(im).astype(int).copy(); pal=np.array(im.getpalette()[:45]).reshape(15,3)
g=np.asarray(Image.open(D+'r1/geschrapt.png').convert('RGB')).astype(int); H,W,_=g.shape; oy=64-H-1; ox=(64-W)//2
r1=s.copy(); zone=np.zeros((64,64),bool)
for (x,y) in [(35,3),(47,3)]:
    zone[y+oy,x+ox]=True; s[y+oy,x+ox]=0
for y in range(28,34):
    for x in range(3,8):
        if s[y+oy,x+ox]==0: continue
        zone[y+oy,x+ox]=True
        s[y+oy,x+ox]=int(np.abs(pal[1:]-g[y,x]).sum(1).argmin())+1
assert (s[~zone]==r1[~zone]).all()
print('gewijzigd:',[(x-ox,y-oy,r1[y,x],s[y,x]) for y,x in zip(*np.where(s!=r1))])
o=Image.fromarray(s.astype('uint8'),'P'); o.putpalette(im.getpalette()); o.save(D+'r2/mate2.png',transparency=0)
