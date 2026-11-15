# v14 = v13 + eindkeuring: MOET 1-3 (7 px -> 10) en MAG vingerstompjes (4 px -> 10), ringlijn lichtkant (4 px -> 2). Alleen herkleuren.
from PIL import Image; import numpy as np, json
im=Image.open('sprite_v13/hauntflare_v13.png'); pal=im.getpalette(); a=np.array(im)
W={}
for p in [(13,53),(59,38),(60,39),(61,40),(61,41),(12,61),(18,60)]: W[p]=10
for p in [(54,42),(57,42),(59,42),(60,42)]: W[p]=10
for p in [(5,34),(4,35),(3,36),(2,37)]: W[p]=2
log=[[x,y,int(a[y,x]),n] for (x,y),n in W.items()]
for (x,y),n in W.items(): a[y,x]=n
o=Image.fromarray(a,'P'); o.putpalette(pal); o.save('sprite_v14/hauntflare_v14.png',transparency=0); json.dump(log,open('sprite_v14/v14_log.json','w')); print(log)
r=Image.open('sprite_v14/hauntflare_v14.png').convert('RGBA'); bg=Image.new('RGBA',(64,64),(255,255,255,255)); bg.alpha_composite(r); bg=bg.convert('RGB')
bg.resize((512,512),Image.NEAREST).save('sprite_v14/hauntflare_v14_8x.png')
