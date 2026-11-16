# r3 = r2, maar ventje buiten het gezicht (rij 10-17, x31-47 lokaal) via de gladde toonkaart (sigma 0,6, modellijnen
# L<70 blijven donkerste groen), zoals de yerba. Les mate fase 1: "het groen is gewoon een groene blur" -> plukjes.
from PIL import Image; import numpy as np, subprocess
D='docs/concept/sprites/mate_fase2/sprite/'
subprocess.run(['python3',D+'r3/bouw3.py'],check=True,capture_output=True)
r2=Image.open(D+'r2/mate2.png'); a=np.asarray(r2).astype(int); v=np.asarray(Image.open(D+'r3/variant_ruw.png')).astype(int)
VENT=np.load(D+'r3/vent.npy'); H,W=VENT.shape; oy=64-H-1; ox=(64-W)//2
yy,xx=np.mgrid[0:H,0:W]; FACE=(yy>=10)&(yy<=17)&(xx>=31)&(xx<=47)
z=np.zeros((64,64),bool); z[oy:oy+H,ox:ox+W]=VENT&~FACE
z&=(a>=6)&(a<=9)&(v>=6)&(v<=9)   # alleen groen->groen
s=a.copy(); s[z]=v[z]
assert (s[~z]==a[~z]).all()
print('ventje-pixels gewijzigd t.o.v. r2:',(s!=a).sum())
o=Image.fromarray(s.astype('uint8'),'P'); o.putpalette(r2.getpalette()); o.save(D+'r3/mate2.png',transparency=0)
