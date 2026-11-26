# Sneeuwmonster fase 2, ronde ek6 op ek5. Jordi: "ik zie nog iets teveel rechte lijnen toch, alles wat rood is mag iets smoother,
# kijk naar hoe het model dat doet" (markering: referenties/jordi_ek5_rechte_lijnen.png).
# Per zone de contour/lijn van het model gemeten (randpositie per halve spriterij in het natieve model, /tmp-script cont.py in KEURING),
# daarna als Gen 3-trap gezet (oplopende/aflopende runs, geen losse hoekjes). Niets getekend buiten de 5 zones; palet ongewijzigd.
# Gebruik: cd sneeuwmonster_fase2 && python3 eindkeuring/ek6/bouw.py
import sys, numpy as np
from PIL import Image, ImageDraw
sys.path.insert(0,'gereedschap'); from gemeen import s2m, MODEL
U='eindkeuring/ek6/'
im=Image.open('eindkeuring/ek5/sneeuwmonster2_ek5.png'); base=np.asarray(im).astype(int); PALET=im.getpalette()[:48]
T,K,l,s,m,h,w=0,1,2,3,4,5,6
o=base.copy(); log=[]
def zet(stap,lijst):
    for X,Y,van,naar in lijst:
        assert base[Y,X]==van,(stap,(X,Y),base[Y,X]); o[Y,X]=naar; log.append((stap,X,Y,van,naar))
ZONES={'arm':(6,33,12,46),'nek':(18,26,24,33),'hand':(39,40,49,49),'flank':(50,38,56,54),'onder':(28,51,40,58)}
# Z1 linkerarm buitenrand. Model links (sprite-x): r36 8,9/8,4 · r37-38 8,0 · r39 8,4/9,3 · r40-43 8,9 · r43,5-44 9,3 · r44,5 10,8.
#    ek5: x8 r36-38, x9 r39-43 (5 recht), x10 r44. Nu x8 r36-39 (4), x9 r40-42 (3), x10 r43-44 (2): runs 1-1-4-3-2.
zet('Z1 arm',[(8,39,T,l),(9,39,l,s),(9,43,l,T),(10,43,s,l)])
# Z2 links van de nek: verticale baardlijn x21 r28-30. Model: streng (19,28) -> (19,7-20,1 r29-30,5) -> (20,5 r31) -> (21 r31,5);
#    de lijn volgt nu die streng: (19,28) (20,29) (20,30) (21,31); (21,28-30) wit (model L242/187/156, dun).
zet('Z2 nek',[(21,28,l,w),(21,29,l,w),(21,30,l,w),(20,29,w,l),(20,30,w,l)])
# Z3 hand rechts: rechte hoek x41 r42-47 + r47 x41-47. Model: x40,8-41,6 r44-46,5, dan (41,3-43,0 r47) en (43,6-46,3 r47,5): ronde hoek.
#    Nu x41 r43-45 (3), (42,46), r47 x43-47: hoekpixel (41,46)/(41,47)/(42,47) naar het lijf eronder (s/m zoals de buren).
zet('Z3 hand',[(41,46,l,s),(42,46,s,l),(41,47,l,m),(42,47,l,m)])
# Z4 rechterflank: ek5 x53 r40-50 (11 recht). Model rechts: r37-39 55,8 · r40-42 54,3 · r43-45 53,9 · r46-48 53,5 · r49-50 53,9 ·
#    r51 53,0/51,5 · r52 51,0 · r53-54 50,6. Nu x55 r37-39 (3), x54 r40-43 (4), x53 r44-48 (5), x52 r49-51 (3), x51 r52, x50 r53:
#    bolling met runs 3-4-5-3-1-1 (max. 1 px van de modelrand). Binnenkant krijgt de tint van de buurpixel (m/s).
zet('Z4 flank',[(54,40,T,K),(54,41,T,K),(54,42,T,K),(54,43,T,K),(53,40,K,m),(53,41,K,m),(53,42,K,m),(53,43,K,s),(54,39,K,m),
                (53,49,K,T),(52,49,s,K),(53,50,K,T),(52,51,T,K),(51,51,K,s),(51,52,T,K),(50,52,K,s)])
# Z5 onderkant tussen/onder de benen: ek5 r54 x30-36 (7 recht), dan losse trapjes x37 r55, x38 r56. Model onder: x30,5-34 54,6 ·
#    x34,5-36,5 55,2 · x37 55,6 · x37,5 56,6 · x38-39,5 57,5. Nu r54 x30-33 (4), r55 x34-36 (3), r56 x37-38 (2), r57 x39-41 (3), r58 (5).
zet('Z5 onder',[(34,55,T,K),(35,55,T,K),(36,55,T,K),(34,54,K,m),(35,54,K,m),(36,54,K,m),(37,56,T,K),(37,55,K,m),(37,54,s,m)])
# ---- controles
D=[(int(X),int(Y)) for Y,X in np.argwhere(o!=base)]
inzone=lambda X,Y: any(x0<=X<=x1 and y0<=Y<=y1 for x0,y0,x1,y1 in ZONES.values())
assert all(inzone(*q) for q in D),'buiten de zones'
MOND={(20,24),(21,25),(22,26),(23,26),(24,25),(25,25),(26,25),(27,25),(28,26),(29,26),(30,26),(31,26),(32,26),(33,26),(34,25),(35,24)}
def ogen(X,Y): return (20<=X<=25 and 18<=Y<=24) or (29<=X<=36 and 19<=Y<=24)
def steen(X,Y): return 19<=X<=29 and 33<=Y<=50 and base[Y,X] in (1,10,11,12,13,14,15)
for f,n in ((ogen,'ogen'),(lambda X,Y:(X,Y) in MOND,'mond'),(steen,'stenen'),(lambda X,Y:base[Y,X] in (7,8,9) or Y<=19 and X>=23,'emmer')):
    d=[q for q in D if f(*q)]; assert not d,(n,d); print('diff %-7s 0 px (assert)'%n)
sil=[q for q in D if (base[q[1],q[0]]>0)!=(o[q[1],q[0]]>0)]
print('gewijzigd',len(D),'px, waarvan silhouet',len(sil),sil)
# buitenlijn 1 px: geen licht op de rand, geen nieuw 2x2-lijnblok rond een gewijzigde pixel
def rand(a,X,Y): return a[Y,X]>0 and any(a[Y+dy,X+dx]==0 for dx,dy in((1,0),(-1,0),(0,1),(0,-1)))
licht=[(X,Y) for Y in range(1,63) for X in range(1,63) if rand(o,X,Y) and o[Y,X] in (4,5,6)]
print('lichte tint op de buitenrand:',licht)
Dset=set(D)
blok=[(X,Y) for Y in range(63) for X in range(63) if any((X+i,Y+j) in Dset for i in(0,1) for j in(0,1)) and all(o[Y+j,X+i] in (1,2) for i in(0,1) for j in(0,1))]
assert not blok,('2x2 lijnblok',blok)
for r in log: print('  ',r)
q=Image.fromarray(o.astype('uint8'),'P'); q.putpalette(PALET); q.save(U+'sneeuwmonster2_ek6.png',transparency=0)
q=Image.open(U+'sneeuwmonster2_ek6.png'); q.convert('RGBA').resize((512,512),Image.NEAREST).save(U+'sneeuwmonster2_ek6_8x.png')
# ---- vel: ek5 | ek6 | model op 8x, gewijzigde zones rood omkaderd; daaronder 1x en 2x op licht en donker
def op(img,bg):
    arr=np.asarray(img); rgba=np.asarray(img.convert('RGBA')).copy(); rgba[...,3]=np.where(arr==0,0,255)
    b=Image.new('RGBA',img.size,bg+(255,)); b.alpha_composite(Image.fromarray(rgba)); return b.convert('RGB')
M=Image.open(MODEL).convert('RGB')
(a0,b0),(a1,b1)=s2m(0,0),s2m(64,64); mw=Image.new('RGB',(int(round(a1-a0)),int(round(b1-b0))),(255,255,255)); mw.paste(M,(-int(round(a0)),-int(round(b0))))
ek5=Image.open('eindkeuring/ek5/sneeuwmonster2_ek5.png'); ek6=Image.open(U+'sneeuwmonster2_ek6.png')
V=Image.new('RGB',(3*522+10,512+30+2*150),(255,255,255)); d=ImageDraw.Draw(V)
for i,(n,img) in enumerate((('ek5',ek5),('ek6',ek6),('model',None))):
    x=10+i*522; V.paste(op(img,(255,255,255)).resize((512,512),0) if img else mw.resize((512,512),Image.LANCZOS),(x,20)); d.text((x,4),n+' 8x (rood = gewijzigde zones)',fill='black')
    for x0,y0,x1,y1 in ZONES.values(): d.rectangle([x+x0*8-1,20+y0*8-1,x+(x1+1)*8,20+(y1+1)*8],outline=(230,0,0),width=2)
y=540
rij=[('ek5',ek5),('ek6',ek6),('fase 1',Image.open('../sneeuwmonster/af/sneeuwmonster.png')),('Skinguin',Image.open('../skinguin/af/skinguin.png')),('Dundragoon',Image.open('../dundragoon/af/dundragoon.png'))]
for j,bg in enumerate(((246,244,236),(40,44,56))):
    V.paste(Image.new('RGB',(V.width,150),bg),(0,y))
    for i,(n,img) in enumerate(rij):
        x=10+i*300; V.paste(op(img,bg),(x,y+20)); V.paste(op(img,bg).resize((128,128),0),(x+74,y+12))
        d.text((x,y+92),n,fill=(0,0,0) if j==0 else (230,230,230))
    y+=150
V.save(U+'vel.png'); print('vel',V.size)
