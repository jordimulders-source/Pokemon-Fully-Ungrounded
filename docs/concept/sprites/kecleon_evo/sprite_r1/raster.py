# Toont een 63x63/64x64 beeld op 12x met coördinatenraster (alleen om te kijken).
import sys; from PIL import Image, ImageDraw
im=Image.open(sys.argv[1]).convert('RGBA'); s=int(sys.argv[3]) if len(sys.argv)>3 else 12
x0,y0,x1,y1=[int(v) for v in sys.argv[4].split(',')] if len(sys.argv)>4 else (0,0,im.width,im.height)
im=im.crop((x0,y0,x1,y1))
bg=Image.new('RGBA',im.size,(190,200,210,255)); bg.alpha_composite(im)
B=bg.resize((im.width*s,im.height*s),Image.NEAREST); d=ImageDraw.Draw(B)
for i in range(im.width+1):
    d.line([(i*s,0),(i*s,B.height)],fill=(255,0,0) if (i+x0)%5==0 else (150,150,150),width=1)
for j in range(im.height+1):
    d.line([(0,j*s),(B.width,j*s)],fill=(255,0,0) if (j+y0)%5==0 else (150,150,150),width=1)
for i in range(0,im.width,5): d.text((i*s+2,1),str(i+x0),fill=(0,0,255))
for j in range(0,im.height,5): d.text((1,j*s+2),str(j+y0),fill=(0,0,255))
B.save(sys.argv[2])
