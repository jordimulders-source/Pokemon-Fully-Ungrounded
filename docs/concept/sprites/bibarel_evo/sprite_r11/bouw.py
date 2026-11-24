# bouw.py ronde 11 (vanaf sprite_r10): Jordi 24 nov. Potlood, staart, gezicht (behalve tanden) en helm: diff 0.
# Draaien vanuit docs/concept/sprites/bibarel_evo:  python3 sprite_r11/bouw.py
# 1 onderkant sluit aan: A = crème tot de kruislijn (zoals Gemini r5), B = binnenlijn linkerbeen verbonden met het losse stompje (26-27,54) (zoals model)
#   sprite.png = A+B; varianten sprite_alleenA.png en sprite_alleenB.png
# 2 puntjes midden boven (schouderplooi (35-37,29),(35,30)) 1 px naar links
# 3 tanden: één tandblok pixel voor pixel uit graphics/pokemon/bibarel/anim_front.png frame 1 (x17-23, r22-26 -> x22-28, r23-27)
# 4 twee kraagbollen onder en linksonder de tanden als ronde bollen (licht f / midden d / donker c + lijn b, zwart aan de onderkant), over het lichaam
import numpy as np
from PIL import Image, ImageDraw
im10=Image.open('sprite_r10/sprite.png'); PAL=np.array(im10.getpalette()[:48]).reshape(16,3).astype('uint8')
r10=np.asarray(im10).astype(int)
L={'K':1,'b':2,'c':3,'d':4,'f':5,'S':6,'C':7,'e':8,'W':13,'w':14,'D':15}
def zet(o,log,n,rij):
    for (x,y),v in rij.items(): o[y,x]=L[v]; log.setdefault(n,[]).append((x,y))
def rijen(spec):   # {y:(x0,'letters')}
    return {(x0+i,y):ch for y,(x0,s) in spec.items() for i,ch in enumerate(s) if ch!='.'}
# ---- 3. tanden (Bibarel: 8 wit, 7 grijs, 3 zwart, 4 bruin -> W, w, K, c); bovenrij r22 (K) blijft
TAND=rijen({23:(23,'Kwww K'.replace(' ','K')),24:(22,'KWWwWWK'),25:(22,'KWWwWWK'),26:(23,'wWwWwc'),27:(24,'KKKc')})
# ---- 4. kraagbollen (vorm uit model r10: bol onder de tanden x24-29 r28-32, bol linksonder x19-22 r24-29)
BOL_A=rijen({27:(28,'b'),28:(23,'bffdddb'),29:(23,'bfddddcb'),30:(23,'bdddcccb'),31:(24,'KdcccK'),32:(25,'KKKK')})
BOL_B=rijen({24:(19,'bbb'),25:(18,'bffd'),26:(18,'bfddc'),27:(18,'bddccb'),28:(19,'bccc'),29:(20,'KKK')})
# ---- 2. puntjes 1 px naar links
PUNT={(37,29):'c',(35,30):'c',(34,29):'b',(35,29):'b',(36,29):'b',(34,30):'b'}
# ---- 1. onderkant
ONDER_A={(28,52):'S',**{(x,53):'S' for x in range(27,31)},**{(x,54):'S' for x in range(28,33)}}
ONDER_B={(22,51):'b',(23,52):'b',(24,52):'b',(25,53):'b',(26,53):'b'}
def bouw(a,b):
    o=r10.copy(); log={}
    zet(o,log,'3 tanden',TAND); zet(o,log,'4 bol linksonder',BOL_B); zet(o,log,'4 bol onder',BOL_A); zet(o,log,'2 puntjes',PUNT)
    if a: zet(o,log,'1A crème tot kruis',ONDER_A)
    if b: zet(o,log,'1B beenlijn',ONDER_B)
    return o,log
def save(idx,pad,z=None):
    im=Image.new('P',(64,64)); im.putpalette(PAL.ravel().tolist()+[0]*3*240)
    im.putdata(idx.astype('uint8').ravel().tolist()); im.save(pad,transparency=0)
    if z: Image.fromarray(PAL[idx]).resize((64*z,64*z),Image.NEAREST).save(pad.replace('.png',f'_{z}x.png'))
o,log=bouw(1,1); oA,_=bouw(1,0); oB,_=bouw(0,1)
save(o,'sprite_r11/sprite.png',8); save(oA,'sprite_r11/sprite_alleenA.png',8); save(oB,'sprite_r11/sprite_alleenB.png',8)
# ---- bewijs
ZONES={'tanden':(22,28,23,27),'bollen':(18,30,24,32),'puntjes':(34,37,29,30),'onder':(22,32,51,54)}
inz=lambda x,y:any(a<=x<=b and c<=y<=d for a,b,c,d in ZONES.values())
dd=[(int(x),int(y)) for y,x in np.argwhere(o!=r10)]
print('gewijzigd:',len(dd),'| buiten zones:',[p for p in dd if not inz(*p)],'| silhouet gelijk:',((o>0)==(r10>0)).all())
POT=np.zeros((64,64),bool); POT[14:29,0:14]=True; STAART=np.zeros((64,64),bool); STAART[20:50,46:64]=True; GEZ=np.zeros((64,64),bool); GEZ[10:23,14:40]=True
print('potlood/staart/gezicht(r<23) gewijzigd:',int(((o!=r10)&POT).sum()),int(((o!=r10)&STAART).sum()),int(((o!=r10)&GEZ).sum()))
for k,v in log.items(): print(k,len(v))
# ---- vel: r11 | r10 | model (8x); kop 12x (met pijlen naar de puntjes); onderkant 12x (A+B, alleen A, alleen B, r10, model, Gemini r5)
fig=np.load('sprite_r1/masker.npy'); yy,xx=np.where(fig)
MK=np.asarray(Image.open('model/r10_k8.png').convert('RGB')); mx0,my0=xx.min(),yy.min(); s_=64/(xx.max()-mx0+1); oy=64-round((yy.max()-my0+1)*s_)
def modelvak(x0,y0,x1,y1,Z):
    W,H=(x1-x0)*Z,(y1-y0)*Z; out=np.full((H,W,3),255,'uint8')
    py,px=np.mgrid[0:H,0:W]; X=(mx0+(x0+px/Z)/s_).astype(int); Y=(my0+(y0+py/Z-oy)/s_).astype(int)
    ok=(X>=0)&(X<99)&(Y>=0)&(Y<99); out[ok]=MK[Y[ok],X[ok]]; return Image.fromarray(out)
big=lambda idx,z,box=(0,0,64,64):Image.fromarray(PAL[idx]).crop(box).resize(((box[2]-box[0])*z,(box[3]-box[1])*z),Image.NEAREST)
V=Image.new('RGB',(2110,1700),'white'); d=ImageDraw.Draw(V)
for i,(img,t) in enumerate([(big(o,8),'r11'),(big(r10,8),'r10'),(modelvak(0,0,64,64,8),'model r10')]):
    V.paste(img,(10+i*522,30)); d.text((10+i*522,10),t+' 8x',fill='black')
y0=580; kb=(12,12,44,36)
for i,(img,t) in enumerate([(big(o,12,kb),'kop r11 12x (pijlen: puntjes, nu 1 px links)'),(big(r10,12,kb),'kop r10 12x (pijlen: puntjes)'),(modelvak(*kb,12),'model 12x')]):
    X0=10+i*400; V.paste(img,(X0,y0+20)); d.text((X0,y0),t,fill='black')
    if i<2:
        for (px,py) in ([(34,29),(35,29),(36,29),(34,30)] if i==0 else [(35,29),(36,29),(37,29),(35,30)]):
            cx,cy=X0+(px-kb[0])*12+6,y0+20+(py-kb[1])*12+6
            d.line([(cx+28,cy+40),(cx+3,cy+5)],fill=(0,90,255),width=3); d.polygon([(cx+1,cy+2),(cx+10,cy+6),(cx+5,cy+12)],fill=(0,90,255))
y0+=320; ob=(14,44,44,60)
G5=Image.open('gemini/r5.png').convert('RGB')
for i,(img,t) in enumerate([(big(o,12,ob),'onder A+B (sprite.png)'),(big(oA,12,ob),'alleen A: crème tot kruis'),(big(oB,12,ob),'alleen B: beenlijn'),(big(r10,12,ob),'r10'),(modelvak(*ob,12),'model'),(G5.crop((240,640,780,900)).resize((360,173),Image.NEAREST),'Gemini r5')]):
    X0=10+(i%3)*400; Y0=y0+20+(i//3)*230; V.paste(img,(X0,Y0)); d.text((X0,Y0-18),t,fill='black')
y0+=480
for j,bg in enumerate([(248,248,248),(40,40,48)]):
    for i,idx in enumerate((o,r10)):
        t=Image.new('RGB',(64,64),bg); t.paste(Image.fromarray(PAL[idx]),(0,0),Image.fromarray(((idx>0)*255).astype('uint8'))); V.paste(t,(10+i*80,y0+20+j*80))
d.text((10,y0),'1x: r11, r10',fill='black')
V.crop((0,0,2110,y0+190)).save('sprite_r11/vel.png')
