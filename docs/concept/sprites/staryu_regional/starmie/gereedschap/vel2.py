# vel2.py UIT.png SPRITE.png [SPRITE2.png ...]: rij 1 op 8x: sprites | r1 | model op schaal | Gen 3 Starmie;
# rij 2: achterster-close-up 12x per sprite naast Gen 3; rij 3: 1x op wit/donker + r1, model, Gen 3, Staryu, maatstaf.
import sys, numpy as np; from PIL import Image, ImageDraw
sys.path.insert(0,'gereedschap'); from gemeen import model_op_schaal

R='../../'
def rgb_from(im,bg=(255,255,255),frame=0):
    o=np.asarray(im)[frame*64:frame*64+64,:64]; pal=np.array(im.getpalette()[:48]).reshape(-1,3)
    img=np.zeros((64,64,3),'uint8'); img[:]=bg
    for k in range(1,len(pal)): img[o==k]=pal[k]
    return Image.fromarray(img)
def pal_png(p,bg=(255,255,255)):
    im=Image.open(p)
    if im.mode=='P': return rgb_from(im,bg)
    im=im.convert('RGBA'); b=Image.new('RGBA',im.size,bg+(255,)); b.alpha_composite(im); return b.convert('RGB').crop((0,0,64,64))
sps=[Image.open(p) for p in sys.argv[2:]]+[Image.open('sprite_r1/starmie_r1.png')]
nam=[p.split('/')[-1][:-4] for p in sys.argv[2:]]+['starmie_r1']
G3=Image.open(R+'../../../graphics/pokemon/starmie/anim_front_gba.png'); g3=rgb_from(G3)
SY=rgb_from(Image.open(R+'../../../graphics/pokemon/staryu/anim_front_gba.png')); m=model_op_schaal()
big=[rgb_from(s) for s in sps]+[m,g3]; nam+=['model op schaal','Gen 3 Starmie']
W=len(big)*520; v=Image.new('RGB',(W,520+14+780+200),'white'); d=ImageDraw.Draw(v)
for i,(im,n) in enumerate(zip(big,nam)): v.paste(im.resize((512,512),Image.NEAREST),(i*520,14)); d.text((i*520,0),n,fill=(0,0,0))
y=540; z=12
for i,s in enumerate(sps[:-1]+[sps[-1]]):
    c=rgb_from(s).crop((2,2,62,62)).resize((60*6,60*6),Image.NEAREST); v.paste(c,(i*372,y))
v.paste(g3.crop((2,2,62,62)).resize((360,360),Image.NEAREST),(len(sps)*372,y)); d.text((0,y+362),'6x: '+' | '.join(nam[:len(sps)])+' | Gen 3 Starmie',fill=(0,0,0))
y+=390
ones=[]
for s in sps: ones+=[rgb_from(s),rgb_from(s,(40,48,56))]
ones+=[m,g3,SY]+[pal_png(R+f) for f in ('skinguin/af/skinguin.png','dundragoon/af/dundragoon.png','viscacha/af/viscacha.png','awki/af/awki.png')]
for i,im in enumerate(ones): v.paste(im,(i*72,y))
d.text((0,y+68),'1x: per sprite wit+donker ('+', '.join(nam[:len(sps)])+') | model | Gen 3 Starmie | Staryu | skinguin | dundragoon | zapacha | princadee',fill=(0,0,0))
y+=90
for i,im in enumerate([rgb_from(s) for s in sps]+[g3]): v.paste(im.resize((128,128),Image.NEAREST),(i*136,y))
v=v.crop((0,0,W,y+140)); v.save(sys.argv[1]); print(sys.argv[1],v.size)
