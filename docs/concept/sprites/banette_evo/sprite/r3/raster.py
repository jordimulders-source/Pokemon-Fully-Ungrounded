# Model-uitsnede met spriteraster (spritecoördinaten in de marge): python3 raster.py x0 y0 x1 y1 out [z]
import sys; from PIL import Image, ImageDraw
x0,y0,x1,y1=[int(v) for v in sys.argv[1:5]]; out=sys.argv[5]; z=int(sys.argv[6]) if len(sys.argv)>6 else 40
S=968/62; m=Image.open('../../model/model.png').convert('RGB'); mw=Image.new('RGB',(1400,1400),'white'); mw.paste(m,(200,200))
mb=(24+(x0-1)*S,1+(y0-4)*S,24+(x1-1)*S,1+(y1-4)*S)
W,H=(x1-x0)*z,(y1-y0)*z
B=mw.crop(tuple(int(round(v))+200 for v in mb)).resize((W,H),Image.NEAREST)
c=Image.new('RGB',(W+30,H+20),'white'); c.paste(B,(30,20)); d=ImageDraw.Draw(c)
for i in range(x1-x0+1):
    d.line([(30+i*z,20),(30+i*z,20+H)],fill=(0,200,255)); 
    if i<x1-x0: d.text((30+i*z+z//3,4),str(x0+i),fill=(0,0,0))
for j in range(y1-y0+1):
    d.line([(30,20+j*z),(30+W,20+j*z)],fill=(0,200,255))
    if j<y1-y0: d.text((2,20+j*z+z//3),str(y0+j),fill=(0,0,0))
c.save(out)
