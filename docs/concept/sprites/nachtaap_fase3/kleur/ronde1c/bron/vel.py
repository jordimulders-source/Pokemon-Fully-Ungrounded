"""vel.png: sprite 1x/4x op licht en donker | model (onderlaag) | fase 2 | echte Gen 3-sprites (1x en 3x)."""
import os
import numpy as np
from PIL import Image, ImageDraw, ImageFont
H=os.path.dirname(os.path.abspath(__file__)); R=os.path.dirname(H); REPO=os.path.join(H,'../../../../../../..')
F=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',13)
def laad(p):
    im=Image.open(p)
    if im.mode=='P':
        idx=np.array(im); a=np.array(im.convert('RGBA')); a[idx==0,3]=0; im=Image.fromarray(a)
    im=im.convert('RGBA')
    if im.size[0]==64 and im.size[1]==128: im=im.crop((0,0,64,64))
    return im
def op(im,bg,s):
    t=Image.new('RGBA',(im.width*s,im.height*s),bg); t.alpha_composite(im.resize((im.width*s,im.height*s),Image.NEAREST)); return t
LICHT=(255,255,255,255); DONKER=(36,36,44,255)
werk=laad(os.path.join(R,'nachtaap_fase3.png'))
model=Image.open(os.path.join(H,'../../../silhouet/onderlaag_256.png')).convert('RGBA')
f2=laad(os.path.join(H,'../../../../nachtaap_evo/af/nachtaap_evo.png'))
G=os.path.join(REPO,'graphics/pokemon')
refs=[(n,laad(os.path.join(G,n,'anim_front_gba.png' if os.path.exists(os.path.join(G,n,'anim_front_gba.png')) else 'anim_front.png')))
      for n in ['primeape','medicham','alakazam','slaking','aipom','reuniclus']]
W=Image.new('RGBA',(1320,720),LICHT); d=ImageDraw.Draw(W)
d.text((10,6),'Nachtaap fase 3 - kleurronde 1c (naast 1b; buiten silhouet ronde 1 alleen hand/gloed, kruin, spiraalgat)',font=F,fill=(0,0,0))
W.alpha_composite(op(werk,LICHT,4),(10,28)); W.alpha_composite(op(werk,DONKER,4),(276,28))
mb=Image.new('RGBA',(256,256),LICHT); mb.alpha_composite(model); W.alpha_composite(mb,(542,28))
d.text((10,288),'4x licht',font=F,fill=(0,0,0)); d.text((276,288),'4x donker',font=F,fill=(0,0,0)); d.text((542,288),'model (onderlaag, zelfde vak)',font=F,fill=(0,0,0))
# 1x en 3x rij
x=808
W.alpha_composite(op(werk,LICHT,1),(x,28)); W.alpha_composite(op(werk,DONKER,1),(x+70,28))
r1=laad(os.path.join(R,'../ronde1b/nachtaap_fase3.png'))
W.alpha_composite(op(werk,LICHT,3),(x,100)); W.alpha_composite(op(r1,LICHT,3),(x+200,100))
d.text((x,92-10),'1x licht / donker',font=F,fill=(0,0,0)); d.text((x,294),'3x fase 3',font=F,fill=(0,0,0)); d.text((x+200,294),'3x ronde 1b (vorige)',font=F,fill=(0,0,0))
# echte sprites 1x en 3x
y=320; d.text((10,y),'1x en 3x naast echte Gen 3-sprites (licht en donker)',font=F,fill=(0,0,0)); y+=20
x=10
for n,im in [('ronde 1c',werk),('ronde 1b',r1),('fase 2',f2)]+refs[:5]:
    W.alpha_composite(op(im,LICHT,1),(x,y)); W.alpha_composite(op(im,DONKER,1),(x+66,y))
    d.text((x,y+66),n,font=F,fill=(0,0,0)); x+=150
y+=90; x=10
for n,im in [('ronde 1c',werk),('ronde 1b',r1)]+refs[:3]:
    W.alpha_composite(op(im,LICHT,3),(x,y)); d.text((x,y+194),n,font=F,fill=(0,0,0)); x+=200
W.convert('RGB').save(os.path.join(R,'vel.png'))
