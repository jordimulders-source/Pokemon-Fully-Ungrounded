# zij.py raster out x0 y0 x1 y1 z: sprite | model (cellen) op dezelfde schaal, met spritepixelraster over het model
import sys,numpy as np,pal
from PIL import Image,ImageDraw
from meet import s2c
M=Image.open('cellen.png').convert('RGB')
def model(x0,y0,x1,y1,z,grid=True):
    a=s2c(x0,y0); b=s2c(x1,y1)
    big=M.resize((3100,3100),Image.NEAREST)
    im=big.crop((int(a[0]*31),int(a[1]*31),int(b[0]*31),int(b[1]*31))).resize(((x1-x0)*z,(y1-y0)*z),Image.BILINEAR)
    if grid:
        d=ImageDraw.Draw(im)
        for i in range(x0,x1):
            d.line([((i-x0)*z,0),((i-x0)*z,im.height)],fill=(255,170,170) if i%4 else (255,60,60))
            if i%4==0: d.text(((i-x0)*z+1,0),str(i),fill=(200,0,0))
        for j in range(y0,y1):
            d.line([(0,(j-y0)*z),(im.width,(j-y0)*z)],fill=(255,170,170) if j%4 else (255,60,60))
            if j%4==0: d.text((0,(j-y0)*z),str(j),fill=(200,0,0))
    return im
def sprite(R,x0,y0,x1,y1,z,bg=(152,208,160)):
    return pal.rgb(R,bg).crop((x0,y0,x1,y1)).resize(((x1-x0)*z,(y1-y0)*z),Image.NEAREST)
if __name__=='__main__':
    R=pal.load(sys.argv[1]); x0,y0,x1,y1,z=map(int,sys.argv[3:8])
    s=sprite(R,x0,y0,x1,y1,z); m=model(x0,y0,x1,y1,z,len(sys.argv)<9)
    o=Image.new('RGB',(s.width*2+6,s.height),'white'); o.paste(s,(0,0)); o.paste(m,(s.width+6,0)); o.save(sys.argv[2])
