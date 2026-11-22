import numpy as np; from PIL import Image
O='/home/user/Pokemon-Fully-Ungrounded/docs/concept/sprites/viscacha/icoon/onderdelen/'
B=Image.open(O+'icon_a10.png'); a=np.array(B); n=a.copy()
E={(13,21):7,(12,21):7}   # gestipte pixel weg = huid; ook het borstwit uit a10 erboven terug naar huid
# buik: alles binnen Jordi's rode grenzen + armlijn, tot de onderrand van het lijf
BUIK=[(12,22),(13,22),(12,23),(13,23),                       # tussen linker boog en armlijn
      (15,22),(16,22),(17,22),(15,23),(16,23),(17,23),(15,24),(16,24),(17,24)]  # onder rechter boog tot dijlijn
for p in BUIK: E[p]=3
for (x,y),v in E.items():
    assert a[y,x] not in (14,15) or (x,y)==(13,21)
    n[y,x]=v
    if y<=22: n[32+y+1,x]=v
    elif y>=24: n[32+y,x]=v
im=Image.fromarray(n,'P'); im.putpalette(B.getpalette()); im.save(O+'icon_a11.png',transparency=0)
im.resize((256,512),Image.NEAREST).save(O+'icon_a11_8x.png',transparency=0)
d=np.argwhere(n!=a); print('diff t.o.v. a10',len(d),[(int(x),int(y),int(a[y,x]),int(n[y,x])) for y,x in d])
for f in (0,32):
  for y in range(19,27): print('%2d '%y+''.join('.' if v==0 else '%X'%v for v in n[f+y][:24]))
