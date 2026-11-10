# zoom.py raster out x0 y0 x1 y1 [z]: uitsnede met raster en coordinaten, naast het model
import sys,os; H=os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0,H+'/../silhouet')
from PIL import Image,ImageDraw
from geo import *
import pal
def zoom(R,x0,y0,x1,y1,z=24,model=True,grid=True):
    s=pal.rgb(R).crop((x0,y0,x1,y1)).resize(((x1-x0)*z,(y1-y0)*z),Image.NEAREST)
    ims=[s]
    if model:
        src=Image.open(D+'referenties/model_silhouet.png').convert('RGB')
        ims.append(src.crop((int(OX+x0*S),int(OY+y0*S),int(OX+x1*S),int(OY+y1*S))).resize(s.size,Image.LANCZOS))
    o=Image.new('RGB',(sum(i.width for i in ims)+30*len(ims),s.height+20),'white'); d=ImageDraw.Draw(o)
    X=20
    for im in ims:
        o.paste(im,(X,20)); 
        if grid:
            for i in range(x1-x0+1): d.line([(X+i*z,20),(X+i*z,20+s.height)],fill=(255,0,0) if (x0+i)%5==0 else (230,190,190))
            for j in range(y1-y0+1): d.line([(X,20+j*z),(X+im.width,20+j*z)],fill=(255,0,0) if (y0+j)%5==0 else (230,190,190))
        for i in range(x0,x1): d.text((X+(i-x0)*z+3,4),str(i%100),fill=(0,0,0))
        X+=im.width+30
    for j in range(y0,y1): d.text((2,20+(j-y0)*z+4),str(j),fill=(0,0,0))
    return o
if __name__=='__main__':
    a=sys.argv; z=int(a[7]) if len(a)>7 else 24
    zoom(pal.load(a[1]),*map(int,a[3:7]),z=z).save(a[2])
