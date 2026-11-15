# v18 = v17 + eindkeuring MOET: rand bol/kuif dicht ((34,16),(35,17) -> 5 selout, (36,17) -> 1 zwart)
from PIL import Image; import numpy as np, json
im=Image.open('sprite_v17/hauntflare_v17.png'); pal=im.getpalette(); a=np.array(im)
W={(34,16):5,(35,17):5,(36,17):1}; log=[[x,y,int(a[y,x]),n] for (x,y),n in W.items()]
for (x,y),n in W.items(): a[y,x]=n
o=Image.fromarray(a,'P'); o.putpalette(pal); o.save('sprite_v18/hauntflare_v18.png',transparency=0); json.dump(log,open('sprite_v18/v18_log.json','w')); print(log)
r=Image.open('sprite_v18/hauntflare_v18.png').convert('RGBA'); bg=Image.new('RGBA',(64,64),(255,255,255,255)); bg.alpha_composite(r); bg.convert('RGB').resize((512,512),Image.NEAREST).save('sprite_v18/hauntflare_v18_8x.png')
