# r4 = r3-png + (1) rechterklauw als voorste vorm (voet.py, variant A of B) + (2) overbodige rechte lijnen (lijnen.py).
# Alles buiten de opdrachtzones: pixeldiff 0 t.o.v. r3 (assert). Uit: sprite.png (= A), sprite_B.png, overlay_8x.png, vel.png.
import sys,numpy as np; from PIL import Image, ImageDraw
sys.path.insert(0,'.'); from voet import voet2,plak; from lijnen import repareer,binnenlijn_goud
PAL=[(152,208,160),(26,16,20),(124,76,18),(196,148,53),(229,184,79),(246,214,124),(206,188,180),(244,240,234),
 (128,28,42),(166,48,63),(208,99,104),(186,82,38),(222,118,50),(50,41,52),(204,192,148),(92,80,96)]
def opslaan(o,pad):
    im=Image.new('P',(64,64)); flat=[x for c in PAL for x in c]; im.putpalette(flat+[0]*(768-len(flat)))
    im.putdata([int(v) for v in o.ravel()]); im.save(pad,transparency=0)
r3=np.array(Image.open('../sprite_r3/sprite.png')).astype(int)
assert (r3==np.load('../sprite_r3/sprite.npy')).all()
# opdrachtzone 1: voet (8x6 vak + 1 px omlijning)
Z1=np.zeros((64,64),bool); Z1[47:55,31:41]=True
# rand van de rechtervleugel (wijkt naar binnen): vorm-over-vorm-lijn, blijft zwart (voorste vorm moet gedefinieerd blijven)
VOORRAND={(26,40),(27,39),(28,38),(29,37),(30,36)}
uit={}
for var in 'AB':
    o,m=plak(r3,voet2(var))
    o,g1=repareer(o,beschermd=Z1); o,g2=binnenlijn_goud(o,beschermd=Z1)
    for p in VOORRAND:
        if o[p]!=r3[p]: o[p]=r3[p]; g2=[q for q in g2 if q!=p]
    Z2=np.zeros((64,64),bool)
    for p in g1+g2: Z2[p]=True
    d=o!=r3; assert not (d&~(Z1|Z2)).any(), 'diff buiten de opdrachtzones'
    uit[var]=(o,Z1&d,Z2&d,g1,g2)
    opslaan(o,'sprite.png' if var=='A' else 'sprite_B.png'); np.save('sprite.npy' if var=='A' else 'sprite_B.npy',o)
    print(var,'klauw',int((Z1&d).sum()),'px | lijnen: zonder modellijn',len(g1),'zwart->goudbinnenlijn',len(g2),'| buiten zones 0 | kleuren',len(set(o.ravel()))-1)
# overlay 8x (A): geel = klauw, magenta = lijnreparatie
o,z1,z2,g1,g2=uit['A']
def rgb(o,bg=(240,240,236)):
    a=np.array(PAL,'uint8')[o]; a[o==0]=bg; return Image.fromarray(a)
def ov(o,z1,z2):
    A=rgb(o).resize((512,512),Image.NEAREST); d=ImageDraw.Draw(A)
    for (Y,X) in zip(*np.where(z1)): d.rectangle([X*8,Y*8,X*8+7,Y*8+7],outline=(255,200,0))
    for (Y,X) in zip(*np.where(z2)): d.rectangle([X*8,Y*8,X*8+7,Y*8+7],outline=(255,0,255))
    return A
W=Image.new('RGB',(1044,530),'white'); W.paste(ov(*uit['A'][:3]),(0,18)); W.paste(ov(*uit['B'][:3]),(532,18))
dd=ImageDraw.Draw(W); dd.text((2,2),'r4 A (geel = rechterklauw, magenta = lijn aangepast)',fill=(0,0,0)); dd.text((534,2),'r4 B',fill=(0,0,0))
W.save('overlay_8x.png')
# vel: r4 A | r4 B | r3 | model (8x) + 1x/2x licht/donker
def op(o,bg,s): return rgb(o,bg).resize((64*s,64*s),Image.NEAREST)
M=Image.open('../gemini/r7.png').convert('RGB').resize((512,512))
V=Image.new('RGB',(4*522,512+20+150),'white'); dv=ImageDraw.Draw(V)
for i,(t,im) in enumerate((('r4 A',op(uit['A'][0],(240,240,236),8)),('r4 B',op(uit['B'][0],(240,240,236),8)),('r3',op(r3,(240,240,236),8)),('model r7',M))):
    V.paste(im,(i*522,18)); dv.text((i*522+2,2),t,fill=(0,0,0))
x=4
for var in 'AB':
    for bg in ((240,240,236),(40,40,56)):
        for s in (1,2): V.paste(op(uit[var][0],bg,s),(x,550)); x+=64*s+10
    dv.text((x-300,535),'r4 '+var,fill=(0,0,0)); x+=30
V.save('vel.png')
# derde paneel: overgebleven rechte stukken >= 5 px (zwart/donker) genummerd, met modelsterkte, zodat Jordi kan aanwijzen
from recht import runs; from lijnen import sterkte
o=uit['A'][0]; P3=rgb(o).resize((512,512),Image.NEAREST); d3=ImageDraw.Draw(P3); rij=[]
for nr,((dy,dx),Y,X,n) in enumerate([r for r in runs(o,ks=(1,2),MIN=5)],1):
    s=[sterkte(X+dx*i,Y+dy*i) for i in range(n)]
    d3.line([(X*8+4,Y*8+4),((X+dx*(n-1))*8+4,(Y+dy*(n-1))*8+4)],fill=(0,190,255),width=3); d3.text((X*8+6,Y*8-10),str(nr),fill=(0,0,200))
    rij.append('%d: start (%d,%d) richting %s lengte %d, modellijn per px %s'%(nr,X,Y,(dy,dx),n,s))
W2=Image.new('RGB',(1044+522,530),'white'); W2.paste(W,(0,0)); W2.paste(P3,(1054,18)); ImageDraw.Draw(W2).text((1056,2),'overgebleven rechte stukken >=5 px (nummers)',fill=(0,0,0))
W2.save('overlay_8x.png'); open('rechte_stukken.txt','w').write('\n'.join(rij)+'\n'); print(len(rij),'rechte stukken over')
