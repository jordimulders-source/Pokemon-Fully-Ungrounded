from PIL import Image, ImageDraw
import numpy as np
m=Image.open('referenties/model_r5.png').convert('RGBA').crop((196,39,833,992))
S=8
mm=m.resize((42*S,63*S),Image.LANCZOS)
can=Image.new('RGBA',(64*S,64*S),'white'); can.paste(mm,(11*S,1*S),mm)
sp=Image.open('sprite/r2/impala_r2.png').convert('RGBA')
a=np.array(sp)[:,:,3]>0
d=ImageDraw.Draw(can)
for y in range(64):
  for x in range(64):
    if a[y,x]:
      for dx,dy in((1,0),(-1,0),(0,1),(0,-1)):
        X,Y=x+dx,y+dy
        if not(0<=X<64 and 0<=Y<64 and a[Y,X]):
          if dx==1:d.line([(X*S,y*S),(X*S,y*S+S)],fill='red',width=2)
          if dx==-1:d.line([(x*S,y*S),(x*S,y*S+S)],fill='red',width=2)
          if dy==1:d.line([(x*S,Y*S),(x*S+S,Y*S)],fill='red',width=2)
          if dy==-1:d.line([(x*S,y*S),(x*S+S,y*S)],fill='red',width=2)
for i in range(0,64,4):
  d.line([(i*S,0),(i*S,4)],fill='blue'); d.text((i*S+1,0),str(i),fill='blue')
  d.text((0,i*S),str(i),fill='blue')
can.save('sprite/r2/keuring/overlay.png')
