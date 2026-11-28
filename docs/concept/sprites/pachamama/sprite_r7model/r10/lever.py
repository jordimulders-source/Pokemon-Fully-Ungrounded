# K1 -> pachamama_r10.png (+8x) en vel.png (hoofd 12x: K1 | r9 | model r10 op K1-schaal; daaronder K1 3x/1x en r9 3x/1x)
import numpy as np
from PIL import Image
D='docs/concept/sprites/pachamama/'; R=D+'sprite_r7model/'
src=Image.open(R+'r4/pachamama_r4.png'); pal=src.getpalette(); r4=np.array(src)
o=np.load(R+'r10/pachamama_r10.npy').astype(np.uint8); r9=np.array(Image.open(R+'r9/pachamama_r9.png'))
zone=np.load(R+'r10/zone_k1.npy'); m=np.load(R+'r10/masker_k1.npy')
print('diff met r4 buiten de hoofdzone:',int(((o!=r4)&~zone).sum()),'| romp-pixels (rood/roze) in de zone die van r4 afwijken:',int(((o!=r4)&zone&~m&np.isin(o,(7,8,9))).sum()))
im=Image.fromarray(o,'P'); im.putpalette(pal); im.save(R+'r10/pachamama_r10.png',transparency=0)
def rgb(a,k):
  i=Image.fromarray(a,'P'); i.putpalette(pal); x=np.array(i.convert('RGB')); x[a==0]=255
  return Image.fromarray(x).resize((64*k,64*k),Image.NEAREST)
rgb(o,8).save(R+'r10/pachamama_r10_8x.png')
k=12; X0,X1,Y0,Y1=16,42,7,33; w=(X1-X0)*k; h=(Y1-Y0)*k
hd=lambda a: rgb(a,k).crop((X0*k,Y0*k,X1*k,Y1*k))
M=Image.open(D+'gemini/r10.png').convert('RGB'); P=5.12; OX,OY=4.6,4.5; T,CI,CJ=3.3,83.7,101.5
mx=lambda x: OX+P*(CI+(x-29)*T); my=lambda y: OY+P*(CJ+(y-30)*T)
mod=M.crop((int(mx(X0)),int(my(Y0)),int(mx(X1)),int(my(Y1)))).resize((w,h),Image.LANCZOS)
V=Image.new('RGB',(3*w+40,h+64*3+30),'white')
V.paste(hd(o),(0,0)); V.paste(hd(r9),(w+20,0)); V.paste(mod,(2*w+40,0))
V.paste(rgb(o,3),(0,h+20)); V.paste(rgb(r9,3),(64*3+20,h+20)); V.paste(rgb(o,1),(2*64*3+40,h+20)); V.paste(rgb(r9,1),(2*64*3+120,h+20))
V.save(R+'r10/vel.png')
