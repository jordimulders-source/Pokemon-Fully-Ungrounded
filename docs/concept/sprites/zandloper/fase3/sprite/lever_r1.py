# Levert ronde 1: A, B, varianten, vel.png en vel_varianten.png in r1/.
import numpy as np; from PIL import Image, ImageDraw; import maak_r1 as m, kijk, schoon, bewerk
R='r1/'
V={'zandloper_fase3_A':dict(brein='A'),
   'zandloper_fase3_B':dict(brein='B'),
   'var_B_ogen_r5afstand':dict(brein='B',oog=dict(dr=-1)),
   'var_B_ogen_r5afstand_1rechts':dict(brein='B',oog=dict(x0=23,dr=-1)),
   'var_B_glas_lager':dict(brein='B',fles=(-8,-10),trechter=(0,-4)),
   'var_B_glas_naar_voren':dict(brein='B',fles=(-5,-13),trechter=(-3,-7))}
LAB={}
for n,kw in V.items():
    LAB[n]=m.bouw_sprite(**kw); m.label_png(LAB[n],R+n+'.png')
    im=Image.open(R+n+'.png'); assert im.size==(64,64) and im.mode=='P'
    print(n,'kleuren in gebruik:',len(np.unique(np.asarray(im))),'(incl. transparant)')
def tekst(c,xy,t): ImageDraw.Draw(c).text(xy,t,fill=(0,0,0))
def model8():
    return kijk.model64().resize((512,512),Image.NEAREST)
# vel.png
A=Image.open(R+'zandloper_fase3_A.png'); B=Image.open(R+'zandloper_fase3_B.png')
c=Image.new('RGB',(3*520+10,512+20+150+20+300),'white')
for i,(im,t) in enumerate([(kijk.op_wit(A,8),'A: hoofdvorm r5 + windingen r8'),(kijk.op_wit(B,8),'B: r5 met minder windingen'),(model8(),'r5 verkleind (64 px, vlakgemiddelde)')]):
    c.paste(im,(i*520,20)); tekst(c,(i*520+4,4),t)
y=552
for i,im in enumerate([A,B]):
    for j,bg in enumerate([(255,255,255),(232,224,208),(40,44,52),(16,16,16)]):
        b=Image.new('RGBA',(64,64),bg+(255,)); b.alpha_composite(im.convert('RGBA')); c.paste(b.convert('RGB'),(i*300+j*70,y))
    tekst(c,(i*300,y+68),['A','B'][i]+' op 1x (licht/donker)')
tekst(c,(640,y),'1x model'); c.paste(kijk.model64(),(640,y+12))
y=700
for i,im in enumerate([A,B]):
    h=kijk.op_wit(im,12).crop((18*12,0,42*12,22*12)); c.paste(h,(i*300,y+14)); tekst(c,(i*300,y),['A','B'][i]+' hoofd 12x')
z=kijk.op_wit(B,12).crop((19*12,48*12,43*12,64*12)); c.paste(z,(600,y+14)); tekst(c,(600,y),'zandloper 12x (A=B)')
c.save(R+'vel.png'); print('vel',c.size)
# vel_varianten.png
names=['zandloper_fase3_B','var_B_ogen_r5afstand','var_B_ogen_r5afstand_1rechts','var_B_glas_lager','var_B_glas_naar_voren']
lbl=['B (ogen r8, onderlinge afstand r8)','ogen op r5-afstand (rechteroog 1 px naar links)','ogen r5-afstand, beide 1 px naar rechts','fles+trechter 4 px lager (dieper in de schouder)','fles 3 px, trechter 3 px naar het hoofd toe']
c=Image.new('RGB',(5*420,24+400+20+300),'white')
for i,n in enumerate(names):
    im=Image.open(R+n+'.png'); g=kijk.op_wit(im,8).crop((64,0,64+400,400)); c.paste(g,(i*420,24)); tekst(c,(i*420+2,4),lbl[i][:60])
    h=kijk.op_wit(im,12).crop((14*12,2*12,48*12,22*12)); c.paste(h.resize((400,235),Image.NEAREST),(i*420,444))
c.save(R+'vel_varianten.png'); print('vel_var',c.size)
