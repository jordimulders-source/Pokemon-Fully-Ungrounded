# gereedschap r7: model op spriteschaal (meta r6: ox=165+x*S, oy=86+(y-14)*S)
import sys,numpy as np
from PIL import Image,ImageDraw
V='/home/user/Pokemon-Fully-Ungrounded/docs/concept/sprites/viscacha/'
D=V+'kleur_r7/'
sys.path.insert(0,D); from palet import PAL
X0,Y0,S,OX,OY=np.load(D+'meta.npy')
SRC=Image.open(V+'referenties/gemini_gekozen_ronde6.png').convert('RGB')
A=np.asarray(SRC).astype(float); LUM=A.mean(2)
def mbox(x,y):
    return (X0+(x-OX)*S, Y0+(y-OY)*S)
def model(x0,y0,x1,y1,z):
    a,b=mbox(x0,y0); c,d=mbox(x1,y1)
    w,h=int(c)-int(a),int(d)-int(b); cv=Image.new('RGB',(w,h),'white'); cv.paste(SRC,(-int(a),-int(b)))
    return cv.resize(((x1-x0)*z,(y1-y0)*z),Image.LANCZOS)
def raster(f): return [l.rstrip('\n').ljust(64,'.')[:64] for l in open(f)][:64]
def rimg(R,bg=(255,255,255)):
    im=Image.new('RGB',(64,64)); im.putdata([bg if c=='.' else PAL[int(c,16)] for r in R for c in r]); return im
def grid(im,x0,y0,z,col=(0,170,0)):
    im=im.copy(); d=ImageDraw.Draw(im)
    for i in range(0,im.width//z+1):
        c=col if (x0+i)%5==0 else (200,200,200)
        if z>=8 or (x0+i)%5==0: d.line([(i*z,0),(i*z,im.height)],fill=c)
        if (x0+i)%5==0: d.text((i*z+1,1),str(x0+i),fill=(0,120,0))
    for j in range(0,im.height//z+1):
        c=col if (y0+j)%5==0 else (200,200,200)
        if z>=8 or (y0+j)%5==0: d.line([(0,j*z),(im.width,j*z)],fill=c)
        if (y0+j)%5==0: d.text((1,j*z+1),str(y0+j),fill=(0,120,0))
    return im
