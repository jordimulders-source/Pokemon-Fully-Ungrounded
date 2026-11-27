# hulp: hi-res model (gezicht) met het spriteraster (vergroot gezicht) erover. sprite cel -> modelpixel via hoofdgroot-mapping
import sys; from PIL import Image,ImageDraw
im=Image.open('../../referenties/gemini_gekozen_r7.png').convert('RGB')
PX,FX,PY,FY=5.704,5.16,5.692,3.088
y0,y1,x0,x1=[int(v) for v in sys.argv[1:5]]; Z=float(sys.argv[5]); uit=sys.argv[6]
fx=lambda sx: FX+(63+(3*sx-64)/1.28)*PX; fy=lambda sy: FY+(22+(3*sy-37)/1.28)*PY
c=im.crop((int(fx(x0)),int(fy(y0)),int(fx(x1)),int(fy(y1)))); ox,oy=int(fx(x0)),int(fy(y0))
c=c.resize((int(c.width*Z),int(c.height*Z)),Image.LANCZOS); d=ImageDraw.Draw(c)
for sx in range(x0,x1+1): X=(fx(sx)-ox)*Z; d.line([(X,0),(X,c.height)],fill=(255,0,255) if sx%5==0 else (120,120,255))
for sy in range(y0,y1+1): Y=(fy(sy)-oy)*Z; d.line([(0,Y),(c.width,Y)],fill=(255,0,255) if sy%5==0 else (120,120,255))
for sx in range(x0,x1): d.text(((fx(sx)-ox)*Z+2,2),str(sx),fill=(255,255,0))
for sy in range(y0,y1): d.text((2,(fy(sy)-oy)*Z+2),str(sy),fill=(0,255,0))
c.save(uit); print(c.size)
