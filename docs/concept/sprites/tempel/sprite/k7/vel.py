import sys
from PIL import Image, ImageDraw
src=sys.argv[1] if len(sys.argv)>1 else 'tempel.png'; out=sys.argv[2] if len(sys.argv)>2 else 'vel.png'
REF='../k6/tempel.png'
M=Image.open('../../referenties/model.webp').convert('RGB'); s=(983-46)/62
def mcrop(x0,y0,x1,y1,z):
    return M.crop((int(46+(x0-1)*s),int(57+(y0-3)*s),int(46+(x1-1)*s),int(57+(y1-3)*s))).resize(((x1-x0)*z,(y1-y0)*z),Image.LANCZOS)
def op(p,bg,box=(0,0,64,64),z=8):
    im=Image.open(p).convert('RGBA').crop(box); b=Image.new('RGBA',im.size,bg+(255,)); b.alpha_composite(im)
    return b.convert('RGB').resize(((box[2]-box[0])*z,(box[3]-box[1])*z),Image.NEAREST)
A=(1,28,33,62); B=(36,8,62,62)  # gezichtsblok+linkervleugel, rechterzijvlakken
hA=(A[3]-A[1])*12; hB=(B[3]-B[1])*12
W=Image.new('RGB',(3*512+40,24+512+30+max(hA,hB)+30+200),(236,236,236)); d=ImageDraw.Draw(W)
W.paste(op(src,(255,255,255)),(10,24)); W.paste(op(REF,(255,255,255)),(532,24)); W.paste(mcrop(0,0,64,64,8),(1054,24))
for i,t in enumerate(['k7 (nieuw) 8x','k6 8x','model 8x']): d.text((10+i*522,6),t,fill=(0,0,0))
y=24+512+24
d.text((10,y-16),'12x: gezichtsblok + linkervleugel (x1-33,y28-62), k7 | k6',fill=(0,0,0))
W.paste(op(src,(255,255,255),A,12),(10,y)); W.paste(op(REF,(255,255,255),A,12),(10+(A[2]-A[0])*12+10,y))
x=10+2*(A[2]-A[0])*12+40
d.text((x,y-16),'12x: rechterzijvlakken (x36-62,y8-62), k7 | k6',fill=(0,0,0))
W.paste(op(src,(255,255,255),B,12),(x,y)); W.paste(op(REF,(255,255,255),B,12),(x+(B[2]-B[0])*12+10,y))
y2=y+max(hA,hB)+30
d.text((10,y2-16),'1x op licht en donker: boven k7, onder k6; rechts 2x',fill=(0,0,0))
for j,c in enumerate([(255,255,255),(232,232,224),(40,40,48),(16,16,20)]):
    W.paste(op(src,c,z=1),(10+j*74,y2)); W.paste(op(REF,c,z=1),(10+j*74,y2+74))
    W.paste(op(src,c,z=2),(320+j*136,y2)); 
W.save(out)
