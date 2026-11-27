# r6 = r5 + beide klauwen (vorm = r3/r5, zelfde pixels) in een eigen teenkleur (A grijs, B donker, C rood) uit het bestaande
# palet, klauwpunten ivoor, en een gesloten omlijning tegen de staart: naast een teen zwart, onder een ivoren klauwpunt de
# donkerste staarttint 2 (anders een rechte zwarte balk). Buiten de klauwzones pixeldiff 0 met r5 (assert).
import numpy as np; from PIL import Image, ImageDraw
PAL=[(152,208,160),(26,16,20),(124,76,18),(196,148,53),(229,184,79),(246,214,124),(206,188,180),(244,240,234),
 (128,28,42),(166,48,63),(208,99,104),(186,82,38),(222,118,50),(50,41,52),(204,192,148),(92,80,96)]
def opslaan(o,pad):
    im=Image.new('P',(64,64)); flat=[x for c in PAL for x in c]; im.putpalette(flat+[0]*(768-len(flat)))
    im.putdata([int(v) for v in o.ravel()]); im.save(pad,transparency=0)
r5=np.array(Image.open('../sprite_r5/sprite.png')).astype(int); r3=np.array(Image.open('../sprite_r3/sprite.png')).astype(int)
# klauwmaskers (teen + klauwpunt + teenlijn), uit de r3/r5-pixels: links X 21-31 Y 49-52, rechts X 32-38 Y 49-52
M=np.zeros((64,64),bool); M[49:53,21:32]=True; M[49:53,32:39]=True; M&=r5>0
TEEN={2,3,4,5,6}; KLAUW={7,14}
KLEUR={'A':{5:6,4:6,6:6,3:15,2:15},          # grijs: wit-schaduw 6 + donkergrijs 15 (condorpoten)
       'B':{5:15,4:15,6:15,3:13,2:13},       # donker: punttint 13 met lichtere 15 bovenop
       'C':{5:10,4:9,6:10,3:8,2:8}}          # rood/karmijn uit kop/pennen
def g(o,Y,X): return o[Y,X] if 0<=Y<64 and 0<=X<64 else 0
uit={}
for var,km in KLEUR.items():
    o=r5.copy(); lijst=[]
    for Y,X in zip(*np.where(M)):
        k=r5[Y,X]
        if k in TEEN: o[Y,X]=km[k]; lijst.append((X,Y,k,o[Y,X],'teen'))
        elif k==14: o[Y,X]=7; lijst.append((X,Y,k,7,'klauwpunt ivoor'))
    # in variant B: lichtere tint alleen bovenop (bovenste teenpixel per kolom), rest donker
    if var=='B':
        for X in range(21,39):
            ys=[Y for Y in range(49,53) if M[Y,X] and r5[Y,X] in TEEN]
            for i,Y in enumerate(ys): o[Y,X]=15 if i==0 else 13
    # omlijning tegen de staart: buur buiten het masker (rechts/onder/links), geen lijn/achtergrond
    for Y,X in zip(*np.where(M)):
        if o[Y,X] in (0,1): continue
        for dy,dx in ((1,0),(0,1),(0,-1)):
            YY,XX=Y+dy,X+dx
            if not(0<=YY<64 and 0<=XX<64) or M[YY,XX] or o[YY,XX] in (0,1): continue
            if YY<49 : continue
            nieuw=2 if (o[Y,X]==7 and dy==1) else 1
            if o[YY,XX]!=nieuw and not(nieuw==2 and o[YY,XX]==2): lijst.append((XX,YY,o[YY,XX],nieuw,'omlijning')); o[YY,XX]=nieuw
    Z=M.copy(); Z[49:54,20:40]=True
    assert not ((o!=r5)&~Z).any(); assert ((o>0)==(r5>0)).all()
    uit[var]=o; opslaan(o,'sprite_%s.png'%var); np.save('sprite_%s.npy'%var,o)
    with open('wissels_%s.txt'%var,'w') as f:
        for X,Y,a,b,r in lijst: f.write('(%d,%d) %d -> %d %s\n'%(X,Y,a,b,r))
    print(var,'px anders dan r5:',int((o!=r5).sum()),'| kleuren',len(set(o.ravel()))-1)
def rgb(o,bg=(240,240,236)):
    a=np.array(PAL,'uint8')[o]; a[o==0]=bg; return Image.fromarray(a)
V=Image.new('RGB',(3*522,18+512+28+256+10+150),'white'); d=ImageDraw.Draw(V)
for i,var in enumerate('ABC'):
    o=uit[var]; x0=i*522
    V.paste(rgb(o).resize((512,512),Image.NEAREST),(x0,18)); d.text((x0+2,2),'r6 %s (8x)'%var,fill=(0,0,0))
    V.paste(rgb(o).crop((16,44,44,58)).resize((448,224),Image.NEAREST),(x0,560)); d.text((x0+2,544),'klauwen 16x',fill=(0,0,0))
    x=x0
    for bg in ((240,240,236),(40,40,56)):
        for s in (1,2): V.paste(rgb(o,bg).resize((64*s,64*s),Image.NEAREST),(x,800)); x+=64*s+8
V.save('vel.png')
