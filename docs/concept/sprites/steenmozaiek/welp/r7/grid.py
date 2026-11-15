import sys,numpy as np
from PIL import Image, ImageDraw
from toon import rgba
FIN=np.load('FIN2.npy')
def gridimg(a,z=14,box=None,pal=None):
    if box: a=a[box[1]:box[3],box[0]:box[2]]
    im=rgba(a) if pal is None else pal(a)
    o=Image.new('RGBA',(im.width*z,im.height*z),(235,235,225,255)); o.alpha_composite(im.resize(o.size,Image.NEAREST))
    d=ImageDraw.Draw(o); x0=box[0] if box else 0; y0=box[1] if box else 0
    for i in range(a.shape[1]+1):
        d.line([(i*z,0),(i*z,o.height)],fill=(0,160,255,255) if (i+x0)%5==0 else (120,120,120,90))
    for j in range(a.shape[0]+1):
        d.line([(0,j*z),(o.width,j*z)],fill=(0,160,255,255) if (j+y0)%5==0 else (120,120,120,90))
    return o
def modelimg(box,z=14):
    n=Image.open('natief.png').convert('RGBA'); s=3.3
    c=n.crop((int(2+box[0]*s),int(2+box[1]*s),int(2+box[2]*s),int(2+box[3]*s))).resize(((box[2]-box[0])*z,(box[3]-box[1])*z),Image.NEAREST)
    d=ImageDraw.Draw(c)
    for i in range(box[2]-box[0]+1): d.line([(i*z,0),(i*z,c.height)],fill=(0,160,255,255) if (i+box[0])%5==0 else (120,120,120,60))
    for j in range(box[3]-box[1]+1): d.line([(0,j*z),(c.width,j*z)],fill=(0,160,255,255) if (j+box[1])%5==0 else (120,120,120,60))
    return c
if __name__=='__main__':
    f=sys.argv[1]; box=tuple(map(int,sys.argv[2].split(','))); out=sys.argv[3]; z=int(sys.argv[4]) if len(sys.argv)>4 else 14
    a=np.load(f); A=gridimg(a,z,box); B=modelimg(box,z)
    V=Image.new('RGBA',(A.width*2+10,A.height),(255,255,255,255)); V.alpha_composite(A,(0,0)); V.alpha_composite(B,(A.width+10,0)); V.save(out)
SRC='../../referenties/model_welp_gekozen.png'
def orig(box,z=24):
    """Uitsnede van het originele model voor spritebox (x0,y0,x1,y1), sprite-raster erover. orig = 99.3+16.9x, 191.5+16.9y"""
    m=Image.open(SRC).convert('RGBA'); k=16.896
    c=m.crop((int(99.3+box[0]*k),int(191.5+box[1]*k),int(99.3+box[2]*k),int(191.5+box[3]*k))).resize(((box[2]-box[0])*z,(box[3]-box[1])*z),Image.LANCZOS)
    d=ImageDraw.Draw(c)
    for i in range(box[2]-box[0]+1): d.line([(i*z,0),(i*z,c.height)],fill=(0,160,255,255) if (i+box[0])%5==0 else (120,120,120,70))
    for j in range(box[3]-box[1]+1): d.line([(0,j*z),(c.width,j*z)],fill=(0,160,255,255) if (j+box[1])%5==0 else (120,120,120,70))
    return c
