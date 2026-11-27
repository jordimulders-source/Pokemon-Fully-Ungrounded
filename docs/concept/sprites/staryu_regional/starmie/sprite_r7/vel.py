# vel.py r7: python3 sprite_r7/vel.py  (vanuit starmie/)
# rij 1 (8x): r7 | r6_licht | model r4 op schaal   (wijzigingen r7 blauw omkaderd in de r7-kolom)
# rij 2: 1x en 2x op wit en donker: r7, r6_licht, model, Gen 3 Starmie, regionale Staryu, Skinguin, Dundragoon, Zapacha, Princadee
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
r7=Image.open('sprite_r7/starmie_r7.png'); r6=Image.open('sprite_r6/starmie_r6_licht.png'); m=gemeen.model_op_schaal()
diff=np.asarray(r7)!=np.asarray(r6)
W,Hh=3*530,14+512+30+2*(140+70)+20; v=Image.new('RGB',(max(W,9*136),Hh),'white'); d=ImageDraw.Draw(v)
for i,(im,n) in enumerate([(rgb(r7,(255,255,255)),'r7'),(rgb(r6,(255,255,255)),'r6_licht'),(m,'model r4 op schaal')]):
    v.paste(im.resize((512,512),Image.NEAREST),(i*530,14)); d.text((i*530,0),n,fill=(0,0,0))
for y,x in zip(*np.where(diff)): d.rectangle((x*8,14+y*8,x*8+7,14+y*8+7),outline=(0,90,255))
y=14+512+30
WIT=(255,255,255); DONK=(40,48,56)
for bg,lab in ((WIT,'wit'),(DONK,'donker')):
    ims=[rgb(r7,bg),rgb(r6,bg),m,g3('starmie',bg),png(R+'staryu_regional/staryu/af/staryu_regional.png',bg)]+\
        [png(R+f,bg) for f in ('skinguin/af/skinguin.png','dundragoon/af/dundragoon.png','viscacha/af/viscacha.png','awki/af/awki.png')]
    for i,im in enumerate(ims):
        v.paste(Image.new('RGB',(136,140),bg),(i*136,y)); v.paste(im.resize((128,128),Image.NEAREST),(i*136+4,y+6))
    y+=140
    for i,im in enumerate(ims): v.paste(Image.new('RGB',(136,70),bg),(i*136,y)); v.paste(im,(i*136+36,y+2))
    y+=70
d.text((0,Hh-14),'2x en 1x op wit / donker: r7 | r6_licht | model | Gen 3 Starmie | regionale Staryu | Skinguin | Dundragoon | Zapacha | Princadee',fill=(0,0,0))
v.save('sprite_r7/vel.png'); print(v.size)
