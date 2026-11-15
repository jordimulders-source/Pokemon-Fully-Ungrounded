# vel_r3.png: r3 | r2 | model (8x); close-ups 12x (oog, bol, staart, aansluiting) model | r3; 1x licht/donker. Vanuit sprite/.
import sys,numpy as np; sys.path.insert(0,'maker'); from pal import PAL
from PIL import Image, ImageDraw
A=sys.argv[1] if len(sys.argv)>1 else 'maker/raster_r3.txt'; OUT=sys.argv[2] if len(sys.argv)>2 else 'maker/vel_r3.png'
B=sys.argv[3] if len(sys.argv)>3 else None
def rgba(f):
  R=[l.rstrip('\n') for l in open(f)]; a=np.zeros((64,64,4),'uint8')
  for y in range(64):
    for x in range(64):
      if R[y][x]!='.': a[y,x]=(*PAL[R[y][x]],255)
  return Image.fromarray(a)
def op(im,bg=(255,255,255)):
  b=Image.new('RGBA',im.size,bg+(255,)); b.alpha_composite(im); return b.convert('RGB')
LA=A.split('_')[-1][:-4]+' (8x)'; LB=(sys.argv[4].split('_')[-1][:-4] if len(sys.argv)>4 else 'r2')+' (8x)'
r3=rgba(A); r2=rgba(sys.argv[4] if len(sys.argv)>4 else 'maker/raster_r2.txt'); rb=rgba(B) if B else None
m0=Image.open('r8_bol_r7.png').convert('RGB'); P=400; model=Image.new('RGB',(m0.width+2*P,m0.height+2*P),(255,255,255)); model.paste(m0,(P,P)); S=(973-144)/56
def mcrop(x0,y0,x1,y1,z):
  box=(P+144+(x0-4)*S,P+215+(y0-19)*S,P+144+(x1-4)*S,P+215+(y1-19)*S)
  return model.crop(tuple(int(round(v)) for v in box)).resize(((x1-x0)*z,(y1-y0)*z),Image.NEAREST)
def scrop(im,x0,y0,x1,y1,z): return op(im.crop((x0,y0,x1,y1))).resize(((x1-x0)*z,(y1-y0)*z),Image.NEAREST)
W=1620; H=1900; vel=Image.new('RGB',(W,H),(236,236,236)); d=ImageDraw.Draw(vel)
def lab(x,y,t): d.text((x,y),t,fill=(0,0,0))
for i,(t,im) in enumerate([(LA,r3),(LB,r2)]):
  lab(10+i*530,5,t); vel.paste(op(im).crop((0,14,64,62)).resize((512,384),Image.NEAREST),(10+i*530,20))
lab(1070,5,'model (8x)'); vel.paste(mcrop(0,14,64,62,8),(1070,20))
y=420
cl=[('oog',6,41,20,52),('bol',19,17,45,43),('staart',39,17,61,52),('aansluiting',17,34,45,53)]
x=10
for n,x0,y0,x1,y1 in cl[:2]:
  w=(x1-x0)*12; lab(x,y,f'{n} 12x: model | r3b'+(' | oog B' if n=='oog' and rb else ''))
  vel.paste(mcrop(x0,y0,x1,y1,12),(x,y+15)); vel.paste(scrop(r3,x0,y0,x1,y1,12),(x+w+8,y+15))
  if n=='oog' and rb: vel.paste(scrop(rb,x0,y0,x1,y1,12),(x+2*w+16,y+15)); x+=w+8
  x+=2*w+30
y=y+15+26*12+20; x=10
for n,x0,y0,x1,y1 in cl[2:]:
  w=(x1-x0)*12; lab(x,y,f'{n} 12x: model | r3b')
  vel.paste(mcrop(x0,y0,x1,y1,12),(x,y+15)); vel.paste(scrop(r3,x0,y0,x1,y1,12),(x+w+8,y+15)); x+=2*w+30
y=y+15+35*12+20
lab(10,y,'1x en 2x op licht/donker: r3b'+(' | oog B' if rb else '')+' | model 1x')
xs=10
for im in [r3]+([rb] if rb else []):
  vel.paste(op(im),(xs,y+15)); vel.paste(op(im,(40,40,48)),(xs+70,y+15))
  vel.paste(op(im).resize((128,128),Image.NEAREST),(xs+140,y+15)); vel.paste(op(im,(40,40,48)).resize((128,128),Image.NEAREST),(xs+275,y+15)); xs+=420
vel.paste(Image.open('meet/model_1x.png'),(xs,y+15))
vel=vel.crop((0,0,W,y+160)); vel.save(OUT); print(OUT,vel.size)
