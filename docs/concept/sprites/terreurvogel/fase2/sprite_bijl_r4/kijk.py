# kijk.py IN.png UIT.png [x0 y0 x1 y1] [schaal]: vergroting met rasterlijnen en coördinaten
import sys; from PIL import Image, ImageDraw
im=Image.open(sys.argv[1]).convert('RGBA')
b=[int(v) for v in sys.argv[3:7]] if len(sys.argv)>6 else [0,0,64,64]
s=int(sys.argv[7]) if len(sys.argv)>7 else 12
c=im.crop(b); bg=Image.new('RGBA',c.size,(200,220,200,255)); bg.alpha_composite(c)
z=bg.resize((c.width*s,c.height*s),Image.NEAREST); d=ImageDraw.Draw(z)
for i in range(c.width+1): d.line([(i*s,0),(i*s,z.height)],fill=(180,180,180),width=1)
for j in range(c.height+1): d.line([(0,j*s),(z.width,j*s)],fill=(180,180,180),width=1)
for i in range(0,c.width,2): d.text((i*s+1,0),str(b[0]+i),fill=(0,0,255))
for j in range(0,c.height,2): d.text((0,j*s+1),str(b[1]+j),fill=(0,0,255))
z.save(sys.argv[2])
