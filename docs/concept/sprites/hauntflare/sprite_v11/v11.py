# v11 = v10 + tanden naar het patroon van Haunter G3 (alleen herkleuren):
#  rechter boventand = voet 3 breed in de liprij (29-31,33) + punt 1 px (30,34), zwart links/rechts van de punt (G3 tand (21-23,39)+(22,40));
#  linker ondertand = punt 1 px (24,37) met zwart ernaast + voet 3 breed (23-25,38) (G3 tand (23,43)+(20-23,44)).
from PIL import Image; import numpy as np, json
im=Image.open('sprite_v10/hauntflare_v10.png'); pal=im.getpalette(); a=np.array(im)
W={(31,33):7,(31,34):1,(30,35):10,(29,35):10,(23,38):7,(25,38):7}
log=[[x,y,int(a[y,x]),n] for (x,y),n in W.items()]
for (x,y),n in W.items(): a[y,x]=n
o=Image.fromarray(a,'P'); o.putpalette(pal); o.save('sprite_v11/hauntflare_v11.png',transparency=0); json.dump(log,open('sprite_v11/v11_log.json','w')); print(log)
def rgb(p):
    r=Image.open(p).convert('RGBA'); bg=Image.new('RGBA',r.size,(255,255,255,255)); bg.alpha_composite(r); return bg.convert('RGB')
t=rgb('sprite_v11/hauntflare_v11.png'); t.resize((512,512),Image.NEAREST).save('sprite_v11/hauntflare_v11_8x.png')
h=Image.open('../../../../graphics/pokemon/haunter/anim_front.png').convert('RGB').crop((0,0,64,64))
v=Image.new('RGB',(16*18*2+40,16*10+40+140),'white')
v.paste(t.crop((18,31,36,41)).resize((288,160),Image.NEAREST),(0,0)); v.paste(h.crop((14,37,32,47)).resize((288,160),Image.NEAREST),(308,0))
v.paste(t,(0,180)); v.paste(t.resize((128,128),Image.NEAREST),(80,180))
v.save('sprite_v11/vel_mond.png')
for y in range(31,41): print('%2d '%y+''.join('%x'%a[y,x] for x in range(18,36)))
