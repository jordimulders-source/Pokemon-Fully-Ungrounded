# vel.py: raster.txt -> alakazam_charlatan.png, _8x.png en vel.png (sprite 8x | model verkleind 8x, close-up kop, 1x licht/donker)
import sys; sys.path.insert(0,'../silhouet')
from PIL import Image, ImageDraw
from geo import *
from pal import *
im=topng(load('raster.txt'),'alakazam_charlatan.png')
rgba=Image.open('alakazam_charlatan.png').convert('RGBA')
def on(bg,img): b=Image.new('RGBA',img.size,bg); b.alpha_composite(img); return b.convert('RGB')
s8=on((152,208,160,255),rgba).resize((512,512),Image.NEAREST); s8.save('alakazam_charlatan_8x.png')
src=Image.open(D+'referenties/model_silhouet.png').convert('RGB')
mo=src.crop((int(OX),int(OY),int(OX+64*S),int(OY+64*S)))
m8=mo.resize((64,64),Image.BOX).resize((512,512),Image.NEAREST)
mfull=mo.resize((512,512),Image.LANCZOS)
W=512*3+40; o=Image.new('RGB',(W,512+20+400+20+140),'white'); d=ImageDraw.Draw(o)
o.paste(s8,(0,0)); o.paste(m8,(520,0)); o.paste(mfull,(1040,0))
d.text((4,514),'sprite r4 (8x)',fill='black'); d.text((524,514),'model verkleind 64x64 (8x)',fill='black'); d.text((1044,514),'model',fill='black')
# close-up kop x20-50, y0-28 op 14x
box=(20,0,50,28); z=13
k1=on((152,208,160,255),rgba).crop(box).resize(((box[2]-box[0])*z,(box[3]-box[1])*z),Image.NEAREST)
k2=mo.crop((int(box[0]*S),int(box[1]*S),int(box[2]*S),int(box[3]*S))).resize(k1.size,Image.LANCZOS)
o.paste(k1,(0,540)); o.paste(k2,(k1.size[0]+10,540))
y1=540+k1.size[1]+10
for i,bg in enumerate([(248,248,248,255),(40,40,48,255),(152,208,160,255)]):
    o.paste(on(bg,rgba),(20+i*80,y1)); o.paste(on(bg,rgba).resize((128,128),Image.NEAREST),(300+i*140,y1))
o=o.crop((0,0,W,y1+140)); o.save('vel.png')
