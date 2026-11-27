# hulp: hi-res model (romp, niet vergroot) met spriteraster; sprite cel (y,x) -> modelpixel FX+(MX+3x)*PX
import sys; from PIL import Image,ImageDraw
im=Image.open('../referenties/gemini_gekozen_r7.png').convert('RGB')
PX,FX,PY,FY=5.704,5.16,5.692,3.088; MY,MX=-21,-2
y0,y1,x0,x1=[int(v) for v in sys.argv[1:5]]; Z=float(sys.argv[5]); uit=sys.argv[6]
fx=lambda x: FX+(MX+3*x)*PX; fy=lambda y: FY+(MY+3*y)*PY
c=im.crop((int(fx(x0)),int(fy(y0)),int(fx(x1)),int(fy(y1)))); ox,oy=int(fx(x0)),int(fy(y0))
c=c.resize((int(c.width*Z),int(c.height*Z)),Image.LANCZOS); d=ImageDraw.Draw(c)
for x in range(x0,x1+1): X=(fx(x)-ox)*Z; d.line([(X,0),(X,c.height)],fill=(255,0,255) if x%5==0 else (150,150,255))
for y in range(y0,y1+1): Y=(fy(y)-oy)*Z; d.line([(0,Y),(c.width,Y)],fill=(255,0,255) if y%5==0 else (150,150,255))
for x in range(x0,x1): d.text(((fx(x)-ox)*Z+2,2),str(x),fill=(0,0,0))
for y in range(y0,y1): d.text((2,(fy(y)-oy)*Z+2),str(y),fill=(0,0,0))
c.save(uit); print(c.size)
