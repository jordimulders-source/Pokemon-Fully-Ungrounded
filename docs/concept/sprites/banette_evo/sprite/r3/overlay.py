# Sprite-omtrek (rood) + donkere spritepixels (cyaan rand) over het model op z×, met offset (dx,dy) in spritepixels
# python3 overlay.py npy x0 y0 x1 y1 out [z] [dx] [dy]
import sys,numpy as np; from PIL import Image, ImageDraw
g=np.load(sys.argv[1]); x0,y0,x1,y1=[int(v) for v in sys.argv[2:6]]; out=sys.argv[6]
z=int(sys.argv[7]) if len(sys.argv)>7 else 8; dx=float(sys.argv[8]) if len(sys.argv)>8 else 0; dy=float(sys.argv[9]) if len(sys.argv)>9 else 0
S=968/62; m=Image.open('../../model/model.png').convert('RGB'); mw=Image.new('RGB',(1400,1400),'white'); mw.paste(m,(200,200))
mb=(24+(x0-1+dx)*S,1+(y0-4+dy)*S,24+(x1-1+dx)*S,1+(y1-4+dy)*S)
W,H=(x1-x0)*z,(y1-y0)*z
B=mw.crop(tuple(int(round(v))+200 for v in mb)).resize((W,H),Image.LANCZOS); d=ImageDraw.Draw(B)
f=g>0
for j in range(y0,y1):
  for i in range(x0,x1):
    if not f[j,i]: continue
    X,Y=(i-x0)*z,(j-y0)*z
    if j==0 or not f[j-1,i]: d.line([(X,Y),(X+z,Y)],fill=(255,0,0),width=2)
    if j==63 or not f[j+1,i]: d.line([(X,Y+z),(X+z,Y+z)],fill=(255,0,0),width=2)
    if i==0 or not f[j,i-1]: d.line([(X,Y),(X,Y+z)],fill=(255,0,0),width=2)
    if i==63 or not f[j,i+1]: d.line([(X+z,Y),(X+z,Y+z)],fill=(255,0,0),width=2)
B.save(out)
