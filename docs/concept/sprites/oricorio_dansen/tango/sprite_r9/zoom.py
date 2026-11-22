# hulpbeeld: uitsnede (x0,y0,x1,y1) van een png op z-voudig met raster en coördinaten
import sys; from PIL import Image, ImageDraw
f,out=sys.argv[1],sys.argv[2]; x0,y0,x1,y1,z=map(int,sys.argv[3:8])
a=Image.open(f).convert('RGBA').crop((x0,y0,x1,y1)); b=Image.new('RGB',(a.width*z,a.height*z),'white'); r=a.resize(b.size,Image.NEAREST); b.paste(r,(0,0),r)
d=ImageDraw.Draw(b)
for k in range(0,b.width,z): d.line([(k,0),(k,b.height)],fill=(225,225,225))
for k in range(0,b.height,z): d.line([(0,k),(b.width,k)],fill=(225,225,225))
for x in range(0,x1-x0,2): d.text((x*z+2,0),str(x+x0),fill='red')
for y in range(0,y1-y0,2): d.text((0,y*z+2),str(y+y0),fill='red')
b.save(out)
