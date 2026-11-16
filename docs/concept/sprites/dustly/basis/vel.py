# basis/vel.png: model (natief, uitsnede) | kale reductie | rode omtrek van de reductie over het model
from PIL import Image, ImageDraw; import numpy as np
n=Image.open('basis/natief.png').convert('RGB').crop((17,18,86,81)).resize((69*12,63*12),Image.NEAREST)
k=np.load('basis/kaal_idx.npy'); C=np.load('basis/modelpalet.npy').astype('uint8')
rgb=np.full(k.shape+(3,),255,'uint8'); rgb[k>=0]=C[k[k>=0]]
r=Image.fromarray(rgb).resize((46*18,42*18),Image.NEAREST)
ov=n.copy(); d=ImageDraw.Draw(ov); m=k>=0; S=18
for y in range(42):
    for x in range(46):
        if not m[y,x]: continue
        for dy,dx,seg in ((0,-1,[(x*S,y*S),(x*S,y*S+S)]),(0,1,[(x*S+S,y*S),(x*S+S,y*S+S)]),(-1,0,[(x*S,y*S),(x*S+S,y*S)]),(1,0,[(x*S,y*S+S),(x*S+S,y*S+S)])):
            yy,xx=y+dy,x+dx
            if not(0<=yy<42 and 0<=xx<46) or not m[yy,xx]: d.line(seg,fill=(230,0,0),width=3)
W=n.width; out=Image.new('RGB',(3*W+40,n.height),(255,255,255))
for i,c in enumerate((n,r,ov)): out.paste(c,(i*(W+20),0))
out.resize((out.width//2,out.height//2),Image.LANCZOS).save('basis/vel.png')
