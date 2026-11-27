# vel.png: rij 1 r1 B | ek1 | model verkleind (8x); rij 2 kop 12x (r1 B, ek1, model, model BOX); rij 3 1x/2x op licht en donker;
# rij 4 1x en 4x naast Raikou/Entei/Suicune (licht), rij 5 idem op donker. Run vanuit docs/concept/sprites/kay_pacha.
import sys,numpy as np; sys.path.insert(0,'sprite/r1'); import meet
from PIL import Image, ImageDraw
G='/home/user/Pokemon-Fully-Ungrounded/graphics/pokemon/'
A='sprite/r1/kay_pacha_r1_B.png'; E='sprite/ek1/kay_pacha_ek1.png'
def big(im,z): return im.resize((im.width*z,im.height*z),Image.NEAREST)
def gba(n,bgc):
    im=Image.open(G+n+'/anim_front_gba.png').crop((0,0,64,64)); im.info['transparency']=0
    return meet.rgba(im,bgc)
big(meet.rgba(E,(255,255,255)),8).save('sprite/ek1/kay_pacha_ek1_8x.png')
W=3*512+40; rows=[]
r1=Image.new('RGB',(W,512+24),'white'); d=ImageDraw.Draw(r1)
for i,(im,t) in enumerate([(meet.rgba(A),'r1 B (voor)'),(meet.rgba(E),'ek1 (na eindkeuring)'),(meet.model_box().convert('RGB'),'model r10a verkleind (BOX)')]):
    r1.paste(big(im,8),(i*(512+20),24)); d.text((i*(512+20),4),t,fill='black')
rows.append(r1)
box=(2,0,26,28); w=(box[2]-box[0])*12; h=(box[3]-box[1])*12
r2=Image.new('RGB',(W,h+24),'white'); d=ImageDraw.Draw(r2)
for i,(src,t) in enumerate([(A,'r1 B kop 12x'),(E,'ek1 kop 12x')]):
    r2.paste(big(meet.rgba(src).crop(box),12),(i*(w+16),24)); d.text((i*(w+16),4),t,fill='black')
r2.paste(meet.model_crop(*box,12),(2*(w+16),24)); d.text((2*(w+16),4),'model kop 12x',fill='black')
rows.append(r2)
r3=Image.new('RGB',(W,64*2+40),'white'); d=ImageDraw.Draw(r3); x=0
for bgc in [(255,255,255),(248,248,232),(152,208,160),(40,40,48),(0,0,0)]:
    for src in (A,E):
        r3.paste(big(meet.rgba(src,bgc),2),(x,24)); x+=140
    x+=20
d.text((0,4),'2x op wit, creme, gba-groen, donker, zwart (per achtergrond: r1 B, ek1)',fill='black'); rows.append(r3)
for bgc,lab in [((248,248,240),'licht'),((40,40,48),'donker')]:
    r=Image.new('RGB',(W,64*4+48),bgc); d=ImageDraw.Draw(r); tc='black' if lab=='licht' else 'white'
    x=0
    for im in [meet.rgba(E,bgc),gba('raikou',bgc),gba('entei',bgc),gba('suicune',bgc)]:
        r.paste(im,(x,24)); x+=68
    d.text((0,4),'1x: ek1, Raikou, Entei, Suicune ('+lab+')',fill=tc)
    x=290
    for im,t in [(meet.rgba(E,bgc),'ek1 4x'),(gba('raikou',bgc),'Raikou'),(gba('entei',bgc),'Entei'),(gba('suicune',bgc),'Suicune')]:
        r.paste(big(im,4),(x,24)); d.text((x,4),t,fill=tc); x+=262
    rows.append(r)
Hh=sum(r.height for r in rows)+10*len(rows); o=Image.new('RGB',(max(W,290+4*262),Hh),'white'); y=0
for r in rows: o.paste(r,(0,y)); y+=r.height+10
o.save('sprite/ek1/vel.png'); print(o.size)
