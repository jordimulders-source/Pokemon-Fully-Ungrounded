import numpy as np, sys; from PIL import Image
O='/home/user/Pokemon-Fully-Ungrounded/docs/concept/sprites/viscacha/icoon/onderdelen/'
B=Image.open(O+'icon_a5b.png'); a=np.array(B); n=a.copy()
E={
 # oog 1 px naar rechts (vorm gelijk)
 (9,16):7,(10,16):15,(11,16):3,(9,17):7,(10,17):15,(11,17):15,
 # kraag "<" 1 px mee naar rechts
 (12,16):7,(13,16):9,(14,16):9,(14,15):7,(15,15):9,
 (12,17):8,(12,18):7,(13,18):8,(14,18):8,(14,19):6,(15,19):8,
 # snuit langer naar linksonder, kin 1 rij lager
 (6,18):7,(6,19):7,(7,20):6,(8,20):6,(9,20):6,(7,21):14,(9,19):7,(10,19):7,
}
for (x,y),v in E.items(): n[y,x]=v; n[32+y+1,x]=v
im=Image.fromarray(n,'P'); im.putpalette(B.getpalette()); im.save(sys.argv[1],transparency=0)
im.resize((256,512),Image.NEAREST).save(sys.argv[1].replace('.png','_8x.png'),transparency=0)
d=np.argwhere(n!=a); print('diff t.o.v. a5b',len(d))
for y in range(12,24): print('%2d '%y+''.join('.' if v==0 else '%X'%v for v in n[y][:22]))
