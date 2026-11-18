import numpy as np, sys; from PIL import Image
O='/home/user/Pokemon-Fully-Ungrounded/docs/concept/sprites/viscacha/icoon/onderdelen/'
B=Image.open(O+'icon_a7.png'); a=np.array(B); n=a.copy()
L1=[(12,19),(13,19),(14,20),(15,20),(16,21)]          # vlak, als de bovenste in de front
L2=[(12,20),(13,21),(14,22),(15,22),(16,23)]          # steiler, als de onderste
for x,y in L1+L2: n[y,x]=14; n[32+y+1,x]=14
im=Image.fromarray(n,'P'); im.putpalette(B.getpalette()); im.save(O+'icon_a8.png',transparency=0)
im.resize((256,512),Image.NEAREST).save(O+'icon_a8_8x.png',transparency=0)
d=np.argwhere(n!=a); print('diff t.o.v. a7',len(d),[(int(x),int(y)) for y,x in d])
