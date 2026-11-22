import numpy as np; from PIL import Image
O='/home/user/Pokemon-Fully-Ungrounded/docs/concept/sprites/viscacha/icoon/onderdelen/'
B=Image.open(O+'icon_a8.png'); a8=np.array(B); a7=np.array(Image.open(O+'icon_a7.png')); n=a8.copy()
# 1. rechtersnorharen weg: terug naar a7 (lijn en kleur); kleurverdeling a8 blijft elders
R=[(12,19),(13,20),(14,20),(15,21),(16,21),(12,21),(13,21),(14,22),(15,22),(16,23)]
for x,y in R:
    n[y,x]=a7[y,x]
    if y<=22: n[32+y+1,x]=a7[32+y+1,x]
# 2. linkersnorharen kort: 2 lijntjes van 2 px; de buitenste pixels weg
for x,y in [(3,19),(4,22)]:
    n[y,x]=0; n[32+y+1,x]=0
im=Image.fromarray(n,'P'); im.putpalette(B.getpalette()); im.save(O+'icon_a9.png',transparency=0)
im.resize((256,512),Image.NEAREST).save(O+'icon_a9_8x.png',transparency=0)
d=np.argwhere(n!=a8); print('diff t.o.v. a8',len(d),[(int(x),int(y),int(a8[y,x]),int(n[y,x])) for y,x in d])
for f in (0,32):
  for y in range(17,25): print('%2d '%y+''.join('.' if v==0 else '%X'%v for v in n[f+y][:24]))
