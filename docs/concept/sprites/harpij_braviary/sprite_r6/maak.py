# kies variant -> harpij_r6.txt/.png/_8x.png; kuifvarianten.png; vel.png
import sys, numpy as np; from PIL import Image, ImageDraw; from pal import *
KEUS=sys.argv[1]; OY,OX=3,13
import shutil; shutil.copy(f'harpij_r6{KEUS}.txt','harpij_r6.txt')
def to64(g): o=np.full((64,64,3),232,'uint8'); m=g!='.'; o[OY:OY+61,OX:OX+38][m]=rgb(g)[m]; return o
g=lees('harpij_r6.txt'); a=np.zeros((64,64),'uint8')
for y in range(61):
  for x in range(38): a[OY+y,OX+x]=L[g[y,x]]
im=Image.fromarray(a,'P'); im.putpalette([v for _,c in PAL for v in c]+[0]*(768-3*len(PAL))); im.save('harpij_r6.png',transparency=0)
def plat(x,s): return Image.fromarray(x).resize((64*s,64*s),Image.NEAREST)
avg=np.load('../sprite_r4/avg.npy'); cov=np.load('../sprite_r4/cov.npy'); MOD=np.full((64,64,3),232,'uint8'); MOD[OY:OY+61,OX:OX+38][cov>=.5]=avg.clip(0,255).astype('uint8')[cov>=.5]
R6=to64(g); R6A=to64(lees('harpij_r6a.txt')); R6B=to64(lees('harpij_r6b.txt'))
# r5/r4 met hun eigen palet (r5: oude m)
import importlib.util
def laad(pad):
  sp=importlib.util.spec_from_file_location('p'+str(abs(hash(pad))),pad); m=importlib.util.module_from_spec(sp); sp.loader.exec_module(m); return m
p5=laad('../sprite_r5/pal.py'); p4=laad('../sprite_r4/pal.py')
def to64p(p,f): G=p.lees(f); o=np.full((64,64,3),232,'uint8'); mm=G!='.'; o[OY:OY+61,OX:OX+38][mm]=p.rgb(G)[mm]; return o
R5=to64p(p5,'../sprite_r5/harpij_r5.txt'); R4=to64p(p4,'../sprite_r4/harpij_r4.txt')
plat(R6,8).save('harpij_r6_8x.png')
G_,T,Z=16,18,12
def strook(V,d,y,titel,srcs,b):
  d.text((G_,y),titel,fill=(0,0,0)); y+=T; x=G_
  for t,s in srcs:
    c=plat(s,Z).crop((b[0]*Z,b[1]*Z,b[2]*Z,b[3]*Z)); V.paste(c,(x,y)); d.text((x,y+c.size[1]+2),t,fill=(0,0,0)); x+=c.size[0]+G_
  return y+(b[3]-b[1])*Z+G_+14
kb=(13,3,43,28)
K=Image.new('RGB',(5*(30*Z+G_)+G_,T+25*Z+G_+20),(255,255,255)); dk=ImageDraw.Draw(K)
strook(K,dk,0,'kuif 12x',[('A: meer zwarte lijn',R6A),('B: minder',R6B),('r5',R5),('r4',R4),('model x0,66',MOD)],kb); K.save('kuifvarianten.png')
zones=[('kop + kuif 12x',kb,[('r6 A',R6A),('r6 B',R6B),('r5',R5),('r4',R4),('model',MOD)]),
       ('snavel 12x',(13,16,25,26),[('r6',R6),('r5',R5),('model',MOD)]),
       ('vleugelrand 12x',(38,40,51,60),[('r6',R6),('r5',R5),('model',MOD)])]
h=T+512+G_+sum(T+(b[3]-b[1])*Z+G_+14 for _,b,_ in zones)
V=Image.new('RGB',(max(4*(512+G_)+G_,5*(30*Z+G_)+G_),h),(255,255,255)); d=ImageDraw.Draw(V)
for i,(t,p) in enumerate((('r6 ('+KEUS.upper()+')',R6),('r5',R5),('r4',R4),('model x0,66',MOD))): V.paste(plat(p,8),(G_+i*(512+G_),T)); d.text((G_+i*(512+G_),3),t+' (8x)',fill=(0,0,0))
y=T+512+G_
for t,b,s in zones: y=strook(V,d,y,t,s,b)
V.save('vel.png'); print(V.size)
