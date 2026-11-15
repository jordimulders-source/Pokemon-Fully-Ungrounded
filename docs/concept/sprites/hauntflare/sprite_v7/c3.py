# C3 = C2 + herkeuring: zwarte muur midden in de mond weg (alleen herkleuren)
from PIL import Image; import numpy as np, json
im=Image.open('sprite_v7/kandidaat_C2.png'); pal=im.getpalette(); a=np.array(im)
W={(26,34):10,(27,34):10,(26,35):5,(25,36):5,(26,36):5}
log=[[x,y,int(a[y,x]),n] for (x,y),n in W.items()]
for (x,y),n in W.items(): a[y,x]=n
o=Image.fromarray(a,'P'); o.putpalette(pal); o.save('sprite_v7/kandidaat_C3.png',transparency=0)
json.dump(log,open('sprite_v7/c3_log.json','w')); print(log)
r=Image.open('sprite_v7/kandidaat_C3.png').convert('RGBA'); bg=Image.new('RGBA',(64,64),(255,255,255,255)); bg.alpha_composite(r)
bg=bg.convert('RGB'); v=Image.new('RGB',(64*6+30*12+20,64*6),'white'); v.paste(bg.resize((384,384),Image.NEAREST),(0,0)); v.paste(bg.crop((14,18,44,42)).resize((360,288),Image.NEAREST),(400,0)); v.paste(bg,(400,300)); v.save('sprite_v7/vel_c3.png')
