# harpij_r5.txt -> harpij_r5.png, _8x.png, vel.png (r5 | r4 | model x0,66; close-ups 12x kop+kuif en vleugel)
import numpy as np; from PIL import Image, ImageDraw; from pal import *
OY,OX=3,13; g=lees('harpij_r5.txt'); g4=lees('harpij_r4.txt')
a=np.zeros((64,64),'uint8')
for y in range(61):
  for x in range(38): a[OY+y,OX+x]=L[g[y,x]]
im=Image.fromarray(a,'P'); im.putpalette([v for _,c in PAL for v in c]+[0]*(768-3*len(PAL))); im.save('harpij_r5.png',transparency=0)
def to64(r,m): o=np.full((64,64,3),232,'uint8'); o[OY:OY+61,OX:OX+38][m]=r[m]; return o
def plat(x,s): return Image.fromarray(x).resize((64*s,64*s),Image.NEAREST)
R5=to64(rgb(g),g!='.'); R4=to64(rgb(g4),g4!='.')
avg=np.load('../sprite_r4/avg.npy'); cov=np.load('../sprite_r4/cov.npy'); MOD=to64(avg.clip(0,255).astype('uint8'),cov>=.5)
plat(R5,8).save('harpij_r5_8x.png')
S,G,T,Z=8,16,18,12; zones=[('kop + kuif',(13,3,43,28)),('vleugel',(29,26,51,59))]
zh=sum((b[3]-b[1])*Z+T+G for _,b in zones)
V=Image.new('RGB',(3*(512+G)+G+200,T+512+G+zh),(255,255,255)); d=ImageDraw.Draw(V)
for i,(t,p) in enumerate((('r5',R5),('r4',R4),('model x0,66',MOD))): V.paste(plat(p,S),(G+i*(512+G),T)); d.text((G+i*(512+G),3),t+' (8x)',fill=(0,0,0))
for j,bg in enumerate(((248,248,248),(40,44,56))):
  b=np.where((a>0)[:,:,None],R5,np.array(bg,'uint8')); V.paste(Image.fromarray(b.astype('uint8')),(3*(512+G)+G+j*72,T)); 
d.text((3*(512+G)+G,T+70),'1x',fill=(0,0,0))
y=T+512+G
for t,b in zones:
  d.text((G,y),t+' 12x: r5 | r4 | model',fill=(0,0,0)); y+=T; x=G
  for src in (R5,R4,MOD):
    c=plat(src,Z).crop((b[0]*Z,b[1]*Z,b[2]*Z,b[3]*Z)); V.paste(c,(x,y)); x+=c.size[0]+G
  y+=(b[3]-b[1])*Z+G
V.save('vel.png'); print(V.size)
