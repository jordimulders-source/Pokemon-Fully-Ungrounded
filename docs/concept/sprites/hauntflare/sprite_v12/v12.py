# v12 = v11 met (31,33) terug naar lipzwart (Jordi: "haal de ingekleurde pixel tand weg", gemarkeerd op (31,33))
from PIL import Image; import numpy as np, json
im=Image.open('sprite_v11/hauntflare_v11.png'); pal=im.getpalette(); a=np.array(im)
print('oud',a[33,31]); a[33,31]=1
o=Image.fromarray(a,'P'); o.putpalette(pal); o.save('sprite_v12/hauntflare_v12.png',transparency=0)
r=Image.open('sprite_v12/hauntflare_v12.png').convert('RGBA'); bg=Image.new('RGBA',(64,64),(255,255,255,255)); bg.alpha_composite(r); bg=bg.convert('RGB')
bg.resize((512,512),Image.NEAREST).save('sprite_v12/hauntflare_v12_8x.png')
