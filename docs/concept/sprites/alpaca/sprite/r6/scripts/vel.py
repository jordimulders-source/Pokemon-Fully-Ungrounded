# Vel r6: model | r6 | r5 (8x, zelfde hoogte) · torso 12x: model op spriteraster | r6 | r5 · kop 12x: r6 | r5 · 1x/2x licht en donker
from PIL import Image, ImageDraw
import subprocess
m=Image.open('../../../model/model.png').convert('RGBA')
H=48*8; mm=m.crop((232,28,814,881)); mm=mm.resize((int(mm.width*H/mm.height),H))
sp=[Image.open(p).convert('RGBA') for p in ['../palpaca.png','../../r5/palpaca.png']]; T=['r6','r5']
TX0,TX1,TY0,TY1=16,47,36,52   # torso-uitsnede
subprocess.run(['python3','modelkop.py',str(TX0),str(TX1),str(TY0),str(TY1),'modeltorso_12x.png'],check=True)
mt=Image.open('modeltorso_12x.png').convert('RGBA')
tw,th=(TX1-TX0)*12,(TY1-TY0)*12
W=Image.new('RGBA',(max(mm.width+2*310+20,3*(tw+20)),20+H+30+th+40+252+40+150),(255,255,255,255)); d=ImageDraw.Draw(W)
W.paste(mm,(0,20),mm); d.text((2,4),'model',fill=(0,0,0))
for i,(im,t) in enumerate(zip(sp,T)):
    z=im.crop((14,14,50,62)).resize((288,384),Image.NEAREST); x=mm.width+20+i*310; W.paste(z,(x,20),z); d.text((x,4),t+' 8x',fill=(0,0,0))
def grid(z,k):
    g=Image.new('RGBA',z.size,(205,220,250,255)); g.alpha_composite(z); dd=ImageDraw.Draw(g)
    for X in range(0,z.width,k): dd.line([(X,0),(X,z.height)],fill=(160,160,170,255))
    for Y in range(0,z.height,k): dd.line([(0,Y),(z.width,Y)],fill=(160,160,170,255))
    return g
y=20+H+30
for i,(im,t) in enumerate([(mt,'model op spriteraster'),(sp[0],'r6'),(sp[1],'r5')]):
    z=im if i==0 else grid(im.crop((TX0,TY0,TX1,TY1)).resize((tw,th),Image.NEAREST),12)
    W.paste(z,(i*(tw+20),y),z); d.text((i*(tw+20),y-14),t+' torso 12x (x%d-%d, y%d-%d)'%(TX0,TX1-1,TY0,TY1-1),fill=(0,0,0))
y+=th+40
for i,(im,t) in enumerate(zip(sp,T)):
    z=grid(im.crop((15,14,35,35)).resize((240,252),Image.NEAREST),12); W.paste(z,(i*260,y),z); d.text((i*260,y-14),t+' kop 12x (x15-34, y14-34)',fill=(0,0,0))
y+=252+40
for j,bg in enumerate([(248,248,248,255),(40,40,48,255)]):
    x0=j*520; d.rectangle([x0,y,x0+510,y+140],fill=bg)
    for k,im in enumerate(sp):
        W.paste(im,(x0+10+k*70,y+10),im); z=im.resize((128,128),Image.NEAREST); W.paste(z,(x0+160+k*170,y+6),z)
d.text((2,y-14),'1x en 2x op licht en donker: r6, r5',fill=(0,0,0))
W.save('../vel.png'); print(W.size)
