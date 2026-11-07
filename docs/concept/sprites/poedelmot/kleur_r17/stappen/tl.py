import sys,numpy as np
from PIL import Image,ImageDraw
P='/home/user/pokemon-fully-ungrounded/docs/concept/sprites/poedelmot/'
x0,y0=139,150; s=(854-139)/62; top,left=17,1
src=Image.open(P+'referenties/samengesteld.png').convert('RGB')
def pal(f):
    L=open(f).read().split()[3:]; return [tuple(map(int,L[i*3:i*3+3])) for i in range(16)]
def raster(f):
    return [l.rstrip('\n') for l in open(f)][:64]
def rimg(f,pf):
    p=pal(pf); R=raster(f); a=np.zeros((64,64,3),'uint8')
    for y,l in enumerate(R):
        for x,ch in enumerate(l):
            a[y,x]=p[int(ch,16)] if ch!='.' else (152,208,160)
    return Image.fromarray(a)
def model(X0,Y0,X1,Y1,z):
    bx=x0+(X0-left)*s; by=y0+(Y0-top)*s
    return src.crop((int(bx),int(by),int(bx+(X1-X0)*s),int(by+(Y1-Y0)*s))).resize(((X1-X0)*z,(Y1-Y0)*z),Image.LANCZOS)
def grid(im,X0,Y0,z):
    d=ImageDraw.Draw(im)
    for i in range(0,im.width//z+1):
        c=(255,0,0) if (X0+i)%5==0 else (90,90,90)
        if (X0+i)%5==0 or z>=99: d.line([(i*z,0),(i*z,im.height)],fill=c,width=1)
        if (X0+i)%5==0: d.text((i*z+1,1),str(X0+i),fill=(255,0,0))
    for j in range(0,im.height//z+1):
        c=(255,0,0) if (Y0+j)%5==0 else (90,90,90)
        if (Y0+j)%5==0 or z>=99: d.line([(0,j*z),(im.width,j*z)],fill=c,width=1)
        if (Y0+j)%5==0: d.text((1,j*z+1),str(Y0+j),fill=(255,0,0))
    return im
if __name__=='__main__':
    X0,Y0,X1,Y1,z=map(int,sys.argv[1:6]); out=sys.argv[6]
    rf=sys.argv[7] if len(sys.argv)>7 else None
    m=grid(model(X0,Y0,X1,Y1,z),X0,Y0,z)
    ims=[m]
    if rf:
        r=rimg(rf,sys.argv[8]).crop((X0,Y0,X1,Y1)).resize(((X1-X0)*z,(Y1-Y0)*z),Image.NEAREST)
        ims=[grid(r,X0,Y0,z),m]
    W=sum(i.width for i in ims)+10*(len(ims)-1); o=Image.new('RGB',(W,ims[0].height),'white'); x=0
    for i in ims: o.paste(i,(x,0)); x+=i.width+10
    o.save(out)
