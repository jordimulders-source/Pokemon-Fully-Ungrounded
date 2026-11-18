# r11 = r10 + de 5 reparaties van keuring r10 (per pixel, door Claude).
from PIL import Image; import numpy as np
im=Image.open('../r10/banette_evo.png'); a=np.array(im); pal=im.getpalette()
set_=[]
for x in (18,19,20): set_.append((x,31,1))                   # 1 onderlijn linkeroog
for x in (20,21,22):
    for y in (32,33): set_.append((x,y,3))                    # 2 vlek onder linkeroog -> egaal grijs
for x,y in ((38,8),(41,11),(41,12)): set_.append((x,y,7))   # 3 doorlopende steek
set_+= [(8,37,1),(52,21,1)]                                   # 4 steel sleutelgat bellen
set_.append((56,53,1))                                        # 5 buitenlijn rechterpoppetje
set_+= [(x,y,6) for x,y in ((33,15),(33,16),(32,16),(30,17),(31,17),(32,17),(31,18))]  # o1 glansvlek kleiner (Claude)
for x,y,v in set_: a[y,x]=v
out=Image.fromarray(a.astype('uint8'),'P'); out.putpalette(pal)
out.save('banette_evo.png',transparency=0); print(len(set_),'px')
