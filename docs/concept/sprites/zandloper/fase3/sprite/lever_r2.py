# Levert ronde 2 in r2/.
import numpy as np; from PIL import Image, ImageDraw; import maak_r2 as m, kijk
R='r2/'
V={'zandloper_fase3_B':('B','b'),'zandloper_fase3_A':('A','b'),
   'gezicht_a_B':('B','a'),'gezicht_c_B':('B','c')}
for n,(br,gz) in V.items():
    m.label_png(m.bouw_sprite(br,gz),R+n+'.png'); im=Image.open(R+n+'.png')
    assert im.size==(64,64) and im.mode=='P'; print(n,len(np.unique(np.asarray(im))),'kleuren incl. transparant')
def tekst(c,xy,t): ImageDraw.Draw(c).text(xy,t,fill=(0,0,0))
B2=Image.open(R+'zandloper_fase3_B.png'); A2=Image.open(R+'zandloper_fase3_A.png'); B1=Image.open('r1/zandloper_fase3_B.png')
c=Image.new('RGB',(3*520,20+512+30+100+30+300),'white')
for i,(im,t) in enumerate([(kijk.op_wit(B2,8),'r2 (B, gezicht b)'),(kijk.op_wit(B1,8),'r1 (B)'),(kijk.model64().resize((512,512),Image.NEAREST),'model r5 verkleind')]):
    c.paste(im,(i*520,20)); tekst(c,(i*520+4,4),t)
y=560
for i,(im,t) in enumerate([(B2,'r2 B'),(A2,'r2 A'),(B1,'r1 B')]):
    for j,bg in enumerate([(255,255,255),(232,224,208),(40,44,52),(16,16,16)]):
        b=Image.new('RGBA',(64,64),bg+(255,)); b.alpha_composite(im.convert('RGBA')); c.paste(b.convert('RGB'),(i*300+j*70,y+14))
    tekst(c,(i*300,y),t+' op 1x')
c.paste(kijk.model64(),(920,y+14)); tekst(c,(920,y),'model 1x')
y=690
for i,(im,t) in enumerate([(B2,'r2 B hoofd 12x'),(A2,'r2 A hoofd 12x'),(B1,'r1 B hoofd 12x')]):
    c.paste(kijk.op_wit(im,12).crop((18*12,0,42*12,22*12)),(i*300,y+14)); tekst(c,(i*300,y),t)
c.paste(kijk.op_wit(B2,12).crop((19*12,48*12,43*12,64*12)),(900,y+14)); tekst(c,(900,y),'r2 zandloper 12x')
c.save(R+'vel.png')
names=[('gezicht_a_B','(a) r8-ogen, wit oogwit, r5-wenkbrauw helemaal weg'),('zandloper_fase3_B','(b) r8-ogen, wenkbrauw alleen boven elk oog'),('gezicht_c_B','(c) Machamp-ogen 1-op-1 (rood -> donkerste zandtint)')]
c=Image.new('RGB',(3*310,20+290+20+330),'white')
for i,(n,t) in enumerate(names):
    im=Image.open(R+n+'.png'); c.paste(kijk.op_wit(im,12).crop((18*12,0,42*12,22*12)),(i*310,20)); tekst(c,(i*310,4),t)
    c.paste(kijk.op_wit(im,5).crop((20,0,320,320)),(i*310,330))
c.save(R+'vel_gezicht.png')
