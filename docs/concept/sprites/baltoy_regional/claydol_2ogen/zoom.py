# zoom.py in.png out.png y0 y1 x0 x1 s : uitsnede met raster en coördinaten
import sys; from PIL import Image, ImageDraw
src,out,y0,y1,x0,x1,s=sys.argv[1],sys.argv[2],*map(int,sys.argv[3:8])
im=Image.open(src); t=im.info.get('transparency',0)
im=im.convert('RGBA') if im.mode!='P' else im
if im.mode=='P':
    p=im.getpalette(); px=im.load(); W,H=im.size
    rg=Image.new('RGBA',im.size)
    for y in range(H):
        for x in range(W):
            i=px[x,y]; rg.putpixel((x,y),(0,0,0,0) if i==t else tuple(p[3*i:3*i+3])+(255,))
    im=rg
c=im.crop((x0,y0,x1,y1)); bg=Image.new('RGBA',c.size,(90,160,200,255)); bg.alpha_composite(c)
m=20; z=Image.new('RGB',((x1-x0)*s+m,(y1-y0)*s+m),'white'); z.paste(bg.convert('RGB').resize(((x1-x0)*s,(y1-y0)*s),Image.NEAREST),(m,m))
d=ImageDraw.Draw(z)
for x in range(x1-x0+1): d.line([(m+x*s,m),(m+x*s,z.size[1])],fill=(0,0,0) if (x0+x)%5==0 else (120,120,120))
for y in range(y1-y0+1): d.line([(m,m+y*s),(z.size[0],m+y*s)],fill=(0,0,0) if (y0+y)%5==0 else (120,120,120))
for x in range(x0,x1):
    if x%5==0: d.text((m+(x-x0)*s+2,2),str(x),fill='black')
for y in range(y0,y1):
    if y%5==0: d.text((1,m+(y-y0)*s+2),str(y),fill='black')
z.save(out)
