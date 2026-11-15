# Hauntflare v5: laatste losse vlakjes uit v4 in hun buurtint (alleen herkleuren), vanaf ../sprite_v4/hauntflare_v4.png
# (22,54),(23,54) C: top van een vingerboog waarvan de rest van de oranje rand in v4 al B werd -> maakt geen rand af -> B
import json; from PIL import Image; import numpy as np
D='docs/concept/sprites/hauntflare/'; S=D+'sprite_v5/'
im=Image.open(D+'sprite_v4/hauntflare_v4.png'); PALF=im.getpalette()[:48]; o4=np.array(im).astype(int); out=o4.copy()
W=[((22,54),11),((23,54),11),((26,57),11),((52,19),11),((41,42),8),((42,42),8)]
LOG=[dict(x=x,y=y,oud=int(out[y,x]),nieuw=v) for (x,y),v in W]
for (x,y),v in W: out[y,x]=v
pim=Image.fromarray(out.astype('uint8'),'P'); pim.putpalette(PALF+[0]*(768-48)); pim.save(S+'hauntflare_v5.png',transparency=0)
P=np.array(PALF).reshape(-1,3); rgb=P[out].astype('uint8'); rgb[out==0]=255
Image.fromarray(rgb).resize((512,512),0).save(S+'hauntflare_v5_8x.png')
d=out!=o4; print('gewijzigd',int(d.sum()),'buiten lijst',[(int(x),int(y)) for y,x in zip(*np.where(d)) if (int(x),int(y)) not in [p for p,_ in W]]); json.dump(LOG,open(S+'v5_log.json','w'))
