# v6 = v5 + MOET 1-3 en MAG-punten uit de eindkeuring van v5 (alleen herkleuren op indexniveau)
from PIL import Image; import numpy as np, json
im=Image.open('sprite_v5/hauntflare_v5.png'); pal=im.getpalette(); a=np.array(im)
W={}  # (x,y): nieuwe index
for p in [(25,34),(24,35)]: W[p]=1                                   # MOET 1
W[(15,27)]=8                                                          # MOET 2
for p in [(30,18),(28,19),(29,19),(27,20)]: W[p]=8                    # MOET 3
for p in [(28,20),(29,20),(37,18)]: W[p]=7
for p in [(30,23),(31,24),(32,24)]: W[p]=8                            # MAG glansspikkel
for p in [(39,32),(38,33),(38,34),(37,35),(35,36),(36,36),(33,37),(34,37)]: W[p]=1   # MAG mondlijn zwart
W[(11,34)]=2                                                          # MAG dubbel zwart
for p in [(58,39),(59,39),(61,39),(60,40)]: W[p]=12                   # MAG hand rechts
log=[]
for (x,y),n in W.items(): log.append([x,y,int(a[y,x]),n]); a[y,x]=n
A=Image.fromarray(a.astype('uint8'),'P'); A.putpalette(pal); A.save('sprite_v6/hauntflare_v6.png',transparency=0)
json.dump(log,open('sprite_v6/v6_log.json','w'))
A=Image.open('sprite_v6/hauntflare_v6.png').convert('RGBA'); bg=Image.new('RGBA',(64,64),(255,255,255,255)); bg.alpha_composite(A)
bg.convert('RGB').resize((512,512),Image.NEAREST).save('sprite_v6/hauntflare_v6_8x.png')
print(len(log),'px', [l for l in log if l[2]==l[3]])
