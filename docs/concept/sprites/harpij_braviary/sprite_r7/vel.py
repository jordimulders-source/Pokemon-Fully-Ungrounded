# snavelvarianten.png: per variant kop 12x + hele sprite 1x en 2x, naast r6 (B) en model; strook referentiesnavels 12x
import numpy as np, subprocess; from PIL import Image, ImageDraw; from pal import *
OY,OX=3,13
def to64(g): o=np.full((64,64,3),232,'uint8'); m=g!='.'; o[OY:OY+61,OX:OX+38][m]=rgb(g)[m]; return o
avg=np.load('../sprite_r4/avg.npy'); cov=np.load('../sprite_r4/cov.npy'); MOD=np.full((64,64,3),232,'uint8'); MOD[OY:OY+61,OX:OX+38][cov>=.5]=avg.clip(0,255).astype('uint8')[cov>=.5]
cols=[('r6 (B)',to64(lees('harpij_r6b.txt')))]+[(k,to64(lees(f'harpij_r7_{k}.txt'))) for k in ('V1','V2','V3','V4')]+[('model x0,66',MOD)]
Z=12; b=(13,13,31,27); w=(b[2]-b[0])*Z; h=(b[3]-b[1])*Z; G=16
subprocess.run(['python3','-I','refsnavel.py','ref.png','12'],check=True); R=Image.open('ref.png')
V=Image.new('RGB',(max(len(cols)*(w+G)+G,R.size[0]+2*G),20+h+G+64+G+128+G+20+R.size[1]+G),(255,255,255)); d=ImageDraw.Draw(V)
for i,(t,a) in enumerate(cols):
  x=G+i*(w+G); im=Image.fromarray(a)
  V.paste(im.crop(b).resize((w,h),Image.NEAREST),(x,20)); d.text((x,4),t+' kop 12x',fill=(0,0,0))
  V.paste(im,(x,20+h+G)); V.paste(im.resize((128,128),Image.NEAREST),(x+72,20+h+G))
y=20+h+G+128+G; d.text((G,y),'referenties 12x (Gen 3 waar beschikbaar)',fill=(0,0,0)); V.paste(R,(G,y+16))
V.save('snavelvarianten.png'); print(V.size)
