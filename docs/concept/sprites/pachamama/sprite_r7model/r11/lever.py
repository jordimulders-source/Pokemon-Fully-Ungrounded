# r11: png's + vel (hoofd 12x: N1 | N2 | N3 | r10 | model r10 op K1-schaal; daaronder elke variant 3x en 1x)
import numpy as np
from PIL import Image
D='docs/concept/sprites/pachamama/'; R=D+'sprite_r7model/'
pal=Image.open(R+'r4/pachamama_r4.png').getpalette()
r10=np.load(R+'r10/pachamama_r10.npy').astype(np.uint8); m=np.load(R+'r10/masker_k1.npy')
V={v:np.load(R+'r11/pachamama_r11_%s.npy'%v).astype(np.uint8) for v in ('N1','N2','N3')}
for v,o in V.items():
  print(v,'diff met r10 buiten het gezicht:',int(((o!=r10)&~m).sum()),'| binnen:',int(((o!=r10)&m).sum()))
  im=Image.fromarray(o,'P'); im.putpalette(pal); im.save(R+'r11/pachamama_r11_%s.png'%v,transparency=0)
def rgb(a,k):
  i=Image.fromarray(a,'P'); i.putpalette(pal); x=np.array(i.convert('RGB')); x[a==0]=255
  return Image.fromarray(x).resize((64*k,64*k),Image.NEAREST)
k=12; X0,X1,Y0,Y1=17,40,9,32; w=(X1-X0)*k; h=(Y1-Y0)*k
hd=lambda a: rgb(a,k).crop((X0*k,Y0*k,X1*k,Y1*k))
M=Image.open(D+'gemini/r10.png').convert('RGB'); P=5.12; OX,OY=4.6,4.5; T,CI,CJ=3.3,83.7,101.5
mx=lambda x: OX+P*(CI+(x-29)*T); my=lambda y: OY+P*(CJ+(y-30)*T)
mod=M.crop((int(mx(X0)),int(my(Y0)),int(mx(X1)),int(my(Y1)))).resize((w,h),Image.LANCZOS)
heads=[hd(V['N1']),hd(V['N2']),hd(V['N3']),hd(r10),mod]
Wd=Image.new('RGB',(5*(w+12),h+64*3+30),'white')
for i,im in enumerate(heads): Wd.paste(im,(i*(w+12),0))
for i,v in enumerate(('N1','N2','N3')):
  Wd.paste(rgb(V[v],3),(i*(64*3+70),h+20)); Wd.paste(rgb(V[v],1),(i*(64*3+70)+64*3+4,h+20))
Wd.save(R+'r11/vel.png')
