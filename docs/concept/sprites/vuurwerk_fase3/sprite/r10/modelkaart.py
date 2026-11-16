# Hulp r10: model_v14 teruggelegd op het r9-spriteraster (zelfde 115%-kopvervorming als ../r5/kop5.py), 16x per spritepixel,
# met raster en coordinaten, naast r9 a. Zo is per spritepixel te zien wat het model daar heeft.
import sys, json, numpy as np; from PIL import Image, ImageDraw
AX,AY,R,S=22.0,18.0,7.0,1.15
M=np.asarray(Image.open('../../referenties/model_v14.png').convert('RGB'))
PAL=json.load(open('../r9/palet.json'))
def inv(u,v):
    d=AX-u; t=np.clip(d/R,0,1); w=t*t*(3-2*t); s=1+(S-1)*w
    return AX-d/s, AY+(v-AY)/s
def kaart(x0,y0,x1,y1,Z=32):
    W,H=(x1-x0)*Z,(y1-y0)*Z; out=np.zeros((H,W,3),np.uint8)
    for j in range(H):
        for i in range(W):
            u,v=inv(x0+(i+.5)/Z,y0+(j+.5)/Z); mx,my=int(106+12*u),int(120+12*v)
            out[j,i]=M[min(max(my,0),1023),min(max(mx,0),1023)]
    return Image.fromarray(out)
def spr(f,x0,y0,x1,y1,Z=32):
    s=np.asarray(Image.open(f)).astype(int); P=np.array(PAL,np.uint8); c=P[s[y0:y1,x0:x1]]; c[s[y0:y1,x0:x1]==0]=255
    return Image.fromarray(c).resize(((x1-x0)*Z,(y1-y0)*Z),Image.NEAREST)
def raster(im,x0,y0,Z=32):
    d=ImageDraw.Draw(im)
    for k in range(0,im.size[0],Z): d.line([(k,0),(k,im.size[1])],fill=(150,150,150) if (x0+k//Z)%5 else (0,90,255))
    for k in range(0,im.size[1],Z): d.line([(0,k),(im.size[0],k)],fill=(150,150,150) if (y0+k//Z)%5 else (0,90,255))
    return im
if __name__=='__main__':
    x0,y0,x1,y1=[int(a) for a in sys.argv[1:5]]; files=sys.argv[6:]
    ims=[raster(spr(f,x0,y0,x1,y1),x0,y0) for f in files]+[raster(kaart(x0,y0,x1,y1),x0,y0)]
    W=sum(i.size[0]+10 for i in ims); v=Image.new('RGB',(W,ims[0].size[1]+20),(230,230,230)); d=ImageDraw.Draw(v)
    x=0
    for i in ims: v.paste(i,(x,20)); x+=i.size[0]+10
    d.text((2,2),'x%d..%d y%d..%d (blauw = veelvoud van 5)'%(x0,x1,y0,y1),fill=0); v.save(sys.argv[5])
