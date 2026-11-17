# Zoomvel met coordinaten: zone x0,y0,x1,y1 van r12 p2 op 16x.
import sys; from PIL import Image, ImageDraw
x0,y0,x1,y1=map(int,sys.argv[1:5]); Z=16
s=Image.open('../r16/sprite_B.png').convert('RGBA')
bg=Image.new('RGBA',(64,64),(255,255,255,255)); bg.alpha_composite(s)
c=bg.crop((x0,y0,x1,y1)).convert('RGB').resize(((x1-x0)*Z,(y1-y0)*Z),Image.NEAREST)
v=Image.new('RGB',(c.width+24,c.height+24),(255,255,255)); v.paste(c,(24,24)); d=ImageDraw.Draw(v)
for i in range(x1-x0+1): d.line((24+i*Z,24,24+i*Z,v.height),fill=(200,200,230))
for j in range(y1-y0+1): d.line((24,24+j*Z,v.width,24+j*Z),fill=(200,200,230))
for i in range(x0,x1): d.text((26+(i-x0)*Z,6),str(i%100),fill=(0,0,0))
for j in range(y0,y1): d.text((2,28+(j-y0)*Z),str(j),fill=(0,0,0))
v.save(sys.argv[5])
