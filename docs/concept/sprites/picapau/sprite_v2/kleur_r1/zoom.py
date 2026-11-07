import sys
from PIL import Image, ImageDraw
S='/tmp/claude-0/-home-user-Pokemon-Fully-Ungrounded/bf4d7a1c-4ab8-5d3b-858d-526450e6e0d5/scratchpad/'
x0,y0,x1,y1=map(int,sys.argv[1:5]); Z=int(sys.argv[5]) if len(sys.argv)>5 else 14
r=Image.open('../../blender/B1/b1.png').convert('RGBA').crop((x0*8,y0*8,x1*8,y1*8)).resize(((x1-x0)*Z,(y1-y0)*Z),Image.LANCZOS)
s=Image.open('picapau.png').convert('RGBA').crop((x0,y0,x1,y1)).resize(((x1-x0)*Z,(y1-y0)*Z),Image.NEAREST)
W=(x1-x0)*Z; H=(y1-y0)*Z
v=Image.new('RGBA',(W*2+10,H+14),(200,200,200,255)); v.alpha_composite(r,(0,14)); v.alpha_composite(s,(W+10,14))
d=ImageDraw.Draw(v)
for x in range(x0,x1):
  if x%2==0: d.text((W+10+(x-x0)*Z+2,1),str(x%100),fill=(0,0,255))
for y in range(y0,y1):
  if y%2==0: d.text((W+10+1,14+(y-y0)*Z+1),str(y),fill=(255,0,0))
v.save(S+'zoom.png')
