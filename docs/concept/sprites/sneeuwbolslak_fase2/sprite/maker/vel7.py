# vel_r7.png: r7 | r6 | model (8x); bol 12x: r7 | r6 | model; 1x en 2x licht/donker (r7, model). Vanuit sprite/.
import sys,numpy as np; sys.path.insert(0,'maker')
from pal6 import PAL as P6
from PIL import Image
def rgba(f):
  R=[l.rstrip('\n') for l in open(f)]; a=np.zeros((64,64,4),'uint8')
  for y in range(64):
    for x in range(64):
      if R[y][x]!='.': a[y,x]=(*P6[R[y][x]],255)
  return Image.fromarray(a)
def op(im,bg=(255,255,255)):
  b=Image.new('RGBA',im.size,bg+(255,)); b.alpha_composite(im); return b.convert('RGB')
A=rgba('maker/raster_r7.txt'); B=rgba('maker/raster_r6.txt'); r7=op(A); r6=op(B)
m0=Image.open('r8_bol_r7.png').convert('RGB'); PD=400; M=Image.new('RGB',(m0.width+2*PD,m0.height+2*PD),(255,255,255)); M.paste(m0,(PD,PD)); SC=(973-144)/56
def mz(b,k):
  box=(PD+144+(b[0]-4)*SC,PD+215+(b[1]-19)*SC,PD+144+(b[2]-4)*SC,PD+215+(b[3]-19)*SC)
  return M.crop(tuple(int(round(v)) for v in box)).resize(((b[2]-b[0])*k,(b[3]-b[1])*k),Image.NEAREST)
z=lambda im,b,k: im.crop(b).resize(((b[2]-b[0])*k,(b[3]-b[1])*k),Image.NEAREST)
V=Image.new('RGB',(1560,1230),(236,236,236))
for i,im in enumerate([r7,r6]): V.paste(z(im,(0,14,64,62),8),(i*520,0))
V.paste(mz((0,14,64,62),8),(1040,0))
b=(19,18,44,41); w=(b[2]-b[0])*12
for i,im in enumerate([z(r7,b,12),z(r6,b,12),mz(b,12)]): V.paste(im,(i*(w+10),400))
y=400+23*12+20; x=10
for im,mod in ((A,False),(None,True)):
  for bg in ((255,255,255),(40,40,48)):
    t=Image.open('meet/model_1x.png').convert('RGB') if mod else op(im,bg)
    V.paste(t,(x,y)); V.paste(t.resize((t.width*2,t.height*2),Image.NEAREST),(x,y+80)); x+=t.width*2+20
    if mod: break
V.save('maker/vel_r7.png'); print('maker/vel_r7.png')
