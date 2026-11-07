"""zoom.py uit.png [x0 y0 x1 y1 schaal]: raster.txt (en v7) naast elkaar met rooster en coordinaten."""
import os,sys
from PIL import Image,ImageDraw
H=os.path.dirname(os.path.abspath(__file__)); R=os.path.dirname(H)
PAL=[(152,208,160),(28,20,40),(50,48,98),(80,82,150),(114,118,190),(156,162,222),(72,56,100),(44,34,64),(214,170,204),(166,122,166),(184,230,255),(104,176,236),(40,98,176),(228,221,240),(170,164,198),(252,252,252)]
TEK='.KDSVLFfPpBbGMmW'
a=sys.argv; uit=a[1]; x0,y0,x1,y1,s=(int(v) for v in a[2:7]) if len(a)>2 else (0,0,64,64,10)
def teken(p):
    g=[l.rstrip('\n') for l in open(p)]
    w,h=(x1-x0)*s,(y1-y0)*s
    im=Image.new('RGB',(w+30,h+30),(255,255,255)); d=ImageDraw.Draw(im)
    for y in range(y0,y1):
        for x in range(x0,x1):
            c=g[y][x]
            if c!='.': d.rectangle([30+(x-x0)*s,30+(y-y0)*s,30+(x-x0+1)*s-1,30+(y-y0+1)*s-1],fill=PAL[TEK.index(c)])
    for x in range(x0,x1+1):
        d.line([(30+(x-x0)*s,30),(30+(x-x0)*s,30+h)],fill=(255,120,120) if x%5==0 else (220,220,220))
        if x%5==0 and x<x1: d.text((30+(x-x0)*s+1,10),str(x),fill=(0,0,0))
    for y in range(y0,y1+1):
        d.line([(30,30+(y-y0)*s),(30+w,30+(y-y0)*s)],fill=(255,120,120) if y%5==0 else (220,220,220))
        if y%5==0 and y<y1: d.text((2,30+(y-y0)*s+1),str(y),fill=(0,0,0))
    return im
A=teken(os.path.join(R,'raster.txt')); B=teken(os.path.join(R,'../ronde1g/raster.txt'))
o=Image.new('RGB',(A.width*2+20,A.height),(255,255,255)); o.paste(A,(0,0)); o.paste(B,(A.width+20,0)); o.save(uit)
