# vel.png: sprite 8x | model BOX-verkleind 8x | model ; close-up kop sprite | model (zelfde schaal) ; 1x op licht en donker
import sys,os; H=os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0,H+'/../silhouet')
from PIL import Image,ImageDraw
from geo import *
import pal
R=pal.load(H+'/raster.txt'); pal.topng(R,H+'/alakazam_charlatan.png')
s8=pal.rgb(R).resize((512,512),Image.NEAREST); s8.save(H+'/alakazam_charlatan_8x.png')
src=Image.open(D+'referenties/model_silhouet.png').convert('RGB')
box=(int(OX),int(OY),int(OX+64*S),int(OY+64*S))
mb=src.crop(box).resize((64,64),Image.BOX).resize((512,512),Image.NEAREST)
mf=src.crop(box).resize((512,512),Image.LANCZOS)
x0,y0,x1,y1,z=16,0,50,30,15
ks=pal.rgb(R).crop((x0,y0,x1,y1)).resize(((x1-x0)*z,(y1-y0)*z),Image.NEAREST)
km=src.crop((int(OX+x0*S),int(OY+y0*S),int(OX+x1*S),int(OY+y1*S))).resize(((x1-x0)*z,(y1-y0)*z),Image.LANCZOS)
W=512*3+40; Hh=512+20+km.height+20+64+40
o=Image.new('RGB',(W,Hh),(255,255,255)); d=ImageDraw.Draw(o)
o.paste(s8,(0,0)); o.paste(mb,(532,0)); o.paste(mf,(1064,0))
o.paste(ks,(0,532)); o.paste(km,(ks.width+20,532))
yy=532+km.height+20
lt=Image.open(H+'/alakazam_charlatan.png').convert('RGBA')
for i,bg in enumerate([(248,248,248),(40,40,48),(152,208,160)]):
    b=Image.new('RGBA',(64,64),bg+(255,)); b.alpha_composite(lt); o.paste(b.convert('RGB'),(i*84,yy))
d.text((0,yy+70),'kleur_r7: sprite 8x | model BOX 8x | model ; kop 15x sprite | model ; 1x licht/donker/groen',fill=(0,0,0))
o.save(H+'/vel.png')
