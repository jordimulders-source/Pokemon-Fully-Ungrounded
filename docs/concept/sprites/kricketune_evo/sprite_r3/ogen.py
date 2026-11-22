# Oogstudie op r3 (Jordi: "ja beide ogen zijn niet mooi, beetje uitgerekt"). Beide ogen weg (kop terug: omlijning x24, selout x25,
# rood binnenin), dan per variant een oogpaar uit een echte Gen 3-sprite, pixel voor pixel, alleen kleuren naar het eigen palet.
# Ver oog: glans rond (25,14) (modelplek); nabij oog op dezelfde hoogte, rond x33-35. Bouwen: cd kricketune_evo && python3 sprite_r3/ogen.py
import sys, numpy as np; sys.path.insert(0,'gereedschap'); from gemeen import *; from PIL import Image, ImageDraw
r3=laden('sprite_r3/kricketune_evo_r3.png'); b=r3.copy()
N8=[(dy,dx) for dy in (-1,0,1) for dx in (-1,0,1) if dy or dx]
weg=[(x,y) for y in range(12,18) for x in range(33,36) if b[y,x] in (1,2,6,12)]+[(x,y) for y in range(12,16) for x in range(26,29) if b[y,x] in (1,2,6,12)]
for x,y in weg: b[y,x]=0; b[y,x]=-1
for _ in range(4):
    for x,y in weg:
        if b[y,x]==-1:
            nb=[b[y+dy,x+dx] for dy,dx in N8 if b[y+dy,x+dx] in (9,10,11)]
            if nb: b[y,x]=max(set(nb),key=nb.count)
for y in range(12,16):
    if b[y,25] in (1,2,6,12): b[y,25]=7
b[b==-1]=10
def bron(n,f=0): return np.asarray(Image.open('../../../../graphics/pokemon/%s/anim_front.png'%n)).astype(int)[f*64:(f+1)*64]
def plak(o,src,box,dx,dy,m):
    x0,x1,y0,y1=box
    for y in range(y0,y1):
        for x in range(x0,x1):
            if src[y,x] in m: o[y+dy,x+dx]=m[src[y,x]]
KT2=bron('kricketune',1); KTOT=bron('kricketot'); VB=bron('volbeat')
V={}
o=b.copy(); m={4:1,5:2,6:12,7:6}
plak(o,KT2,(25,28,18,22),-1,-4,m); plak(o,KT2,(33,37,17,21),-1,-4,m)
V['A']=('Kricketune frame 2 (veraf x25-27 y18-21, nabij x33-36 y17-20), zelfde onderlinge plek',o)
o=b.copy(); m={4:1,7:12,6:6}
plak(o,KTOT,(30,33,28,32),-4,-16,m); plak(o,KTOT,(30,33,28,32),4,-16,m)
V['B']=('Kricketot (oog x30-32 y28-31, voor beide ogen; donkerbruin -> grijsbruin, creme glans -> wit)',o)
o=b.copy(); m={2:1,5:2,6:12,7:12,3:6,14:6}
plak(o,VB,(19,23,25,29),6,-11,m); plak(o,VB,(19,23,25,29),14,-11,m)
V['C']=('Volbeat (linkeroog x19-22 y25-28, voor beide ogen; geel -> grijsbruin, pupil zwart, glans wit)',o)
for k,(t,o) in V.items():
    opslaan(o,'sprite_r3/ogen_%s.png'%k); d=o!=r3
    print(k,t,'| anders dan r3:',int(d.sum()),'px'); toon(o,y0=10,y1=19,x0=22,x1=40)
# vel: koppen 12x (r3 + varianten) met letter en bron; elke variant 1x en 4x
x0,y0,x1,y1=18,4,44,22; z=12; bw,bh=(x1-x0)*z,(y1-y0)*z
P=[('r3 (nu)','Kricketune frame 1',r3)]+[(k,t,o) for k,(t,o) in V.items()]
W=Image.new("RGB",(len(P)*(bw+12),30+bh+12+256+12+70),'white'); dr=ImageDraw.Draw(W)
for i,(k,t,o) in enumerate(P):
    X=i*(bw+12); dr.text((X+2,2),k,fill=(0,0,0)); dr.text((X+2,12),t[:50],fill=(80,80,80)); dr.text((X+2,21),t[50:100],fill=(80,80,80))
    W.paste(rgb(o,(255,255,255)).crop((x0,y0,x1,y1)).resize((bw,bh),Image.NEAREST),(X,32))
    W.paste(rgb(o,(255,255,255)).resize((256,256),Image.NEAREST),(X,42+bh))
    for j,bg in enumerate([(232,232,216),(40,48,56)]): W.paste(rgb(o,bg),(X+j*70,54+bh+256))
W.save('sprite_r3/ogen_vel.png'); print(W.size)
