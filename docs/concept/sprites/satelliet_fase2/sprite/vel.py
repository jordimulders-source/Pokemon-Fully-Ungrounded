# vel: sprite 8x | model verkleind (vlakgemiddelde, alleen ter vergelijking) 8x
#      close-ups 12x: oog | model, paneel | model, antennes | model ; onderaan 1x op licht/donker + model 1x
import numpy as np, sys; from PIL import Image, ImageDraw
SP=sys.argv[1]; UIT=sys.argv[2]; VORIG=sys.argv[3] if len(sys.argv)>3 else None
spr=Image.open(SP).convert('RGBA')
from cfg import MODEL, X0, Y0, s, TOP, oudrij, oudkol
M=Image.open(MODEL).convert('RGB')
mm=M.crop((X0,int(round(Y0-TOP*s)),int(round(X0+64*s)),int(round(Y0+(64-TOP)*s)))).resize((64,64),Image.BOX)
def big(im,f): return im.resize((im.width*f,im.height*f),Image.NEAREST)
def on(im,bg):
    b=Image.new('RGBA',im.size,bg+(255,)); b.alpha_composite(im); return b.convert('RGB')
def mcrop(x0,y0,x1,y1,f):   # model zelf (1024) op dezelfde uitsnede, raster erover
    c=M.crop((int(X0+x0*s),int(Y0+(y0-TOP)*s),int(X0+x1*s),int(Y0+(y1-TOP)*s))).resize(((x1-x0)*f,(y1-y0)*f),Image.LANCZOS)
    d=ImageDraw.Draw(c)
    for i in range(x1-x0+1): d.line([(i*f,0),(i*f,c.height)],fill=(255,0,0))
    for j in range(y1-y0+1): d.line([(0,j*f),(c.width,j*f)],fill=(255,0,0))
    return c
CL=[((12,22,30,40),'oog'),((38,14,58,32),'paneel'),((24,7,50,20),'antennes')]
CL=[((max(0,oudkol(a)),max(0,oudrij(b-7)+TOP),min(64,oudkol(c)),min(64,oudrij(d-7)+TOP)),n) for (a,b,c,d),n in CL]
hs=[(y1-y0)*12 for (x0,y0,x1,y1),_ in CL]
Wd=max(1064 if not VORIG else 1616,max(2*(x1-x0)*12+30 for (x0,y0,x1,y1),_ in CL))
out=Image.new('RGB',(Wd,530+sum(h+30 for h in hs)+90),(205,205,205)); d=ImageDraw.Draw(out)
out.paste(big(on(spr,(255,255,255)),8),(0,0)); out.paste(big(mm,8),(552,0))
d.text((4,514),'sprite 8x',fill=(0,0,0)); d.text((556,514),'model verkleind 8x (BOX, ter vergelijking)',fill=(0,0,0))
if VORIG:
    vr=Image.open(VORIG).convert('RGBA'); out.paste(big(on(vr,(255,255,255)),8),(1104,0)); d.text((1108,514),'vorige ronde 8x: '+VORIG,fill=(0,0,0))
y=530
for ((x0,y0,x1,y1),n),h in zip(CL,hs):
    a=big(on(spr.crop((x0,y0,x1,y1)),(255,255,255)),12); b=mcrop(x0,y0,x1,y1,12)
    d.text((4,y),'%s 12x  (x %d-%d, y %d-%d)'%(n,x0,x1,y0,y1),fill=(0,0,0)); out.paste(a,(0,y+14)); out.paste(b,(a.width+20,y+14)); y+=h+30
for n,bg in enumerate(((255,255,255),(232,232,216),(40,40,48),(0,0,0))): out.paste(on(spr,bg),(10+n*80,y+10))
if VORIG:
    for n,bg in enumerate(((255,255,255),(40,40,48))): out.paste(on(vr,bg),(500+n*80,y+10))
    d.text((500,y-4),'vorige 1x',fill=(0,0,0))
out.paste(mm,(10+4*80+30,y+10)); d.text((10,y-4),'1x: licht / creme / donker / zwart | model 1x',fill=(0,0,0))
out.save(UIT); print(UIT)
