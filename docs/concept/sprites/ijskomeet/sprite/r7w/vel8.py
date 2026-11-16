import sys; sys.path.insert(0,'r7w')
from proj import *; from PIL import ImageDraw
def wit(p,s,bg=(255,255,255)):
    im=Image.open(p).convert('RGBA').resize((64*s,64*s),0); b=Image.new('RGBA',im.size,bg+(255,)); b.alpha_composite(im); return b.convert('RGB')
def crop12(src,y0,y1,x0,x1):
    if src=='model': return model_s(12).crop((x0*12,y0*12,x1*12,y1*12)).convert('RGB')
    return wit(src,12).crop((x0*12,y0*12,x1*12,y1*12))
W=Image.new('RGB',(1600,1820),'white'); d=ImageDraw.Draw(W)
for k,(im,t) in enumerate([(wit('r8.png',8),'r8'),(wit('r5.png',8),'r5'),(model_s(8).convert('RGB'),'model (r5-uitlijning)')]):
    W.paste(im,(10+k*530,24)); d.text((10+k*530,6),t,fill=0)
y=560; d.text((10,y),'schotsen 12x: model | r8',fill=0)
a=crop12('model',36,61,0,36); b=crop12('r8.png',36,61,0,36); W.paste(a,(10,y+18)); W.paste(b,(10+a.width+10,y+18))
y2=y+18+a.height+12; d.text((10,y2),'kop 12x: model | r8',fill=0)
a=crop12('model',22,40,0,24); b=crop12('r8.png',22,40,0,24); W.paste(a,(10,y2+18)); W.paste(b,(10+a.width+10,y2+18))
x3=10+2*a.width+40; d.text((x3,y2),'kern 12x: model | r8',fill=0)
a=crop12('model',25,41,19,34); b=crop12('r8.png',25,41,19,34); W.paste(a,(x3,y2+18)); W.paste(b,(x3+a.width+10,y2+18))
y3=y2+18+18*12+16; x=10
for bg in [(255,255,255),(40,40,48)]:
    for s in (1,2):
        W.paste(wit('r8.png',s,bg),(x,y3)); x+=64*s+12
d.text((x+10,y3),'1x/2x licht en donker',fill=0)
W.save('vel_r8.png'); print(W.size, y3+140)
