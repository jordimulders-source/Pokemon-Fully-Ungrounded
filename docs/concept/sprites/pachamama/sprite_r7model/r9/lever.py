# schrijft pachamama_r9.png (+8x) en vel.png; controleert diff buiten het gezichtsmasker
import sys, numpy as np
from PIL import Image
D='docs/concept/sprites/pachamama/'; R=D+'sprite_r7model/r9/'
o=np.load(sys.argv[1]).astype(np.uint8)
src=Image.open(D+'sprite_r7model/r4/pachamama_r4.png'); r4=np.array(src); pal=src.getpalette()
m=np.load(R+'masker.npy')
print('diff buiten masker:',int(((o!=r4)&~m).sum()),' gewijzigd binnen masker:',int(((o!=r4)&m).sum()),'van',int(m.sum()))
print('kleuren gebruikt:',sorted(set(np.unique(o))-{0}),' r4:',sorted(set(np.unique(r4))-{0}))
im=Image.fromarray(o,'P'); im.putpalette(pal); im.info['transparency']=0; im.save(R+'pachamama_r9.png',transparency=0)
def rgb(a,k):
  i=Image.fromarray(a,'P'); i.putpalette(pal); x=np.array(i.convert('RGB')); x[a==0]=255
  return Image.fromarray(x).resize((64*k,64*k),Image.NEAREST)
rgb(o,8).save(R+'pachamama_r9_8x.png')
# vel: hoofd 12x  r9 | r10-gezicht (zelfde schaal, natief 3:1) | r4 v1 ; daaronder hele sprite 3x en 1x
k=12; X0,X1,Y0,Y1=17,42,9,34; w=(X1-X0)*k; h=(Y1-Y0)*k
def hoofd(a): return rgb(a,k).crop((X0*k,Y0*k,X1*k,Y1*k))
M=Image.open(D+'gemini/r10.png').convert('RGB'); P=5.12; OX,OY=4.6,4.5; A,B=2,7
mx=lambda x: OX+P*(3*x-A); my=lambda y: OY+P*(3*y+B)
mod=M.crop((int(mx(X0)),int(my(Y0)),int(mx(X1)),int(my(Y1)))).resize((w,h),Image.LANCZOS)
V=Image.new('RGB',(3*w+40,h+64*3+40),'white')
V.paste(hoofd(o),(0,0)); V.paste(mod,(w+20,0)); V.paste(hoofd(r4),(2*w+40,0))
V.paste(rgb(o,3),(0,h+20)); V.paste(rgb(r4,3),(64*3+20,h+20))
V.paste(rgb(o,1),(2*64*3+40,h+20)); V.paste(rgb(r4,1),(2*64*3+40+80,h+20))
V.save(R+'vel.png')
