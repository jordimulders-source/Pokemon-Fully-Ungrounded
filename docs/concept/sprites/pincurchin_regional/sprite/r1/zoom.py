# uitsnede sprite | model op 16x met raster. zoom.py sprite.png uit x0 y0 x1 y1
import sys; from PIL import Image,ImageDraw
sp=Image.open(sys.argv[1]).convert('RGBA'); x0,y0,x1,y1=map(int,sys.argv[3:7]); Z=16
b=Image.new('RGBA',sp.size,(255,255,255,255)); b.alpha_composite(sp)
c=b.crop((x0,y0,x1,y1)).resize(((x1-x0)*Z,(y1-y0)*Z),Image.NEAREST)
m=Image.open('natief_A.png').convert('RGB'); s=82/60; oy=63-round(73/s)
mc=m.resize(c.size,Image.NEAREST,box=(10+(x0-2)*s,13+(y0-oy)*s,10+(x1-2)*s,13+(y1-oy)*s))
v=Image.new('RGB',(c.width*2+10,c.height),'white'); v.paste(c.convert('RGB'),(0,0)); v.paste(mc,(c.width+10,0))
d=ImageDraw.Draw(v)
for off in (0,c.width+10):
    for i in range(x1-x0+1): d.line([(off+i*Z,0),(off+i*Z,c.height)],fill=(200,200,255))
    for j in range(y1-y0+1): d.line([(off,j*Z),(off+c.width,j*Z)],fill=(200,200,255))
for i in range(0,x1-x0,5): d.text((i*Z+2,2),str(x0+i),fill=(0,0,255))
for j in range(0,y1-y0,5): d.text((2,j*Z+2),str(y0+j),fill=(0,0,255))
v.save(sys.argv[2])
