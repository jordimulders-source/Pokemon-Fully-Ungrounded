# vel_r6.png: r6 | r5 | model (8x); 12x close-ups ring/aansluiting en kop (r6 | r5 | model); 1x licht/donker. Vanuit sprite/.
import sys,numpy as np; sys.path.insert(0,'maker')
from pal5 import PAL as P5; from pal6 import PAL as P6
from PIL import Image
def rgba(f,PAL):
  R=[l.rstrip('\n') for l in open(f)]; a=np.zeros((64,64,4),'uint8')
  for y in range(64):
    for x in range(64):
      if R[y][x]!='.': a[y,x]=(*PAL[R[y][x]],255)
  return Image.fromarray(a)
def op(im,bg=(255,255,255)):
  b=Image.new('RGBA',im.size,bg+(255,)); b.alpha_composite(im); return b.convert('RGB')
r6=op(rgba('maker/raster_r6.txt',P6)); r5=op(rgba('maker/raster_r5.txt',P5)); m=Image.open('meet/model_raster_8x.png').convert('RGB')
z=lambda im,b,k: im.crop(b).resize(((b[2]-b[0])*k,(b[3]-b[1])*k),Image.NEAREST)
m0=Image.open('r8_bol_r7.png').convert('RGB'); PD=400; M=Image.new('RGB',(m0.width+2*PD,m0.height+2*PD),(255,255,255)); M.paste(m0,(PD,PD)); SC=(973-144)/56
def mz(b,k):
  box=(PD+144+(b[0]-4)*SC,PD+215+(b[1]-19)*SC,PD+144+(b[2]-4)*SC,PD+215+(b[3]-19)*SC)
  return M.crop(tuple(int(round(v)) for v in box)).resize(((b[2]-b[0])*k,(b[3]-b[1])*k),Image.NEAREST)
V=Image.new('RGB',(1880,1080),(236,236,236))
for i,im in enumerate([r6,r5]): V.paste(z(im,(0,14,64,62),8),(i*520,0))
V.paste(mz((0,14,64,62),8),(1040,0))
x=0
for b in ((16,34,44,50),(3,35,25,58)):
  w=(b[2]-b[0])*12; V.paste(z(r6,b,12),(x,400)); V.paste(z(r5,b,12),(x+w+6,400)); V.paste(mz(b,12),(x+2*w+12,400)); x+=3*w+30
for i,bg in enumerate([(255,255,255),(40,40,48)]):
  V.paste(op(rgba('maker/raster_r6.txt',P6),bg),(10+i*74,1000))
V.save('maker/vel_r6.png'); print('maker/vel_r6.png')
