import numpy as np; from PIL import Image
O='/home/user/Pokemon-Fully-Ungrounded/docs/concept/sprites/viscacha/icoon/onderdelen/'
B=Image.open(O+'icon_a11.png'); a=np.array(B); n=a.copy()
E={
 # 1. buik (wit omlijnd) = buikkleur zoals in a9/a10, geen wit
 (12,22):7,(13,22):7,(12,23):7,(13,23):6,
 (15,22):7,(16,22):7,(17,22):7,(15,23):7,(16,23):7,(17,23):7,(15,24):7,(16,24):7,(17,24):6,
 # 2. de 2 witte pixels met bruine krabbel (in a10 wit, in a11 zand) -> bruin
 (12,21):6,(13,21):6,
 # 3. linkerarm (zwarte lijn (9,22)-(8,23)) 1 px dunner aan de buitenkant, omlijning dicht
 (7,22):0,(8,22):14,(6,23):0,(7,23):14,(7,24):0,
 # 4. dijlijn boven het been: bruin in plaats van donker
 (19,20):6,(19,21):6,(18,22):6,(18,23):6,
}
for (x,y),v in E.items():
    n[y,x]=v
    if y<=22 or (x<=10 and y<=24): n[32+y+1,x]=v   # wantje zakt in frame 2 helemaal mee
    elif y>=24: n[32+y,x]=v
im=Image.fromarray(n,'P'); im.putpalette(B.getpalette()); im.save(O+'icon_a12.png',transparency=0)
im.resize((256,512),Image.NEAREST).save(O+'icon_a12_8x.png',transparency=0)
d=np.argwhere(n!=a); print('diff t.o.v. a11',len(d))
print('wit over:',[(int(x),int(y)) for y,x in np.argwhere(n==3)])
for f in (0,32):
  for y in range(19,27): print('%2d '%y+''.join('.' if v==0 else '%X'%v for v in n[f+y][:26]))
