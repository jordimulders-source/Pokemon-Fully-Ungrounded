# vergelijk: modelnatief-uitsnede en sprite-uitsnede op dezelfde schaal, met spriteraster over het model
import sys,numpy as np; from PIL import Image, ImageDraw; from toon import img
f,x0,y0,x1,y1,uit=sys.argv[1],*map(int,sys.argv[2:6]),sys.argv[6]; S=16
o=np.load(f)
n=Image.open('natief.png').convert('RGB')
OY=OX=1
m=n.crop((OX+3*x0,OY+3*y0,OX+3*x1,OY+3*y1)).resize(((x1-x0)*S,(y1-y0)*S),0)
m=m.convert('RGBA'); d=ImageDraw.Draw(m,'RGBA')
for x in range(x1-x0+1): d.line([(x*S,0),(x*S,m.height)],fill=(255,0,255,90))
for y in range(y1-y0+1): d.line([(0,y*S),(m.width,y*S)],fill=(255,0,255,90))
s=img(o[y0:y1,x0:x1],S)
out=Image.new('RGB',(m.width*2+10,m.height),(128,128,128)); out.paste(m.convert('RGB'),(0,0)); out.paste(s,(m.width+10,0)); out.save(uit)
