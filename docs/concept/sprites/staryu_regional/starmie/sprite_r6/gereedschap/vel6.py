# vel6.py: python3 sprite_r6/gereedschap/vel6.py   (vanuit starmie/)
# rij 1 (8x): r6 licht | r6 sterk | r6 jordi | r5 licht | model r4 op schaal | Gen 3 Starmie
# rij 2 (12x): de twee Gen 3-punten die Jordi aanwees (rl naar rechts, br naar rechtsonder) naast twee punten van r6_jordi
#              (voorste ster rechts, achterpunt rechtsonder), elk 16x16 uitgesneden
# rij 3 (1x): elke sprite op wit en donker + model, Gen 3, maatstaf-sprites
import sys, numpy as np; from PIL import Image, ImageDraw
sys.path.insert(0,'gereedschap'); sys.path.insert(0,'sprite_r5/gereedschap'); import gemeen, voor_r4; gemeen.natief=voor_r4.natief
from gemeen import model_op_schaal
R='../../'
def rgb_from(im,bg=(255,255,255)):
    o=np.asarray(im)[:64,:64]; pal=np.array(im.getpalette()[:48]).reshape(-1,3); img=np.zeros((64,64,3),'uint8'); img[:]=bg
    for k in range(1,16): img[o==k]=pal[k]
    return Image.fromarray(img)
def pal_png(p,bg=(255,255,255)):
    im=Image.open(p)
    if im.mode=='P': return rgb_from(im,bg)
    im=im.convert('RGBA'); b=Image.new('RGBA',im.size,bg+(255,)); b.alpha_composite(im); return b.convert('RGB').crop((0,0,64,64))
F=['sprite_r6/starmie_r6_licht.png','sprite_r6/starmie_r6_sterk.png','sprite_r6/starmie_r6_jordi.png','sprite_r5/starmie_r5_licht.png']
sps=[Image.open(f) for f in F]; nam=['r6 licht','r6 sterk','r6 jordi','r5 licht','model r4 op schaal','Gen 3 Starmie']
g3=rgb_from(Image.open(R+'../../../graphics/pokemon/starmie/anim_front_gba.png')); m=model_op_schaal()
big=[rgb_from(s) for s in sps]+[m,g3]
W=len(big)*520; v=Image.new('RGB',(W,14+512+20+16*12+30+90+140),'white'); d=ImageDraw.Draw(v)
for i,(im,n) in enumerate(zip(big,nam)): v.paste(im.resize((512,512),Image.NEAREST),(i*520,14)); d.text((i*520,0),n,fill=(0,0,0))
y=14+512+20; jd=rgb_from(sps[2])
uit=[(g3,(46,24),'Gen 3 rl (naar rechts)'),(g3,(42,34),'Gen 3 br (naar rechtsonder)'),
     (jd,(42,15),'r6 jordi: voorste ster rechts'),(jd,(40,31),'r6 jordi: achterpunt rechtsonder')]
for i,(im,(x0,y0),n) in enumerate(uit):
    v.paste(im.crop((x0,y0,x0+16,y0+16)).resize((192,192),Image.NEAREST),(i*210,y)); d.text((i*210,y+194),n,fill=(0,0,0))
y+=16*12+30
ones=[]
for s in sps: ones+=[rgb_from(s),rgb_from(s,(40,48,56))]
ones+=[m,g3]+[pal_png(R+f) for f in ('skinguin/af/skinguin.png','dundragoon/af/dundragoon.png','viscacha/af/viscacha.png','awki/af/awki.png')]
for i,im in enumerate(ones): v.paste(im,(i*72,y))
d.text((0,y+68),'1x: wit+donker per sprite (r6 licht, r6 sterk, r6 jordi, r5 licht) | model | Gen 3 | skinguin | dundragoon | zapacha | princadee',fill=(0,0,0))
y+=90
for i,im in enumerate([rgb_from(s) for s in sps]+[g3]): v.paste(im.resize((128,128),Image.NEAREST),(i*136,y-2))
v.save('sprite_r6/vel.png'); print(v.size)
