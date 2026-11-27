# zoom.py SPRITE UIT [x0 y0 x1 y1]: uitsnede op 14x met raster en coordinaten
import sys; from PIL import Image, ImageDraw
a=Image.open(sys.argv[1]); a.info['transparency']=0; a=a.convert('RGBA'); B=Image.new('RGBA',a.size,(255,255,255,255)); B.alpha_composite(a); a=B.convert('RGB')
x0,y0,x1,y1=map(int,sys.argv[3:7]) if len(sys.argv)>3 else (0,0,64,64); Z=14
c=a.crop((x0,y0,x1,y1)).resize(((x1-x0)*Z,(y1-y0)*Z),0); d=ImageDraw.Draw(c)
for i in range(x1-x0):
    d.line([(i*Z,0),(i*Z,c.height)],fill=(220,220,220)); 
    if (x0+i)%5==0: d.text((i*Z+1,1),str(x0+i),fill='blue')
for j in range(y1-y0):
    d.line([(0,j*Z),(c.width,j*Z)],fill=(220,220,220))
    if (y0+j)%5==0: d.text((1,j*Z+1),str(y0+j),fill='blue')
c.save(sys.argv[2])
