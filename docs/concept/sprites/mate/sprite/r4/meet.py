# Model in canvascoördinaten (zelfde afbeelding als vel.py): m1 = 64x64 boxgemiddelde, m8 = 8x met raster.
import numpy as np; from PIL import Image, ImageDraw
o=np.load('r1/kaal.npy'); yy,xx=np.where(o>0); oy0,ox0=yy.min(),xx.min(); hh=yy.max()-oy0+1; ww=xx.max()-ox0+1
top=63-hh; fx=(64-ww)//2; s=1.75; NY0,NX0=8+0.4,16+0.6
def tm(sx,sy): return ((NX0+(sx-fx+ox0)*s)*10.24-1.0,(NY0+(sy-top+oy0)*s)*10.24-1.0)
M=Image.open('../referenties/model.png').convert('RGB'); (a0,b0),(a1,b1)=tm(0,0),tm(64,64)
big=Image.new('RGB',(3000,3000),'white'); big.paste(M,(1000,1000))
crop=big.crop((int(a0)+1000,int(b0)+1000,int(a1)+1000,int(b1)+1000))
def m(n): return np.asarray(crop.resize((n,n),Image.BOX)).astype(int)
if __name__=='__main__':
    import sys
    x0,y0,x1,y1=map(int,sys.argv[1:5]); S=int(sys.argv[5]) if len(sys.argv)>5 else 16; out=sys.argv[6]
    c=crop.resize((64*S,64*S),Image.LANCZOS).crop((x0*S,y0*S,(x1+1)*S,(y1+1)*S)); d=ImageDraw.Draw(c)
    for x in range(x0,x1+2): d.line([((x-x0)*S,0),((x-x0)*S,c.size[1])],fill=(0,160,255) if x%5 else (255,0,0))
    for y in range(y0,y1+2): d.line([(0,(y-y0)*S),(c.size[0],(y-y0)*S)],fill=(0,160,255) if y%5 else (255,0,0))
    c.save(out); print('rode lijnen op veelvouden van 5; links-boven =',x0,y0)
