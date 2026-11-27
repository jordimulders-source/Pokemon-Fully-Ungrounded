# vel.png: rij 1 A | B | model verkleind (8x) ; rij 2 gezicht-close-ups 12x (A, B, model) ; rij 3 1x op licht/donker ; rij 4 naast Raikou/Entei 1x en 4x
import sys,numpy as np; sys.path.insert(0,'sprite/r1'); import meet
from PIL import Image, ImageDraw
D='sprite/r1/'; G='/home/user/Pokemon-Fully-Ungrounded/graphics/pokemon/'
A=D+'kay_pacha_r1_A.png'; B=D+'kay_pacha_r1_B.png'
def big(im,z): return im.resize((im.width*z,im.height*z),Image.NEAREST)
def gba(n,bgc):
    im=Image.open(G+n+'/anim_front_gba.png').crop((0,0,64,64)); im.info['transparency']=0
    return meet.rgba(im,bgc)
W=3*512+40; rows=[]
r1=Image.new('RGB',(W,512+24),'white'); d=ImageDraw.Draw(r1)
for i,(im,t) in enumerate([(meet.rgba(A),'A: met 2e paars'),(meet.rgba(B),'B: zonder 2e paars'),(meet.model_box().convert('RGB'),'model verkleind (BOX)')]):
    r1.paste(big(im,8),(i*(512+20),24)); d.text((i*(512+20),4),t,fill='black')
rows.append(r1)
r2=Image.new('RGB',(W,16*12+24),'white'); d=ImageDraw.Draw(r2)
box=(3,10,19,26)
for i,(src,t) in enumerate([(A,'A kop 12x'),(B,'B kop 12x')]):
    r2.paste(big(meet.rgba(src).crop(box),12),(i*(16*12+20),24)); d.text((i*(16*12+20),4),t,fill='black')
r2.paste(meet.model_crop(*box,12),(2*(16*12+20),24)); d.text((2*(16*12+20),4),'model kop 12x',fill='black')
ma=meet.model_box().convert('RGB').crop(box); r2.paste(big(ma,12),(3*(16*12+20),24)); d.text((3*(16*12+20),4),'model BOX 12x',fill='black')
rows.append(r2)
r3=Image.new('RGB',(W,64*2+40),'white'); d=ImageDraw.Draw(r3); x=0
for bgc in [(255,255,255),(248,248,232),(152,208,160),(40,40,48),(0,0,0)]:
    for src in (A,B):
        r3.paste(big(meet.rgba(src,bgc),2),(x,24)); x+=140
d.text((0,4),'2x op wit, creme, gba-groen, donker, zwart (A,B per achtergrond)',fill='black'); rows.append(r3)
r4=Image.new('RGB',(W,64*4+48),(248,248,240)); d=ImageDraw.Draw(r4)
x=0
for im in [meet.rgba(A,(248,248,240)),gba('raikou',(248,248,240)),gba('entei',(248,248,240)),gba('suicune',(248,248,240))]:
    r4.paste(im,(x,24)); x+=70
x=300
for im,t in [(meet.rgba(A,(248,248,240)),'Kay Pacha A'),(gba('raikou',(248,248,240)),'Raikou'),(gba('entei',(248,248,240)),'Entei')]:
    r4.paste(big(im,4),(x,24)); d.text((x,4),t,fill='black'); x+=270
d.text((0,4),'1x: A, Raikou, Entei, Suicune',fill='black'); rows.append(r4)
H=sum(r.height for r in rows)+10*len(rows); o=Image.new('RGB',(W,H),'white'); y=0
for r in rows: o.paste(r,(0,y)); y+=r.height+10
o.save(D+'vel.png'); print(o.size)
