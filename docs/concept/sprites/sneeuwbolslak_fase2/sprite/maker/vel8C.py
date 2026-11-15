# vel_r8C.png: A | B | raster_af (8x); bol 12x A | B | model; 1x en 2x op licht/donker (A, B). Vanuit sprite/.
import sys,numpy as np; sys.path.insert(0,'maker')
from pal6 import PAL as P6
from PIL import Image, ImageDraw
def rgba(f):
  R=[l.rstrip('\n') for l in open(f)]; a=np.zeros((64,64,4),'uint8')
  for y in range(64):
    for x in range(64):
      if R[y][x]!='.': a[y,x]=(*P6[R[y][x]],255)
  return Image.fromarray(a)
def op(im,bg=(255,255,255)):
  b=Image.new('RGBA',im.size,bg+(255,)); b.alpha_composite(im); return b.convert('RGB')
IC,IA,IB=rgba('maker/raster_r8C.txt'),rgba('maker/raster_r8A.txt'),rgba('maker/raster_r8B.txt')
m0=Image.open('r8_bol_r7.png').convert('RGB'); PD=400; M=Image.new('RGB',(m0.width+2*PD,m0.height+2*PD),(255,255,255)); M.paste(m0,(PD,PD)); SC=(973-144)/56
def mz(b,k):
  box=(PD+144+(b[0]-4)*SC,PD+215+(b[1]-19)*SC,PD+144+(b[2]-4)*SC,PD+215+(b[3]-19)*SC)
  return M.crop(tuple(int(round(v)) for v in box)).resize(((b[2]-b[0])*k,(b[3]-b[1])*k),Image.NEAREST)
z=lambda im,b,k: im.crop(b).resize(((b[2]-b[0])*k,(b[3]-b[1])*k),Image.NEAREST)
V=Image.new('RGB',(1560,1000),(236,236,236)); d=ImageDraw.Draw(V)
for i,(t,im) in enumerate([('C hybride',IC),('A sneeuwjacht',IA),('B plusvlokken',IB)]):
  d.text((i*520+4,2),t,fill=(0,0,0)); V.paste(z(op(im),(0,14,64,62),8),(i*520,14))
b=(19,18,44,41); w=(b[2]-b[0])*12
for i,(t,im) in enumerate([('C',z(op(IC),b,12)),('model',mz(b,12))]):
  d.text((i*(w+10)+4,404),t,fill=(0,0,0)); V.paste(im,(i*(w+10),418))
y=418+23*12+16; x=10
for t,im in (('C',IC),):
  d.text((x,y-12),t,fill=(0,0,0))
  for bg in ((255,255,255),(40,40,48)):
    o=op(im,bg); V.paste(o,(x,y)); V.paste(o.resize((128,128),Image.NEAREST),(x,y+70)); x+=140
  x+=30
V=V.crop((0,0,1560,y+205)); V.save('maker/vel_r8C.png'); print('maker/vel_r8C.png',V.size)
