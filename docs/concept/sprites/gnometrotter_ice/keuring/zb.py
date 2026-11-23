import sys; sys.path.insert(0,'../../gnometrotter_rock/sprite')
from kijk import model_op_schaal, sprite
from PIL import Image, ImageDraw, ImageFont
S=16; x0,y0,x1,y1=[int(v) for v in sys.argv[2:6]]
m=model_op_schaal(sys.argv[1],64*S).crop((x0*S,y0*S,x1*S,y1*S))
s=sprite(sys.argv[6]).resize((64*S,64*S),Image.NEAREST).crop((x0*S,y0*S,x1*S,y1*S))
W=Image.new('RGB',(m.width*2+10,m.height),'white'); W.paste(s,(0,0)); W.paste(m,(m.width+10,0))
d=ImageDraw.Draw(W)
for off in (0,m.width+10):
  for x in range(x0,x1+1):
    c=(255,0,0) if x%5==0 else (255,200,200); d.line([(off+(x-x0)*S,0),(off+(x-x0)*S,W.height)],fill=c)
    if x%5==0: d.text((off+(x-x0)*S+2,2),str(x),fill=(255,0,0))
  for y in range(y0,y1+1):
    c=(255,0,0) if y%5==0 else (255,200,200); d.line([(off,(y-y0)*S),(off+m.width,(y-y0)*S)],fill=c)
    if y%5==0: d.text((off+2,(y-y0)*S+2),str(y),fill=(255,0,0))
W.save(sys.argv[7])
