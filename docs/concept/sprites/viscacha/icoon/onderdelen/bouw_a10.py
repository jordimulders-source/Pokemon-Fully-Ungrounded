import numpy as np; from PIL import Image
O='/home/user/Pokemon-Fully-Ungrounded/docs/concept/sprites/viscacha/icoon/onderdelen/'
B=Image.open(O+'icon_a9.png'); a=np.array(B); n=a.copy()
E={ # Jordi's krabbel over a9 frame 1 (krabbel_jordi_a9.png)
 (13,21):3,             # geel gestipt grijs pixel weg -> wordt borstlicht
 (14,22):14,(15,21):14, # zwart: armlijn langer, vanaf (14,23) schuin omhoog naar rechts
 (12,21):3,             # borst (links rood): wit in het midden, rand zand
 (16,22):3,(16,23):3,   # buik (rechts rood, tussen pootlijn en dij): wit midden
 (15,22):7,(15,23):7,(17,22):7,(17,23):7,(15,24):7,(16,24):7,  # rand zand
}
for (x,y),v in E.items():
    n[y,x]=v
    if y<=22: n[32+y+1,x]=v
    elif y>=24: n[32+y,x]=v
im=Image.fromarray(n,'P'); im.putpalette(B.getpalette()); im.save(O+'icon_a10.png',transparency=0)
im.resize((256,512),Image.NEAREST).save(O+'icon_a10_8x.png',transparency=0)
d=np.argwhere(n!=a); print('diff t.o.v. a9',len(d),[(int(x),int(y),int(a[y,x]),int(n[y,x])) for y,x in d])
for f in (0,32):
  for y in range(19,26): print('%2d '%y+''.join('.' if v==0 else '%X'%v for v in n[f+y][:24]))
