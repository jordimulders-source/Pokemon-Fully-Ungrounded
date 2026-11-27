# vel.png: eind | r7A | model (8x); close-ups 12x; 1x/2x licht/donker; naast Gen 3
from lib import *
import os
E=lees('raster_e.txt'); A=lees('raster_r7A.txt')
PE=dict(PAL); PE.update(n=(32,44,70),d=(60,72,98),s=(84,104,136),m=(114,138,168))
ROOT=os.path.join(D,'../../../../../..')
def gen3(n,bgc):
    p=Image.open(os.path.join(ROOT,'graphics/pokemon/%s/anim_front_gba.png'%n)); pal=p.getpalette()
    im=Image.new('RGB',(64,64),bgc)
    for y in range(64):
        for x in range(64):
            i=p.getpixel((x,y))
            if i: im.putpixel((x,y),tuple(pal[3*i:3*i+3]))
    return im
def lab(im,t):
    d=ImageDraw.Draw(im); d.text((4,2),t,fill=(200,0,0)); return im
blocks=[]
# rij 1: 8x
r=[lab(grid(rgb(E,pal=PE).resize((512,512),Image.NEAREST),8,(225,225,225)),'eind'),
   lab(grid(rgb(A).resize((512,512),Image.NEAREST),8,(225,225,225)),'r7A'),
   lab(model_in_sprite(0,0,64,64,8),'model')]
blocks.append(r)
# close-ups 12x
for naam,(x0,y0,x1,y1) in [('geestvlam',(44,16,64,46)),('rechtervleugel',(36,26,58,42)),('linkerkop',(0,7,30,29)),
                          ('rechterkop',(28,1,52,24)),('kronkels',(2,40,52,64))]:
    s=12
    a=grid(rgb(E,pal=PE).crop((x0,y0,x1,y1)).resize(((x1-x0)*s,(y1-y0)*s),Image.NEAREST),s,(225,225,225))
    b=grid(rgb(A).crop((x0,y0,x1,y1)).resize(((x1-x0)*s,(y1-y0)*s),Image.NEAREST),s,(225,225,225))
    m=model_in_sprite(x0,y0,x1,y1,s)
    blocks.append([lab(a,naam+' eind'),lab(b,'r7A'),lab(m,'model')])
# 1x/2x licht/donker + gen3
klein=[]
for bgc in [(255,255,255),(40,40,48)]:
    e=rgb(E,bg=bgc,pal=PE); klein+= [e, e.resize((128,128),Image.NEAREST)]
g=[]
for bgc in [(255,255,255),(40,40,48)]:
    row=[rgb(E,bg=bgc,pal=PE).resize((128,128),Image.NEAREST)]+[gen3(n,bgc).resize((128,128),Image.NEAREST) for n in ['arbok','seviper','gyarados','milotic','rayquaza']]
    g.append(row)
W=max(sum(i.width for i in b)+10*len(b) for b in blocks)
H=sum(max(i.height for i in b)+10 for b in blocks)+140+2*138+20
V=Image.new('RGB',(W,H),(255,255,255)); y=0
for b in blocks:
    x=0
    for i in b: V.paste(i,(x,y)); x+=i.width+10
    y+=max(i.height for i in b)+10
x=0
for i in klein: V.paste(i,(x,y)); x+=i.width+10
y+=140
for row in g:
    x=0
    for i in row: V.paste(i,(x,y)); x+=138
    y+=138
V.save('vel.png'); print(V.size)
