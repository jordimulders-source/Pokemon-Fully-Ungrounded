import numpy as np, subprocess; from PIL import Image, ImageDraw; from pal import *
OY,OX=3,13
def to64(g): o=np.full((64,64,3),232,'uint8'); m=g!='.'; o[OY:OY+61,OX:OX+38][m]=rgb(g)[m]; return o
g=lees('harpij_r8.txt'); a=np.zeros((64,64),'uint8')
for y in range(61):
  for x in range(38): a[OY+y,OX+x]=L[g[y,x]]
im=Image.fromarray(a,'P'); im.putpalette([v for _,c in PAL for v in c]+[0]*(768-3*len(PAL))); im.save('harpij_r8.png',transparency=0)
Image.fromarray(to64(g)).resize((512,512),Image.NEAREST).save('harpij_r8_8x.png')
avg=np.load('../sprite_r4/avg.npy'); cov=np.load('../sprite_r4/cov.npy'); MOD=np.full((64,64,3),232,'uint8'); MOD[OY:OY+61,OX:OX+38][cov>=.5]=avg.clip(0,255).astype('uint8')[cov>=.5]
cols=[('r8 min (harpij_r8)',to64(g)),('r8 meer',to64(lees('harpij_r8_meer.txt'))),('r7 V2',to64(lees('harpij_r7_V2.txt'))),('r6 B',to64(lees('../sprite_r6/harpij_r6b.txt'))),('model x0,66',MOD)]
G_=Image.open('/home/user/Pokemon-Fully-Ungrounded/graphics/pokemon/pidgeot/anim_front_gba.png'); L_=[l.split() for l in open('/home/user/Pokemon-Fully-Ungrounded/graphics/pokemon/pidgeot/normal_gba.pal').read().split('\n')[3:] if l.strip()]
G_.putpalette([int(v) for t in L_ for v in t[:3]]); pg=np.array(G_.convert('RGB')); pg[np.array(G_)==0]=232
Z=12; b=(13,13,31,27); w=(b[2]-b[0])*Z; h=(b[3]-b[1])*Z; G=16
V=Image.new('RGB',(G+6*(w+G),20+h+G+20+512+G),(255,255,255)); d=ImageDraw.Draw(V)
for i,(t,x64) in enumerate(cols):
  x=G+i*(w+G); V.paste(Image.fromarray(x64).crop(b).resize((w,h),Image.NEAREST),(x,20)); d.text((x,4),t+' 12x',fill=(0,0,0))
x=G+5*(w+G); V.paste(Image.fromarray(pg).crop((2,22,20,36)).resize((w,h),Image.NEAREST),(x,20)); d.text((x,4),'pidgeot gen3 12x',fill=(0,0,0))
y=20+h+G; d.text((G,y),'r8 (8x) | r7 V2 (8x) | 1x',fill=(0,0,0))
V.paste(Image.fromarray(to64(g)).resize((512,512),Image.NEAREST),(G,y+16)); V.paste(Image.fromarray(cols[2][1]).resize((512,512),Image.NEAREST),(G+528,y+16))
V.paste(Image.fromarray(to64(g)),(G+1060,y+16))
V.save('vel.png'); print(V.size)
