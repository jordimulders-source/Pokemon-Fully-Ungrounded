# Past de MOET-lijst toe op r8 (assert op oude index); schrijft sim_moet_sprite.png (zelfde palet, index 0 transparant).
import numpy as np;from PIL import Image
im=Image.open('../af/pitahaya_draak.png');a=np.array(im).copy()
MOET=[(26,37,1,8),(29,37,1,8),(32,37,1,8)]
for x,y,o,n in MOET: assert a[y,x]==o,(x,y,a[y,x]); a[y,x]=n
out=Image.fromarray(a.astype(np.uint8),'P');out.putpalette(im.getpalette());out.save('sim_moet_sprite.png',transparency=0)
r=np.array(im);print('gewijzigd',int((r!=a).sum()),'px; silhouet-diff',int(((r>0)!=(a>0)).sum()),'; gezicht x18-36 y22-34 diff',int((r[22:35,18:37]!=a[22:35,18:37]).sum()))
