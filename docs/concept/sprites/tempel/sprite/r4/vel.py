# vel.py nieuw.png vorig.png out.png : rN | r3 | model op 8x, gevelzone op 12x (rN | model), 1x op licht en donker
import sys, numpy as np
from PIL import Image, ImageDraw
M='/home/user/Pokemon-Fully-Ungrounded/docs/concept/sprites/tempel/referenties/model.webp'
s=(983-46)/62; X0,Y0,left,top=46,57,1,3
src=Image.open(M).convert('RGB')
def modelcrop(x0,y0,x1,y1,z):
    return src.crop((int(X0+(x0-left)*s),int(Y0+(y0-top)*s),int(X0+(x1-left)*s),int(Y0+(y1-top)*s))).resize(((x1-x0)*z,(y1-y0)*z),Image.LANCZOS)
def rgba(p):
    im=Image.open(p)
    if im.mode=='P': im=im.convert('RGBA')
    return im
def on(im,col):
    b=Image.new('RGBA',im.size,col+(255,)); b.alpha_composite(im); return b.convert('RGB')
A=rgba(sys.argv[1]); B=rgba(sys.argv[2])
W=512*3+16; FX,FY,FX1,FY1=16,2,42,28  # gevelzone + topgevels
fz=12; fw=(FX1-FX)*fz; fh=(FY1-FY)*fz
o=Image.new('RGB',(W,512+8+fh+8+140),(255,255,255))
o.paste(on(A,(255,255,255)).resize((512,512),Image.NEAREST),(0,0))
o.paste(on(B,(255,255,255)).resize((512,512),Image.NEAREST),(520,0))
o.paste(modelcrop(0,0,64,64,8),(1040,0))
o.paste(on(A.crop((FX,FY,FX1,FY1)),(255,255,255)).resize((fw,fh),Image.NEAREST),(0,520))
o.paste(modelcrop(FX,FY,FX1,FY1,fz),(fw+8,520))
y=520+fh+8
o.paste(on(A,(255,255,255)),(0,y)); o.paste(on(A,(40,40,48)),(72,y)); o.paste(on(A,(152,208,160)),(144,y))
o.paste(on(A,(255,255,255)).resize((128,128),Image.NEAREST),(230,y)); o.paste(on(A,(40,40,48)).resize((128,128),Image.NEAREST),(366,y))
o.save(sys.argv[3])
