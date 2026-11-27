# overlay.py sprite_I.npy out x0 y0 x1 y1 Z : hoge-res model op spriteraster | sprite, rasters per pixel
import sys; sys.path.insert(0,'../sprite')
import numpy as np
from PIL import Image,ImageDraw
from reduceer import X0,Y0,s,LEFT,TOP
from basis import PAL
k=10.24
I=np.load(sys.argv[1]); x0,y0,x1,y1,Z=map(int,sys.argv[3:8])
M=Image.open('../model.png').convert('RGB')
def mx(x): return (X0+(x-LEFT)*s)*k
def my(y): return (Y0+(y-TOP)*s)*k
A=M.crop((int(mx(x0)),int(my(y0)),int(mx(x1)),int(my(y1)))).resize(((x1-x0)*Z,(y1-y0)*Z),Image.LANCZOS)
P=np.array([(255,255,255)]+list(PAL[1:]),dtype='uint8')
B=Image.fromarray(P[I[y0:y1,x0:x1]]).resize(A.size,Image.NEAREST)
for im in (A,B):
    d=ImageDraw.Draw(im)
    for X in range(x0,x1+1): d.line([((X-x0)*Z,0),((X-x0)*Z,im.height)],fill=(255,0,255) if X%5==0 else (150,150,255))
    for Y in range(y0,y1+1): d.line([(0,(Y-y0)*Z),(im.width,(Y-y0)*Z)],fill=(255,0,255) if Y%5==0 else (150,150,255))
    for X in range(x0,x1):
        if X%5==0: d.text(((X-x0)*Z+2,2),str(X),fill=(255,0,0))
    for Y in range(y0,y1):
        if Y%5==0: d.text((2,(Y-y0)*Z+2),str(Y),fill=(255,0,0))
o=Image.new('RGB',(A.width*2+10,A.height),'white'); o.paste(A,(0,0)); o.paste(B,(A.width+10,0)); o.save(sys.argv[2])
