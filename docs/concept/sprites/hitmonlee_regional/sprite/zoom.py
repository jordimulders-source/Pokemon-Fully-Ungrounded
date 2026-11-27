# zoom.py <idx.npy> <pal-bouwscript> x0 y0 x1 y1 uit.png : sprite-uitsnede op 12x naast het natieve model (6x) met raster
from PIL import Image, ImageDraw; import numpy as np, sys, importlib.util
D='docs/concept/sprites/hitmonlee_regional/sprite/'
RD=[4,8,13,17,22,28,45,55,64,70]; CD=[1,5,16,37,42,50,56,60,65]
keepr=[r for r in range(74) if r not in RD]; keepc=[c for c in range(68) if c not in CD]
def model_zoom(x0,y0,x1,y1):
    nat=Image.open(D+'natief.png').convert('RGB')
    a,b=2*keepc[x0],2*keepc[x1-1]+2; c,d=2*keepr[y0],2*keepr[y1-1]+2
    im=nat.crop((a,c,b,d)).resize(((b-a)*6,(d-c)*6),Image.NEAREST)
    return im
def sprite_zoom(L,PAL,x0,y0,x1,y1,S=12):
    sub=L[y0:y1,x0:x1]; h,w=sub.shape
    im=Image.new('RGB',(w*S,h*S),'white'); dr=ImageDraw.Draw(im)
    for y in range(h):
        for x in range(w):
            if sub[y,x]: dr.rectangle([x*S,y*S,x*S+S-1,y*S+S-1],fill=tuple(PAL[sub[y,x]]))
    for x in range(w+1): dr.line([x*S,0,x*S,h*S],fill=(200,200,200))
    for y in range(h+1): dr.line([0,y*S,w*S,y*S],fill=(200,200,200))
    for x in range(0,w,5): dr.text((x*S+2,2),str(x+x0),fill=(0,0,255))
    for y in range(0,h,5): dr.text((2,y*S+2),str(y+y0),fill=(0,0,255))
    return im
if __name__=='__main__':
    L=np.load(sys.argv[1]); PAL=eval(open(sys.argv[2]).read().split('PAL=')[1].split(']')[0]+']')
    x0,y0,x1,y1=map(int,sys.argv[3:7])
    a=sprite_zoom(L,PAL,x0,y0,x1,y1); b=model_zoom(x0,y0,x1,y1)
    c=Image.new('RGB',(a.width+b.width+10,max(a.height,b.height)),(180,180,180)); c.paste(a,(0,0)); c.paste(b,(a.width+10,0)); c.save(sys.argv[7])
