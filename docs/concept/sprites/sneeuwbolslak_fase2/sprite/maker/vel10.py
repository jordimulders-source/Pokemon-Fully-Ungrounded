# vel_r10.png: kop 12x model | r9 | A | B; A en B op 8x; 1x en 2x licht/donker. Vanuit sprite/.
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
I9,IA,IB=rgba('maker/raster_r9.txt'),rgba('maker/raster_r10A.txt'),rgba('maker/raster_r10B.txt')
m0=Image.open('r8_bol_r7.png').convert('RGB'); PD=400; M=Image.new('RGB',(m0.width+2*PD,m0.height+2*PD),(255,255,255)); M.paste(m0,(PD,PD)); SC=(973-144)/56
def mz(b,k):
  box=(PD+144+(b[0]-4)*SC,PD+215+(b[1]-19)*SC,PD+144+(b[2]-4)*SC,PD+215+(b[3]-19)*SC)
  return M.crop(tuple(int(round(v)) for v in box)).resize(((b[2]-b[0])*k,(b[3]-b[1])*k),Image.NEAREST)
z=lambda im,b,k: op(im).crop(b).resize(((b[2]-b[0])*k,(b[3]-b[1])*k),Image.NEAREST)
V=Image.new('RGB',(1560,1000),(236,236,236)); d=ImageDraw.Draw(V)
b=(2,38,24,58); w=(b[2]-b[0])*12
for i,(t,im) in enumerate([('model',mz(b,12)),('r9',z(I9,b,12)),('A (d)',z(IA,b,12)),('B (#, d lichtkant)',z(IB,b,12))]):
  d.text((i*(w+10)+4,0),'kop '+t,fill=(0,0,0)); V.paste(im,(i*(w+10),12))
y=12+20*12+16
for i,(t,im) in enumerate([('A',IA),('B',IB)]):
  d.text((i*520+4,y),t+' 8x',fill=(0,0,0)); V.paste(z(im,(0,14,64,62),8),(i*520,y+12))
x=1050
for t,im in (('A',IA),('B',IB)):
  for bg in ((255,255,255),(40,40,48)):
    o=op(im,bg); V.paste(o,(x,y+12)); V.paste(o.resize((128,128),Image.NEAREST),(x+70,y+12)) if False else V.paste(o.resize((128,128),Image.NEAREST),(x,y+90)); x+=140
  x=1050; y+=230
V=V.crop((0,0,1560,max(y,12+20*12+16+400))); V.save('maker/vel_r10.png'); print('maker/vel_r10.png',V.size)
