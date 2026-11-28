# hoofd 12x: sprite(s) | r10 natief op dezelfde schaal (3 natief = 1 spritepx, uitgelijnd met A,B)
import sys, numpy as np
from PIL import Image
D='docs/concept/sprites/pachamama/'
A=int(sys.argv[1]); B=int(sys.argv[2]); uit=sys.argv[3]; fs=sys.argv[4:]
pal=Image.open(D+'sprite_r7model/r4/pachamama_r4.png').getpalette()
k=12; X0,X1,Y0,Y1=17,42,10,34
ims=[]
for f in fs:
  a=np.load(f).astype(np.uint8) if f.endswith('.npy') else np.array(Image.open(f))
  im=Image.fromarray(a,'P'); im.putpalette(pal); im.info.pop('transparency',None)
  rgb=np.array(im.convert('RGB')); rgb[a==0]=255
  ims.append(Image.fromarray(rgb).crop((X0,Y0,X1,Y1)).resize(((X1-X0)*k,(Y1-Y0)*k),0))
M=Image.open(D+'gemini/r10.png').convert('RGB')
P=5.12; OX,OY=4.6,4.5
# spritepx x <-> natief i0=3x-A ; modelx = OX+P*i
mx=lambda x: OX+P*(3*x-A); my=lambda y: OY+P*(3*y+B)
ims.append(M.crop((int(mx(X0)),int(my(Y0)),int(mx(X1)),int(my(Y1)))).resize(((X1-X0)*k,(Y1-Y0)*k),Image.LANCZOS))
W=Image.new('RGB',(len(ims)*((X1-X0)*k+8),(Y1-Y0)*k),'white')
for i,im in enumerate(ims): W.paste(im,(i*((X1-X0)*k+8),0))
W.save(uit)
