# zoomcrop met raster en coordinaten: zoom.py in.png out.png x0 y0 x1 y1 [z]
import sys; from PIL import Image, ImageDraw
im=Image.open(sys.argv[1]).convert('RGBA'); x0,y0,x1,y1=map(int,sys.argv[3:7]); z=int(sys.argv[7]) if len(sys.argv)>7 else 20
c=im.crop((x0,y0,x1,y1)); W,H=c.size; o=Image.new('RGB',(W*z+30,H*z+20),(255,255,255))
bg=Image.new('RGBA',c.size,(200,200,220,255)); bg.alpha_composite(c); o.paste(bg.convert('RGB').resize((W*z,H*z),Image.NEAREST),(30,20))
d=ImageDraw.Draw(o)
for i in range(W+1): d.line([(30+i*z,20),(30+i*z,20+H*z)],fill=(128,128,128) if (x0+i)%5 else (255,0,0))
for j in range(H+1): d.line([(30,20+j*z),(30+W*z,20+j*z)],fill=(128,128,128) if (y0+j)%5 else (255,0,0))
for i in range(0,W,2): d.text((30+i*z+2,5),str(x0+i),fill=(0,0,0))
for j in range(0,H,2): d.text((2,20+j*z+4),str(y0+j),fill=(0,0,0))
o.save(sys.argv[2])
