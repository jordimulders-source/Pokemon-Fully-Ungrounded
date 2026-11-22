"""Vormpuntenvel: front-kop op 12x met de afgelezen polygonen (wat Jordi in 1 blik controleert/verschuift)
naast de kop van a2_af en van de proef op 12x."""
import sys,numpy as np, importlib.util
from PIL import Image, ImageDraw
R='/home/user/Pokemon-Fully-Ungrounded/docs/concept/sprites/viscacha/'; S=sys.path[0]+'/'
src=open(S+'kop_vector.py').read(); i=src.index('VORM={'); j=src.index('KLEUR=')
ns={}; exec(src[i:j],ns); VORM,OOG=ns['VORM'],ns['OOG']
Z=12
fr=Image.open(R+'af/viscacha.png').convert('RGBA').crop((2,12,30,40))
F=Image.new('RGBA',fr.size,'white'); F.alpha_composite(fr); F=F.resize((28*Z,28*Z),Image.NEAREST)
d=ImageDraw.Draw(F); K={'verre oor':(0,0,255),'kop':(255,0,160),'nabije oor':(0,150,255),'wangpluk':(0,160,0),'kraag':(255,90,0)}
for n,(_,pts) in VORM.items():
    P=[((x-2)*Z,(y-12)*Z) for x,y in pts]; d.line(P+[P[0]],fill=K[n],width=3)
    for p in P: d.ellipse((p[0]-4,p[1]-4,p[0]+4,p[1]+4),fill=K[n])
ex,ey=OOG; d.ellipse(((ex-2)*Z-7,(ey-12)*Z-7,(ex-2)*Z+7,(ey-12)*Z+7),outline=(255,0,0),width=3)
def kop(p):
    im=Image.open(p).convert('RGBA').crop((0,4,18,24)); g=Image.new('RGBA',im.size,(152,208,160,255)); g.alpha_composite(im); return g.resize((18*Z*1,20*Z),Image.NEAREST)
A=kop(R+'icoon/onderdelen/icon_a2_af.png'); B=kop(S+sys.argv[2])
W=Image.new('RGBA',(F.width+A.width+B.width+40,max(F.height,A.height)+30),'white')
W.paste(F,(0,30)); W.paste(A,(F.width+20,30)); W.paste(B,(F.width+A.width+40,30))
dd=ImageDraw.Draw(W); dd.text((4,8),'front: vormpunten (Claude leest af, Jordi verschuift)',fill=0); dd.text((F.width+24,8),'a2_af (pixels verkleind)',fill=0); dd.text((F.width+A.width+44,8),'vormpunten gerasterd',fill=0)
W.save(S+sys.argv[1])
