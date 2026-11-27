# Sneeuwmonster fase 2, eindkeuring ek5 op ek4A (Jordi: "ek4 leest het beste en mag naar de eindkeuring").
# Eindkeuring = schaduw + belijning + kleurtinten (Dragonfly Cave). Niets hertekend: alleen bestaande pixels krijgen een andere
# bestaande paletindex; palet ongewijzigd. Bevroren (assert index-diff 0): silhouet, ogen, mond, stenen (rand + gloed).
# Gebruik: cd sneeuwmonster_fase2 && python3 eindkeuring/ek5/bouw.py
import sys, numpy as np
from PIL import Image, ImageDraw
sys.path.insert(0,'gereedschap'); from gemeen import s2m, MODEL
U='eindkeuring/ek5/'
im=Image.open('eindkeuring/ek4/sneeuwmonster2_ek4A.png'); base=np.asarray(im).astype(int); PALET=im.getpalette()[:48]
a=np.asarray(Image.open(MODEL).convert('RGB')).astype(float); L=a@[.299,.587,.114]
def mL(X,Y):
    (xa,ya),(xb,yb)=s2m(X,Y),s2m(X+1,Y+1); return L[int(round(ya)):int(round(yb)),int(round(xa)):int(round(xb))].mean()
K,l,s=1,2,3
o=base.copy(); log=[]
def zet(stap,pix,naar,van):
    for X,Y in pix:
        assert base[Y,X]==van,(stap,(X,Y),base[Y,X]); o[Y,X]=naar; log.append((stap,X,Y,int(mL(X,Y))))
# E1 lijnklontjes op de trapjes van de buitenlijn (DC: "remove the clusters so that the outline is always one pixel wide"):
#    lijntint l binnen de l-buitenlijn in de binnenhoek van een trapje -> s (model L131-161, schaduwtint)
zet('E1 trapjes kop/arm/flank links',[(20,17),(18,23),(9,38),(17,50)],s,l)
# E2 zwart en lijntint om en om (SPRITE_KERN): enkele K tussen twee l op de linkerflank -> l
zet('E2 om-en-om linksonder',[(17,51)],l,K)
# E3 dubbele rand (l direct binnen de buitenlijn) -> s
zet('E3 dubbele rand voet links',[(19,52)],s,l)                    # naast l-buitenlijn (18,52); model 141
zet('E3 dubbele rand kruis',[(27,53),(28,53),(30,53)],s,l)         # boven K (27-28,54)/(30,54); binnenlijn loopt via (26,53) in de buitenlijn
zet('E3 dubbele rand rechtsonder',[(49,52),(49,53)],s,l)           # naast K (50,52-53); model 129/143
zet('E3 dubbele rand hand rechts',[(52,44)],s,l)                   # naast K (53,44); model 128 (lijn (51-52,45) blijft)
# ---- bevroren zones
MOND={(20,24),(21,25),(22,26),(23,26),(24,25),(25,25),(26,25),(27,25),(28,26),(29,26),(30,26),(31,26),(32,26),(33,26),(34,25),(35,24)}
def ogen(X,Y): return (20<=X<=25 and 18<=Y<=24) or (29<=X<=36 and 19<=Y<=24)
def steen(X,Y): return 19<=X<=29 and 33<=Y<=50 and base[Y,X] in (1,10,11,12,13,14,15)
D=[(int(X),int(Y)) for Y,X in np.argwhere(o!=base)]
assert ((base>0)==(o>0)).all(),'silhouet'
for f,n in ((ogen,'ogen'),(lambda X,Y:(X,Y) in MOND,'mond'),(steen,'stenen'),(lambda X,Y:Y<=19 and X>=23,'emmer')):
    d=[q for q in D if f(*q)]; assert not d,(n,d); print('diff %-7s 0 px (assert)'%n)
print('gewijzigd',len(D),'px'); [print('  ',r) for r in log]
q=Image.fromarray(o.astype('uint8'),'P'); q.putpalette(PALET); q.save(U+'sneeuwmonster2_ek5.png',transparency=0)
q=Image.open(U+'sneeuwmonster2_ek5.png'); q.convert('RGBA').resize((512,512),Image.NEAREST).save(U+'sneeuwmonster2_ek5_8x.png')
# ---- vel: ek4A | ek5 | model (8x), daaronder 1x en 2x op licht en donker naast fase 1, Skinguin, Dundragoon
def op(img,bg):
    arr=np.asarray(img); rgba=np.asarray(img.convert('RGBA')).copy(); rgba[...,3]=np.where(arr==0,0,255)
    b=Image.new('RGBA',img.size,bg+(255,)); b.alpha_composite(Image.fromarray(rgba)); return b.convert('RGB')
M=Image.open(MODEL).convert('RGB')
(a0,b0),(a1,b1)=s2m(0,0),s2m(64,64); mw=Image.new('RGB',(int(round(a1-a0)),int(round(b1-b0))),(255,255,255)); mw.paste(M,(-int(round(a0)),-int(round(b0))))
ek4=Image.open('eindkeuring/ek4/sneeuwmonster2_ek4A.png'); ek5=Image.open(U+'sneeuwmonster2_ek5.png')
V=Image.new('RGB',(3*522+10,512+30+2*150),(255,255,255)); d=ImageDraw.Draw(V)
for i,(n,img) in enumerate((('ek4A',ek4),('ek5',ek5),('model',None))):
    x=10+i*522; V.paste(op(img,(255,255,255)).resize((512,512),0) if img else mw.resize((512,512),Image.LANCZOS),(x,20)); d.text((x,4),n+' 8x',fill='black')
y=540
rij=[('ek4A',ek4),('ek5',ek5),('fase 1',Image.open('../sneeuwmonster/af/sneeuwmonster.png')),('Skinguin',Image.open('../skinguin/af/skinguin.png')),('Dundragoon',Image.open('../dundragoon/af/dundragoon.png'))]
for j,bg in enumerate(((246,244,236),(40,44,56))):
    V.paste(Image.new('RGB',(V.width,150),bg),(0,y))
    for i,(n,img) in enumerate(rij):
        x=10+i*300; V.paste(op(img,bg),(x,y+20)); V.paste(op(img,bg).resize((128,128),0),(x+74,y+12))
        d.text((x,y+92),n,fill=(0,0,0) if j==0 else (230,230,230))
    y+=150
V.save(U+'vel.png'); print('vel',V.size)
