# C_8x.png + vel.png: B | C | fase 3 op 8x; kop-close-ups 12x B/C/fase 3; 1x/2x licht/donker
from PIL import Image, ImageDraw
F3='../../../vuurwerk_fase3/af/vuurwerkslang.png'
def on(fn,bgc,z,box=None):
    a=Image.open(fn).convert('RGBA'); bg=Image.new('RGBA',a.size,bgc+(255,)); bg.alpha_composite(a)
    if box: bg=bg.crop(box)
    return bg.resize((bg.width*z,bg.height*z),Image.NEAREST).convert('RGB')
on('C.png',(255,255,255),8).save('C_8x.png')
F=[('B','../r12/B.png',(27,0,52,23)),('C','C.png',(27,0,52,23)),('fase 3',F3,(0,0,30,32))]
W=3*522+10; V=Image.new('RGB',(W,20+512+20+32*12+20+128+10),'white'); d=ImageDraw.Draw(V)
for k,(n,f,box) in enumerate(F):
    x=10+k*522; d.text((x,4),n,fill=(0,0,0)); V.paste(on(f,(255,255,255),8),(x,20))
    y=20+512+20; d.text((x,y-14),n+' kop 12x',fill=(0,0,0)); V.paste(on(f,(255,255,255),12,box),(x,y))
    y+=32*12+20
    V.paste(on(f,(248,248,240),1),(x,y)); V.paste(on(f,(40,40,48),1),(x+70,y))
    V.paste(on(f,(248,248,240),2),(x+140,y)); V.paste(on(f,(40,40,48),2),(x+274,y))
V.save('vel.png'); print(V.size)
