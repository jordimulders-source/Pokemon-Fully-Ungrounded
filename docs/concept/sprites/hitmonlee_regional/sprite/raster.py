# raster.py x0 y0 x1 y1 uit.png [idx.npy pal-script]: natief model met het spritepixelraster erover (sprite-coord. erbij),
# geschrapte rijen/kolommen grijs gearceerd; optioneel de sprite ernaast op dezelfde schaal.
from PIL import Image, ImageDraw; import numpy as np, sys
D='docs/concept/sprites/hitmonlee_regional/sprite/'
RD=[4,8,13,17,22,28,45,55,64,70]; CD=[1,5,16,37,42,50,56,60,65]
keepr=[r for r in range(74) if r not in RD]; keepc=[c for c in range(68) if c not in CD]
x0,y0,x1,y1=map(int,sys.argv[1:5]); S=10
nat=np.asarray(Image.open(D+'natief.png').convert('RGB'))
c0,c1=keepc[x0],keepc[x1-1]+1; r0,r1=keepr[y0],keepr[y1-1]+1
sub=nat[2*r0:2*r1,2*c0:2*c1]
im=Image.fromarray(sub).resize((sub.shape[1]*S,sub.shape[0]*S),Image.NEAREST); dr=ImageDraw.Draw(im,'RGBA')
for c in range(c0,c1):
    X=(c-c0)*2*S
    if c in CD: dr.rectangle([X,0,X+2*S,im.height],fill=(0,0,0,90))
    else: dr.text((X+2,2),str(keepc.index(c)),fill=(0,0,255))
    dr.line([X,0,X,im.height],fill=(0,0,255,120))
for r in range(r0,r1):
    Y=(r-r0)*2*S
    if r in RD: dr.rectangle([0,Y,im.width,Y+2*S],fill=(0,0,0,90))
    else: dr.text((2,Y+2),str(keepr.index(r)),fill=(0,0,255))
    dr.line([0,Y,im.width,Y],fill=(0,0,255,120))
out=im
if len(sys.argv)>6:
    L=np.load(sys.argv[6]); PAL=eval(open(sys.argv[7]).read().split('PAL=')[1].split(']')[0]+']')
    T=2*S; sp=Image.new('RGB',((x1-x0)*T,(y1-y0)*T),'white'); d2=ImageDraw.Draw(sp)
    for y in range(y0,y1):
        for x in range(x0,x1):
            if L[y,x]: d2.rectangle([(x-x0)*T,(y-y0)*T,(x-x0)*T+T-1,(y-y0)*T+T-1],fill=tuple(PAL[L[y,x]]))
    for x in range(x0,x1+1): d2.line([(x-x0)*T,0,(x-x0)*T,sp.height],fill=(190,190,190))
    for y in range(y0,y1+1): d2.line([0,(y-y0)*T,sp.width,(y-y0)*T],fill=(190,190,190))
    for x in range(x0,x1): d2.text(((x-x0)*T+2,2),str(x),fill=(0,0,255))
    for y in range(y0,y1): d2.text((2,(y-y0)*T+2),str(y),fill=(0,0,255))
    out=Image.new('RGB',(im.width+sp.width+10,max(im.height,sp.height)),(150,150,150)); out.paste(im,(0,0)); out.paste(sp,(im.width+10,0))
out.save(sys.argv[5])
