import sys; from PIL import Image, ImageDraw
x0,y0,x1,y1,z=[int(v) for v in sys.argv[1:6]]; out=sys.argv[6]
m=Image.open('../../model/model.png').convert('RGB').crop((x0,y0,x1,y1)); m=m.resize(((x1-x0)*z//2,(y1-y0)*z//2),Image.NEAREST)
d=ImageDraw.Draw(m); f=z/2
for x in range((x0//25+1)*25,x1,25):
    d.line([((x-x0)*f,0),((x-x0)*f,m.height)],fill=(0,160,255) if x%100 else (255,0,255)); d.text(((x-x0)*f+2,2),str(x),fill=(0,0,200))
for y in range((y0//25+1)*25,y1,25):
    d.line([(0,(y-y0)*f),(m.width,(y-y0)*f)],fill=(0,160,255) if y%100 else (255,0,255)); d.text((2,(y-y0)*f+2),str(y),fill=(0,0,200))
m.save(out)
