# zoom.py x0 y0 x1 y1 [sprite.npy] -> _tmp/zoom.png: links model (natief, 3 cellen per spritepixel), rechts sprite; raster per spritepixel, label elke 2
import sys; import numpy as np; from PIL import Image, ImageDraw
x0,y0,x1,y1=map(int,sys.argv[1:5]); f=sys.argv[5] if len(sys.argv)>5 else 'r3.npy'
N=np.asarray(Image.open('_tmp/natief.png').convert('RGB'))
PAL=[(255,255,255),(24,20,16),(226,150,96),(192,110,60),(142,74,42),(250,242,214),(230,210,166),(196,170,124),
     (232,82,74),(204,196,192),(142,132,130),(78,70,70),(252,226,96),(212,170,52),(255,255,255),(98,48,26)]
o=np.load(f); S=24
w,h=x1-x0,y1-y0; im=Image.new('RGB',(2*w*S+60,h*S+30),(180,180,180)); d=ImageDraw.Draw(im)
for y in range(y0,y1):
  for x in range(x0,x1):
    for j in range(3):
      for i in range(3):
        r,c=3*y-2+j,4+3*x+i
        col=tuple(int(v) for v in N[r,c]) if 0<=r<200 and 0<=c<200 else (255,255,255)
        d.rectangle([20+(x-x0)*S+i*8,20+(y-y0)*S+j*8,20+(x-x0)*S+i*8+7,20+(y-y0)*S+j*8+7],fill=col)
    d.rectangle([40+w*S+(x-x0)*S,20+(y-y0)*S,40+w*S+(x-x0)*S+S-1,20+(y-y0)*S+S-1],fill=PAL[o[y,x]])
for k,x in enumerate(range(x0,x1+1)):
  for ox in (20,40+w*S): d.line([(ox+k*S,20),(ox+k*S,20+h*S)],fill=(120,120,255))
  if x%2==0 and x<x1: d.text((22+k*S,4),str(x),fill=(0,0,0)); d.text((42+w*S+k*S,4),str(x),fill=(0,0,0))
for k,y in enumerate(range(y0,y1+1)):
  for ox in (20,40+w*S): d.line([(ox,20+k*S),(ox+w*S,20+k*S)],fill=(120,120,255))
  if y%2==0 and y<y1: d.text((2,24+k*S),str(y),fill=(0,0,0))
im.save(sys.argv[6] if len(sys.argv)>6 else '_tmp/zoom.png'); print(im.size)
