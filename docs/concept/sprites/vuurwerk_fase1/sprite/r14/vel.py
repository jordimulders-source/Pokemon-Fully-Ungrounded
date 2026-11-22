# sprite_8x.png + vel.png: r14 | B | fase 3 op 8x; palet voor/na met luma; 1x/2x licht/donker
from PIL import Image, ImageDraw
F3='../../../vuurwerk_fase3/af/vuurwerkslang.png'
def on(fn,bgc,z):
    a=Image.open(fn).convert('RGBA'); bg=Image.new('RGBA',a.size,bgc+(255,)); bg.alpha_composite(a)
    return bg.resize((a.width*z,a.height*z),Image.NEAREST).convert('RGB')
on('sprite.png',(255,255,255),8).save('sprite_8x.png')
F=[('r14','sprite.png'),('B (r12)','../r12/B.png'),('fase 3',F3)]
V=Image.new('RGB',(3*522+10,20+512+20+150+20+128+10),'white'); d=ImageDraw.Draw(V)
NM={'sprite.png':'# D d s m l r M p Y S c k b w'.split(),'../r12/B.png':'# E d s m l r M p Y t c k b w'.split(),F3:None}
for k,(n,f) in enumerate(F):
    x=10+k*522; d.text((x,4),n,fill=(0,0,0)); V.paste(on(f,(255,255,255),8),(x,20))
    im=Image.open(f); pal=im.getpalette()[:48]; used=set(im.getdata())
    y=20+512+16; d.text((x,y-12),'palet (index: luma)',fill=(0,0,0))
    for i in range(1,16):
        rgb=tuple(pal[i*3:i*3+3]); L=int(.3*rgb[0]+.59*rgb[1]+.11*rgb[2])
        xx=x+((i-1)%8)*62; yy=y+((i-1)//8)*70
        d.rectangle([xx,yy,xx+28,yy+28],fill=rgb if i in used else (255,255,255),outline=(0,0,0))
        lab=(NM[f][i-1] if NM[f] else str(i))+' '+str(L)+('' if i in used else ' -')
        d.text((xx,yy+32),lab,fill=(0,0,0))
    y=20+512+20+150+20
    V.paste(on(f,(248,248,240),1),(x,y)); V.paste(on(f,(40,40,48),1),(x+70,y))
    V.paste(on(f,(248,248,240),2),(x+140,y)); V.paste(on(f,(40,40,48),2),(x+274,y))
V.save('vel.png'); print(V.size)
