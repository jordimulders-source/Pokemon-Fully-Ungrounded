# model crop with sprite-pixel grid: python3 mgrid.py x0 y0 x1 y1 out z
import sys; from PIL import Image,ImageDraw
S=968/62;m=Image.open('../../model/model.png').convert('RGB'); mw=Image.new('RGB',(1400,1400),'white'); mw.paste(m,(200,200))
x0,y0,x1,y1=[int(v) for v in sys.argv[1:5]]; out=sys.argv[5]; z=float(sys.argv[6])
box=(int(round(24+(x0-1)*S))+200,int(round(1+(y0-4)*S))+200,int(round(24+(x1-1)*S))+200,int(round(1+(y1-4)*S))+200)
c=mw.crop(box); c=c.resize((int(c.width*z),int(c.height*z)),Image.LANCZOS); P=S*z
c2=Image.new('RGB',(c.width+30,c.height+20),'white'); c2.paste(c,(30,20)); d=ImageDraw.Draw(c2)
for X in range(x0,x1+1):
    px=30+(X-x0)*P; d.line([(px,20),(px,20+c.height)],fill=(255,0,255) if X%5==0 else (150,200,255)); d.text((px+2,4),str(X%100),fill=(0,0,0))
for Y in range(y0,y1+1):
    py=20+(Y-y0)*P; d.line([(30,py),(30+c.width,py)],fill=(255,0,255) if Y%5==0 else (150,200,255)); d.text((2,py+2),str(Y),fill=(0,0,0))
c2.save(out)
