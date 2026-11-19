# Vel r4: model | r4 | r3B met nieuw palet | r3B (8x, zelfde hoogte) · kop 12x: model op spriteraster | r4 | r3B · 1x/2x op licht en donker
from PIL import Image, ImageDraw
import subprocess
m=Image.open('../../../model/model.png').convert('RGBA')
H=48*8; mm=m.crop((232,28,814,881)); mm=mm.resize((int(mm.width*H/mm.height),H))
P=['../palpaca.png','../r3B_nieuwpalet.png','../../r3/palpaca_B.png']; T=['r4','r3B, alleen nieuw palet','r3B']
sp=[Image.open(p).convert('RGBA') for p in P]
subprocess.run(['python3','modelkop.py','15','35','14','35','modelkop_12x.png'],check=True)
mk=Image.open('modelkop_12x.png').convert('RGBA')
W=Image.new('RGBA',(mm.width+3*310+20,20+H+30+260+30+150),(255,255,255,255)); d=ImageDraw.Draw(W)
W.paste(mm,(0,20),mm); d.text((2,4),'model',fill=(0,0,0))
for i,(im,t) in enumerate(zip(sp,T)):
    z=im.crop((14,14,50,62)).resize((288,384),Image.NEAREST); x=mm.width+20+i*310; W.paste(z,(x,20),z); d.text((x,4),t+' 8x',fill=(0,0,0))
y=20+H+30
for i,(im,t) in enumerate([(mk,'model op spriteraster'),(sp[0],'r4'),(sp[2],'r3B')]):
    z=im if i==0 else im.crop((15,14,35,35)).resize((240,252),Image.NEAREST)
    W.paste(z,(i*260,y),z); d.text((i*260,y-14),t+' kop 12x (x15-34, y14-34)',fill=(0,0,0))
y+=290
for j,bg in enumerate([(248,248,248,255),(40,40,48,255)]):
    x0=j*520; d.rectangle([x0,y,x0+510,y+140],fill=bg)
    for k,im in enumerate([sp[0],sp[2]]):
        W.paste(im,(x0+10+k*70,y+10),im); z=im.resize((128,128),Image.NEAREST); W.paste(z,(x0+160+k*170,y+6),z)
d.text((2,y-14),'1x en 2x op licht en donker: r4, r3B',fill=(0,0,0))
W.save('../vel.png'); print(W.size)
