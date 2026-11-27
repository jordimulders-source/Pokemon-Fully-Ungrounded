# vel.py r9: python3 sprite_r9/vel.py  (vanuit starmie/)
# rij 1 (8x): r9 | r8_A | r7  (wijzigingen r9 t.o.v. r8_A blauw omkaderd), rechts 12x close-up bovenpunt r9 | r8_A | model
# rij 2: 2x en 1x op wit en donker: r9, r8_A, r7, model, Gen 3 Starmie, regionale Staryu
import sys, numpy as np; from PIL import Image, ImageDraw
sys.path.insert(0,'gereedschap'); sys.path.insert(0,'sprite_r5/gereedschap'); import gemeen, voor_r4; gemeen.natief=voor_r4.natief
R='../../'; G='../../../../../graphics/pokemon/'
def rgb(im,bg):
    o=np.asarray(im)[:64,:64]; pal=np.array(im.getpalette()[:48]).reshape(-1,3); img=np.zeros((64,64,3),'uint8'); img[:]=bg
    for k in range(1,16): img[o==k]=pal[k]
    return Image.fromarray(img)
def g3(n,bg):
    im=Image.open(G+n+'/anim_front_gba.png'); pal=[tuple(int(v) for v in l.split()) for l in open(G+n+'/normal_gba.pal').read().split('\n')[3:19]]
    o=np.asarray(im)[:64,:64]; img=np.zeros((64,64,3),'uint8'); img[:]=bg
    for k in range(1,16): img[o==k]=pal[k]
    return Image.fromarray(img)
def png(p,bg):
    im=Image.open(p)
    if im.mode=='P': return rgb(im,bg)
    im=im.convert('RGBA'); b=Image.new('RGBA',im.size,bg+(255,)); b.alpha_composite(im); return b.convert('RGB').crop((0,0,64,64))
r9=Image.open('sprite_r9/starmie_r9.png'); r8=Image.open('sprite_r8/starmie_r8_A.png'); r7=Image.open('sprite_r7/starmie_r7.png'); m=gemeen.model_op_schaal()
diff=np.asarray(r9)!=np.asarray(r8)
WIT=(255,255,255); DONK=(40,48,56)
CX0,CY0,CW,CH=22,2,16,12   # close-up bovenpunt
cw=CW*12
W=3*530+3*(cw+10); Hh=14+512+30+2*(140+70)+20
v=Image.new('RGB',(W,Hh),'white'); d=ImageDraw.Draw(v)
for i,(im,n) in enumerate([(rgb(r9,WIT),'r9'),(rgb(r8,WIT),'r8_A'),(rgb(r7,WIT),'r7')]):
    v.paste(im.resize((512,512),Image.NEAREST),(i*530,14)); d.text((i*530,0),n,fill=(0,0,0))
for y,x in zip(*np.where(diff)): d.rectangle((x*8,14+y*8,x*8+7,14+y*8+7),outline=(0,90,255))
for i,(im,n) in enumerate([(rgb(r9,WIT),'r9 bovenpunt 12x'),(rgb(r8,WIT),'r8_A'),(m,'model')]):
    c=im.crop((CX0,CY0,CX0+CW,CY0+CH)).resize((cw,CH*12),Image.NEAREST); x0=3*530+i*(cw+10); v.paste(c,(x0,14)); d.text((x0,0),n,fill=(0,0,0))
    if i==0:
        for y,x in zip(*np.where(diff)): d.rectangle((x0+(x-CX0)*12,14+(y-CY0)*12,x0+(x-CX0)*12+11,14+(y-CY0)*12+11),outline=(0,90,255))
y=14+512+30
for bg in (WIT,DONK):
    ims=[rgb(r9,bg),rgb(r8,bg),rgb(r7,bg),m,g3('starmie',bg),png(R+'staryu_regional/staryu/af/staryu_regional.png',bg)]
    for i,im in enumerate(ims): v.paste(Image.new('RGB',(136,140),bg),(i*136,y)); v.paste(im.resize((128,128),Image.NEAREST),(i*136+4,y+6))
    y+=140
    for i,im in enumerate(ims): v.paste(Image.new('RGB',(136,70),bg),(i*136,y)); v.paste(im,(i*136+36,y+2))
    y+=70
d.text((0,Hh-14),'2x en 1x op wit / donker: r9 | r8_A | r7 | model | Gen 3 Starmie | regionale Staryu',fill=(0,0,0))
v.save('sprite_r9/vel.png'); print(v.size)
