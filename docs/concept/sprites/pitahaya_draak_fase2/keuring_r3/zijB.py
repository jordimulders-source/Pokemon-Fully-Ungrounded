import sys
from PIL import Image, ImageDraw
import numpy as np
s=Image.open('sprite_r3/pitahaya2_r3_lipB.png').convert('RGB')
m=Image.open('model/model.png').convert('RGB')
P=5.076; off=3.2
def mx(sx): return (3*sx+2)*P+off
def my(sy): return (3*sy-39)*P+off
x0,y0,x1,y1,W,name=[int(a) for a in sys.argv[1:6]]+[sys.argv[6]]
a=s.crop((x0,y0,x1,y1)).resize(((x1-x0)*W,(y1-y0)*W),Image.NEAREST)
b=m.crop((int(mx(x0)),int(my(y0)),int(mx(x1)),int(my(y1)))).resize(a.size,Image.LANCZOS)
sh=Image.new('RGB',(a.width*2+10,a.height),(128,128,128)); sh.paste(a,(0,0)); sh.paste(b,(a.width+10,0))
d=ImageDraw.Draw(sh)
for i in range(0,x1-x0+1):
  d.line([(a.width+10+i*W,0),(a.width+10+i*W,a.height)],fill=(160,160,255) if (x0+i)%5 else (0,0,255))
for j in range(0,y1-y0+1):
  d.line([(a.width+10,j*W),(sh.width,j*W)],fill=(160,160,255) if (y0+j)%5 else (0,0,255))
sh.save('keuring_r3/'+name)
