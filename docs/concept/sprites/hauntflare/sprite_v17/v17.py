# v17 = v16 + (31,32) zwart -> hoofdroze 8 (Jordi gele stip): de rechter boventand zit weer vast aan het hoofd
from PIL import Image; import numpy as np
im=Image.open('sprite_v16/hauntflare_v16.png'); pal=im.getpalette(); a=np.array(im); print('oud',a[32,31]); a[32,31]=8
o=Image.fromarray(a,'P'); o.putpalette(pal); o.save('sprite_v17/hauntflare_v17.png',transparency=0)
r=Image.open('sprite_v17/hauntflare_v17.png').convert('RGBA'); bg=Image.new('RGBA',(64,64),(255,255,255,255)); bg.alpha_composite(r); bg=bg.convert('RGB')
bg.resize((512,512),Image.NEAREST).save('sprite_v17/hauntflare_v17_8x.png')
dk=Image.new('RGBA',(64,64),(40,40,48,255)); dk.alpha_composite(r)
v=Image.new('RGB',(160+500,200),'white'); v.paste(bg,(10,10)); v.paste(dk.convert('RGB'),(80,10)); v.paste(bg.crop((18,29,38,39)).resize((480,240),Image.NEAREST).crop((0,0,480,190)),(170,5)); v.save('sprite_v17/mond.png')
