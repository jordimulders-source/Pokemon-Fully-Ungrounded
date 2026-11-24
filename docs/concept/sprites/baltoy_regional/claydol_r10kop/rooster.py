# Hulpje: beeld op N× met rasterlijnen en coördinaten (alleen om te kijken)
import sys, numpy as np; from PIL import Image, ImageDraw
def rooster(im, N=12, uit='x.png', x0=0,y0=0,x1=None,y1=None):
    im=im.convert('RGBA'); w,h=im.size; x1=x1 or w; y1=y1 or h
    c=im.crop((x0,y0,x1,y1)).resize(((x1-x0)*N,(y1-y0)*N),Image.NEAREST)
    v=Image.new('RGBA',(c.width+30,c.height+30),(255,255,255,255)); v.alpha_composite(c,(30,30)); d=ImageDraw.Draw(v)
    for i in range(x1-x0+1):
        X=30+i*N; d.line((X,30,X,v.height),fill=(0,160,255,255) if (x0+i)%5==0 else (200,200,200,255))
        if (x0+i)%5==0: d.text((X+1,2),str(x0+i),fill='blue')
    for j in range(y1-y0+1):
        Y=30+j*N; d.line((30,Y,v.width,Y),fill=(0,160,255,255) if (y0+j)%5==0 else (200,200,200,255))
        if (y0+j)%5==0: d.text((2,Y+1),str(y0+j),fill='blue')
    v.save(uit)
if __name__=='__main__':
    p=sys.argv[1]; im=Image.open(p)
    if im.mode=='P': im.info['transparency']=0
    a=[int(x) for x in sys.argv[3:]]
    rooster(im,12,sys.argv[2],*a)
