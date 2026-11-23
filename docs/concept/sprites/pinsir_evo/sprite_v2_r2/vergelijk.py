# Hulpmiddel: sprite en model (zelfde maat, zelfde uitsnede) naast elkaar op Z x met spriteraster en coordinaten.
import sys, numpy as np
sys.path.insert(0,'sprite_v2')
from reductie import X0,Y0,S,kaart
from PIL import Image, ImageDraw
cx,cy=kaart(0.3,0.3); OY=63-cy[88]
mod0=Image.open('referenties/model_v2_r4.webp').convert('RGB'); MOD=Image.new('RGB',(1424,1424),'white'); MOD.paste(mod0,(200,200))
p_=10.24; e_=lambda i: 9.25+0.5+(i-1)*p_
SZ=64/S*p_; LX=e_(X0)-0.3/S*p_+200+0.4*SZ/64; TY=e_(Y0)-(0.3+OY)/S*p_+200+0.4*SZ/64
def modelstuk(x0,y0,x1,y1,Z):
    f=SZ/64; return MOD.crop((int(LX+x0*f),int(TY+y0*f),int(LX+x1*f),int(TY+y1*f))).resize(((x1-x0)*Z,(y1-y0)*Z),Image.LANCZOS)
def spritestuk(sp,x0,y0,x1,y1,Z,bg=(255,255,255)):
    o=Image.new('RGB',(64,64),bg); s=sp.convert('RGBA'); o.paste(s,(0,0),s)
    return o.crop((x0,y0,x1,y1)).resize(((x1-x0)*Z,(y1-y0)*Z),Image.NEAREST)
def raster(im,x0,y0,Z,col=(120,120,120)):
    d=ImageDraw.Draw(im)
    for i in range(im.width//Z+1):
        d.line([(i*Z,0),(i*Z,im.height)],fill=(255,0,0) if (x0+i)%5==0 else col)
    for j in range(im.height//Z+1):
        d.line([(0,j*Z),(im.width,j*Z)],fill=(255,0,0) if (y0+j)%5==0 else col)
    return im
def paar(sps,box,Z,titels=None):
    x0,y0,x1,y1=box
    ims=[raster(spritestuk(s,*box,Z),x0,y0,Z) for s in sps]+[raster(modelstuk(*box,Z),x0,y0,Z,(170,170,170))]
    w=ims[0].width; h=ims[0].height
    can=Image.new('RGB',(len(ims)*(w+12)+30,h+44),'white'); d=ImageDraw.Draw(can)
    for k,im in enumerate(ims):
        X=30+k*(w+12); can.paste(im,(X,30))
        for i in range(x1-x0):
            if (x0+i)%5==0: d.text((X+i*Z+1,18),str(x0+i),fill=(0,0,0))
        if titels: d.text((X,2),titels[k],fill=(0,0,0))
    for j in range(y1-y0):
        if (y0+j)%5==0: d.text((2,30+j*Z+1),str(y0+j),fill=(0,0,0))
    return can
if __name__=='__main__':
    box=tuple(map(int,sys.argv[1].split(','))); Z=int(sys.argv[2]); out=sys.argv[3]; fs=sys.argv[4:]
    paar([Image.open(f) for f in fs],box,Z,[f.split('/')[-1] for f in fs]+['model']).save(out)
