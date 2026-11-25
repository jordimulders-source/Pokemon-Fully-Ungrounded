import sys
from PIL import Image, ImageDraw
src='tempel.png'; K7='../k7/tempel.png'; K6='../k6/tempel.png'
M=Image.open('../../referenties/model.webp').convert('RGB'); s=(983-46)/62
def mcrop(x0,y0,x1,y1,z):
    return M.crop((int(46+(x0-1)*s),int(57+(y0-3)*s),int(46+(x1-1)*s),int(57+(y1-3)*s))).resize(((x1-x0)*z,(y1-y0)*z),Image.LANCZOS)
def op(p,bg,box=(0,0,64,64),z=8):
    im=Image.open(p).convert('RGBA').crop(box); b=Image.new('RGBA',im.size,bg+(255,)); b.alpha_composite(im)
    return b.convert('RGB').resize(((box[2]-box[0])*z,(box[3]-box[1])*z),Image.NEAREST)
A=(1,28,33,62); B=(36,8,62,62)
wA=(A[2]-A[0])*12; wB=(B[2]-B[0])*12; hA=(A[3]-A[1])*12; hB=(B[3]-B[1])*12
W=Image.new('RGB',(4*522+10,24+512+40+hA+40+hB+40+180),(236,236,236)); d=ImageDraw.Draw(W)
for i,(p,t) in enumerate([(src,'k8 (nieuw)'),(K7,'k7'),(K6,'k6')]):
    W.paste(op(p,(255,255,255)),(10+i*522,24)); d.text((10+i*522,6),t+' 8x',fill=(0,0,0))
W.paste(mcrop(0,0,64,64,8),(10+3*522,24)); d.text((10+3*522,6),'model 8x',fill=(0,0,0))
y=24+512+30
d.text((10,y-16),'12x gezichtsblok + linkervleugel (x1-33,y28-62): k8 | k7 | k6',fill=(0,0,0))
for i,p in enumerate([src,K7,K6]): W.paste(op(p,(255,255,255),A,12),(10+i*(wA+10),y))
y+=hA+30
d.text((10,y-16),'12x rechterzijvlakken (x36-62,y8-62): k8 | k7 | k6',fill=(0,0,0))
for i,p in enumerate([src,K7,K6]): W.paste(op(p,(255,255,255),B,12),(10+i*(wB+10),y))
y+=hB+30
d.text((10,y-16),'1x op licht en donker: k8 | k7 | k6 ; rechts k8 2x',fill=(0,0,0))
for j,c in enumerate([(255,255,255),(232,232,224),(40,40,48),(16,16,20)]):
    for i,p in enumerate([src,K7,K6]): W.paste(op(p,c,z=1),(10+i*290+j*70,y))
    W.paste(op(src,c,z=2),(900+j*136,y))
W.save('vel.png')
