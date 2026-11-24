import sys
from PIL import Image, ImageDraw
src=sys.argv[1] if len(sys.argv)>1 else 'tempel.png'; out=sys.argv[2] if len(sys.argv)>2 else 'vel.png'
M=Image.open('../../referenties/model.webp').convert('RGB'); s=(983-46)/62
def mcrop(x0,y0,x1,y1,z):
    return M.crop((int(46+(x0-1)*s),int(57+(y0-3)*s),int(46+(x1-1)*s),int(57+(y1-3)*s))).resize(((x1-x0)*z,(y1-y0)*z),Image.LANCZOS)
def op(p,bg,box=(0,0,64,64),z=8):
    im=Image.open(p).convert('RGBA').crop(box); b=Image.new('RGBA',im.size,bg+(255,)); b.alpha_composite(im)
    return b.convert('RGB').resize(((box[2]-box[0])*z,(box[3]-box[1])*z),Image.NEAREST)
W=Image.new('RGB',(3*512+40,512+30+61*12+30+150),(236,236,236)); d=ImageDraw.Draw(W)
W.paste(op(src,(255,255,255)),(10,24)); W.paste(op('../k4/tempel.png',(255,255,255)),(532,24)); W.paste(mcrop(0,0,64,64,8),(1054,24))
for i,t in enumerate(['k5 (nieuw) 8x','k4 8x','model 8x']): d.text((10+i*522,6),t,fill=(0,0,0))
y=24+512+24
d.text((10,y-16),'rechterhelft x32-64, y2-63 op 12x: k5 | model',fill=(0,0,0))
W.paste(op(src,(255,255,255),(32,2,64,63),12),(10,y)); W.paste(mcrop(32,2,64,63,12),(10+32*12+10,y))
x=10+64*12+40
for j,c in enumerate([(255,255,255),(40,40,48),(152,208,160)]):
    W.paste(op(src,c,z=1),(x+j*74,y+20)); W.paste(op('../k4/tempel.png',c,z=1),(x+j*74,y+100))
    W.paste(op(src,c,z=2),(x+j*140,y+200)); W.paste(op('../k4/tempel.png',c,z=2),(x+j*140,y+340))
d.text((x,y),'1x: boven k5, onder k4',fill=(0,0,0)); d.text((x,y+182),'2x: boven k5, onder k4',fill=(0,0,0))
W.save(out)
