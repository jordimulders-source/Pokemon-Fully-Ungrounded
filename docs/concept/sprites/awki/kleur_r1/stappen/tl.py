# gedeelde helpers awki (aangepast van hatun runa): model-bbox x19 y19, schaal 6.232, top 2, left 4 (silhouet/sil.py 56)
import sys,numpy as np
from PIL import Image,ImageDraw
P='/home/user/Pokemon-Fully-Ungrounded/docs/concept/sprites/awki/'
x0,y0=19,19; s=6.232; top,left=2,4
src=Image.open(P+'referenties/model_gekozen.png').convert('RGB')
C=np.asarray(src).astype(float); LUM=C.mean(2)
SIL=np.array(Image.open(P+'silhouet/silhouet.png'))[:,:,3]>0
def box(x,y):
    bx=x0+(x-left)*s; by=y0+(y-top)*s
    return (slice(max(0,int(by)),int(by+s)),slice(max(0,int(bx)),int(bx+s)))
def pal(f):
    L=open(f).read().split()[3:]; return [tuple(map(int,L[i*3:i*3+3])) for i in range(16)]
def raster(f):
    return [l.rstrip('\n') for l in open(f)][:64]
def rimg(f,pf,bg=(152,208,160)):
    p=pal(pf); R=raster(f); a=np.zeros((64,64,3),'uint8')
    for y,l in enumerate(R):
        for x,ch in enumerate(l):
            a[y,x]=p[int(ch,16)] if ch!='.' else bg
    return Image.fromarray(a)
def model(X0,Y0,X1,Y1,z):
    bx=x0+(X0-left)*s; by=y0+(Y0-top)*s
    pad=Image.new('RGB',(src.width+2000,src.height+2000),(247,247,239)); pad.paste(src,(1000,1000))
    return pad.crop((int(bx)+1000,int(by)+1000,int(bx+(X1-X0)*s)+1000,int(by+(Y1-Y0)*s)+1000)).resize(((X1-X0)*z,(Y1-Y0)*z),Image.LANCZOS)
def grid(im,X0,Y0,z,every=1):
    d=ImageDraw.Draw(im)
    for i in range(0,im.width//z+1):
        if (X0+i)%5==0: d.line([(i*z,0),(i*z,im.height)],fill=(255,0,0)); d.text((i*z+1,1),str(X0+i),fill=(255,0,0))
        elif every: d.line([(i*z,0),(i*z,im.height)],fill=(120,120,120))
    for j in range(0,im.height//z+1):
        if (Y0+j)%5==0: d.line([(0,j*z),(im.width,j*z)],fill=(255,0,0)); d.text((1,j*z+1),str(Y0+j),fill=(255,0,0))
        elif every: d.line([(0,j*z),(im.width,j*z)],fill=(120,120,120))
    return im
def naast(ims,out,gap=10):
    W=sum(i.width for i in ims)+gap*(len(ims)-1); H=max(i.height for i in ims)
    o=Image.new('RGB',(W,H),'white'); x=0
    for i in ims: o.paste(i,(x,0)); x+=i.width+gap
    o.save(out)
if __name__=='__main__':
    X0,Y0,X1,Y1,z=map(int,sys.argv[1:6]); out=sys.argv[6]
    ims=[grid(model(X0,Y0,X1,Y1,z),X0,Y0,z)]
    if len(sys.argv)>7:
        ims.insert(0,grid(rimg(sys.argv[7],sys.argv[8]).crop((X0,Y0,X1,Y1)).resize(((X1-X0)*z,(Y1-Y0)*z),Image.NEAREST),X0,Y0,z))
    naast(ims,out)
