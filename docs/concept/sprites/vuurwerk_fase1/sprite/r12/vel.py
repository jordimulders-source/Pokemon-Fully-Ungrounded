# _8x.png (op wit) per bestand + vel.png: r11 | stap1 | A | B | fase 3 op 8x, eronder 1x en 2x op licht en donker
from PIL import Image, ImageDraw
def rgba(fn): return Image.open(fn).convert('RGBA')   # bestanden zijn opgeslagen met transparency=0
def on(fn,bgc,z):
    a=rgba(fn); bg=Image.new('RGBA',a.size,bgc+(255,)); bg.alpha_composite(a); return bg.resize((a.width*z,a.height*z),Image.NEAREST).convert('RGB')
for f in ['stap1','A','B']: on(f+'.png',(255,255,255),8).save(f+'_8x.png')
F=[('r11','../r11/sprite.png'),('stap1','stap1.png'),('A','A.png'),('B','B.png'),('fase 3','../../../vuurwerk_fase3/af/vuurwerkslang.png')]
W=len(F)*(512+10)+10; Hh=20+512+10+64*2+20+10
V=Image.new('RGB',(W,Hh),(255,255,255)); d=ImageDraw.Draw(V)
for k,(n,f) in enumerate(F):
    x=10+k*522; d.text((x,4),n,fill=(0,0,0)); V.paste(on(f,(255,255,255),8),(x,20))
    y=20+512+10
    V.paste(on(f,(248,248,240),1),(x,y)); V.paste(on(f,(40,40,48),1),(x+70,y))
    V.paste(on(f,(248,248,240),2),(x+140,y)); V.paste(on(f,(40,40,48),2),(x+140+134,y))
V.save('vel.png'); print(V.size)
