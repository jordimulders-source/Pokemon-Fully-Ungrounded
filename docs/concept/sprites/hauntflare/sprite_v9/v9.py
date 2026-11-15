# v9 = kandidaat_T2 + MOET keuring T2: onderlip dicht bij x26 (alleen herkleuren)
from PIL import Image; import numpy as np, json
im=Image.open('sprite_v8b/kandidaat_T2.png'); pal=im.getpalette(); a=np.array(im)
W={(26,38):1,(26,39):7}; log=[[x,y,int(a[y,x]),n] for (x,y),n in W.items()]
for (x,y),n in W.items(): a[y,x]=n
o=Image.fromarray(a,'P'); o.putpalette(pal); o.save('sprite_v9/hauntflare_v9.png',transparency=0); json.dump(log,open('sprite_v9/v9_log.json','w')); print(log)
r=Image.open('sprite_v9/hauntflare_v9.png').convert('RGBA'); bg=Image.new('RGBA',(64,64),(255,255,255,255)); bg.alpha_composite(r); bg=bg.convert('RGB')
bg.resize((512,512),Image.NEAREST).save('sprite_v9/hauntflare_v9_8x.png')
v=Image.new('RGB',(512+20+360,512),'white'); v.paste(bg.resize((512,512),Image.NEAREST),(0,0)); v.paste(bg.crop((14,18,44,42)).resize((360,288),Image.NEAREST),(532,0)); v.paste(bg,(532,310)); v.paste(bg.resize((128,128),Image.NEAREST),(620,310)); v.save('sprite_v9/hauntflare_v9_toon.png')
