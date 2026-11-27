# zoom10.py SPRITE x0 x1 y0 y1 UIT: uitsnede op 20x met rasterlijnen en coördinaten (alleen om te kijken)
import sys; from PIL import Image, ImageDraw
f,x0,x1,y0,y1,uit=sys.argv[1],*map(int,sys.argv[2:6]),sys.argv[6]; Z=20
a=Image.open(f); a.info['transparency']=0; a=a.convert('RGBA'); B=Image.new('RGBA',a.size,(255,255,255,255)); B.alpha_composite(a)
c=B.convert('RGB').crop((x0,y0,x1,y1)).resize(((x1-x0)*Z,(y1-y0)*Z),0)
T=Image.new('RGB',(c.width+30,c.height+20),'white'); T.paste(c,(30,20)); d=ImageDraw.Draw(T)
for i in range(x1-x0+1): d.line([(30+i*Z,20),(30+i*Z,T.height)],fill=(200,200,200))
for j in range(y1-y0+1): d.line([(30,20+j*Z),(T.width,20+j*Z)],fill=(200,200,200))
for i in range(x1-x0): d.text((32+i*Z,4),str((x0+i)%100),fill='black')
for j in range(y1-y0): d.text((2,24+j*Z),str(y0+j),fill='black')
T.save(uit)
