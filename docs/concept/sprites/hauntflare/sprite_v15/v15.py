# v15 = v14 + herkeuring: 6 px terug naar zwart (om-en-om opgelost), (61,41) -> 11 (MAG)
from PIL import Image; import numpy as np, json
im=Image.open('sprite_v14/hauntflare_v14.png'); pal=im.getpalette(); a=np.array(im)
W={p:1 for p in [(54,42),(57,42),(59,42),(60,42),(12,61),(18,60)]}; W[(61,41)]=11
log=[[x,y,int(a[y,x]),n] for (x,y),n in W.items()]
for (x,y),n in W.items(): a[y,x]=n
o=Image.fromarray(a,'P'); o.putpalette(pal); o.save('sprite_v15/hauntflare_v15.png',transparency=0); json.dump(log,open('sprite_v15/v15_log.json','w')); print(log)
r=Image.open('sprite_v15/hauntflare_v15.png').convert('RGBA'); bg=Image.new('RGBA',(64,64),(255,255,255,255)); bg.alpha_composite(r); bg=bg.convert('RGB')
bg.resize((512,512),Image.NEAREST).save('sprite_v15/hauntflare_v15_8x.png')
v=Image.new('RGB',(512+20+300,512),'white'); v.paste(bg.resize((512,512),Image.NEAREST),(0,0)); v.paste(bg,(532,0)); v.paste(bg.resize((128,128),Image.NEAREST),(620,0))
dk=Image.new('RGBA',(64,64),(40,40,48,255)); dk.alpha_composite(r); v.paste(dk.convert('RGB'),(532,150)); v.paste(dk.convert('RGB').resize((128,128),Image.NEAREST),(620,150)); v.save('sprite_v15/hauntflare_v15_toon.png')
