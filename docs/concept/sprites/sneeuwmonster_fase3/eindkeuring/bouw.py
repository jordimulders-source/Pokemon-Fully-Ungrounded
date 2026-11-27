# Sauna-yeti (sneeuwmonster fase 3) eindkeuring: schaduw + belijning + kleurtinten (Dragonfly Cave), nadruk emmer en gezicht.
# Bron sprite_r6/sauna_yeti_r6.png. Niets hertekend: alleen tinten van bestaande pixels (index) en paletwaarden, elk op een gemeten modelwaarde.
# Silhouet: index-diff 0 (assert). Gebruik: cd sneeuwmonster_fase3 && python3 eindkeuring/bouw.py
import sys, os, colorsys, numpy as np
from PIL import Image, ImageDraw
sys.path.insert(0,'gereedschap'); from gemeen import MX0,MY0,F,CH,label,model_op_schaal
U='eindkeuring/'
im=Image.open('sprite_r6/sauna_yeti_r6.png'); base=np.asarray(im).astype(int)
p=im.getpalette(); PAL_OUD=[tuple(p[3*i:3*i+3]) for i in range(16)]
# 0 transp | 1 K | 2 l lijn | 3 s | 4 m | 5 h | 6 w | 7 # hout donker | 8 d hout midden | 9 b hout licht | 10 g grijs (band, steenfacet)
# 11 a hand/voet midden | 12 A hand/voet licht | 13 c steen | 14 o gloed | 15 y geel
M=np.asarray(model_op_schaal()).astype(float); ML=M@[.299,.587,.114]    # model per spritepixel (vlakgemiddelde van het natieve raster)
PAL=list(PAL_OUD)
# P1 hout donker: model donker hout (96,56,32) L65 / schaduwkant emmer L56-86; r6 (132,78,42) L91 lag tussen midden en donker
#    (zelfde index als outline base van de emmer; ramp 9 L155 / 8 L115 / 7 L68 / K, hue schuift naar rood in het donker)
PAL[7]=(100,58,38)
# P2 gezichtshuid: model huid mediaan (201,227,236) L219, hue 199 (cyaan, dezelfde familie als handen en voeten);
#    h (208,226,244) hue 210 werd voor 59 van zijn 65 px in het gezicht gebruikt
PAL[5]=(200,226,236)
o=base.copy(); stappen={}
def zet(stap,lijst,nieuw,van):
    for X,Y in lijst:
        assert base[Y,X] in van,(stap,(X,Y),CH[base[Y,X]])
        if o[Y,X]!=nieuw: o[Y,X]=nieuw; stappen.setdefault(stap,[]).append((X,Y))
# ---------------- E: emmer (hout + band), licht linksboven zoals het model
# E1 houtvulling (geen randpixels): meerderheid van de natieve houtcellen per spritepixel (licht L>=140 / midden 95-140 / donker <95;
#    dezelfde regel als de kale reductie van r1: meerderheid, geen gemiddelde). Gelijkspel -> midden. Een r6-naad (#) blijft midden als
#    donker+midden >= de helft van licht. Donker naast de buitenlijn wordt midden (anders 2 px donkere rand).
N4=((1,0),(-1,0),(0,1),(0,-1))
t0=lambda X,Y: not(0<=X<64 and 0<=Y<64) or base[Y,X]==0
nat=np.asarray(Image.open('natief.png').convert('RGB')).astype(int); NL=nat@[.299,.587,.114]
_yy,_xx=np.mgrid[0:nat.shape[0],0:nat.shape[1]]
_Xm=np.floor((_xx+0.5-MX0)/F).astype(int); _Ym=np.floor((_yy+0.5-MY0)/F).astype(int)
HOUTCEL=((nat[...,0]-nat[...,2])>35)&(NL<235)
TEL={}
for Y in range(12,16):
    for X in range(29,41):
        if base[Y,X] in (7,8,9) and not any(t0(X+dx,Y+dy) for dx,dy in N4):
            c=NL[(_Xm==X)&(_Ym==Y)&HOUTCEL]; k=[(c>=140).sum(),((c>=95)&(c<140)).sum(),(c<95).sum()]; TEL[(X,Y)]=k
            mx=max(k); n=[9,8,7][k.index(mx)] if k.count(mx)==1 else 8
            if base[Y,X]==7 and n==9 and k[1]+k[2]>=k[0]/2: n=8
            if n==7 and any(base[Y+dy,X+dx]==7 and t0(X+2*dx,Y+2*dy) for dx,dy in N4) and base[Y,X]!=7: n=8
            zet('E1 hout per meerderheid modelcellen',[(X,Y)],n,{7,8,9})
# E2 band (stalen band, model licht (152,144,136) L145 / midden L120 / donker L80): s licht linksboven, g midden, c donker onder/rechts
zet('E2 band licht (model L132-151)',[(28,16),(30,16),(31,16),(32,16)],3,{10})
zet('E2 band onderrand rechts in de schaduw (model L56-74)',[(38,17),(36,18),(37,18),(40,18),(41,18),(40,19)],13,{10})
zet('E2 band linkereind: outline base in de eigen donkerste tint',[(27,16),(26,17)],13,{7})
# ---------------- G: gezicht
# G1 lijnen in het gezicht (s, grenzend aan huid >= 67 %, model min-L 74-131): s (L149) -> a (96,140,156) L128 = gemeten modellijn in de huid (100,136,154)
zet('G1 gezichtslijnen s -> a',[(32,21),(33,21),(35,21),(26,22),(29,22),(31,22),(36,22),(30,23),(37,23),(25,27),(35,27),(35,28),(26,29),(27,30),(27,32),(28,32),(29,32),(30,32)],11,{3})
# G2 huidpixels (modelhuid >= 50 %, model L 204-225) die w of m waren -> h (huid)
zet('G2 huid w/m -> h',[(27,22),(37,22),(27,25),(33,25)],5,{4,6})
# ---------------- B: belijning volgens Dragonfly Cave
# B1 onder de rechterarm: de 2-3 px brede l-band is in het model de teal schaduw van het lijf onder de arm (L124-136), niet de lijn
zet('B1 schaduw onder rechterarm l -> a (model L124-136)',[(43,33),(43,34),(44,34),(43,35),(44,35),(43,36),(44,36),(43,37),(44,37),(42,38),(43,38),(44,38),(42,39),(43,39),(44,39),(44,40)],11,{2})
zet('B1 schaduw onder rechterarm l -> s (model L144-157)',[(42,37),(40,39),(41,39),(43,40),(44,41)],3,{2})
# B2 binnenlijnen niet zwart: K binnen de figuur (lijn van arm/hand/voet over het lijf) -> l, op dezelfde plek
zet('B2 binnenlijn rechterarm K -> l',[(43,32),(44,32),(44,33),(45,34),(45,35),(46,35),(45,36),(47,36),(45,37),(48,37),(45,38),(45,39),(45,40),(45,41),(48,41),(45,42),(48,42),(46,43),(48,43),(46,44),(46,45),(46,46),(46,47),(46,48),(47,48),(46,49)],2,{1})
zet('B2 binnenlijn linkerarm K -> l',[(17,38),(16,39),(15,40),(15,41)],2,{1})
zet('B2 contour rechterhand / linkervoet K -> l',[(45,50),(45,51),(41,53),(41,54),(41,55),(40,56),(40,57),(33,57)],2,{1})
zet('B3 knooppunt arm: 2x2 lijnblok (model L192)',[(46,36)],4,{2})
# B4 dubbele onderrand rechterhand (l boven de zwarte buitenlijn) -> hand midden (a)
zet('B4 dubbele onderrand rechterhand',[(52,55),(54,55),(55,55),(56,55)],11,{2})
# B5 outline highlights (DC: "on the outlines in the very most highlighted parts"): s op de lichtste lijnpixels (model L211-226)
zet('B5 outline highlights linkerschouder/-arm',[(15,30),(14,31),(7,37),(6,38)],3,{2})
# ---------------- bevroren / controles
assert ((base>0)==(o>0)).all(),'silhouet'
OGEN={(26,23),(27,23),(28,23),(32,23),(33,23),(34,23),(35,23),(26,24),(27,24),(28,24),(32,24),(33,24),(34,24),(35,24),(30,25),(33,26)}
D=[(int(X),int(Y)) for Y,X in np.argwhere(o!=base)]
assert not [q for q in D if q in OGEN],'ogen/neus'
ST=[q for q in D if base[q[1],q[0]] in (13,14,15) or o[q[1],q[0]] in (14,15)]; assert not ST,('stenen',ST)
for k in (1,2,3,4,6,8,9,10,11,12,13,14,15): assert PAL[k]==PAL_OUD[k],k
print('silhouet 0 px, ogen/pupillen/neus 0 px, stenen 0 px (assert)')
for s,l in stappen.items(): print('%-62s %2d px %s'%(s,len(l),l))
print('totaal index-diff',len(D),'px')
def opslaan(o,path):
    q=Image.fromarray(o.astype('uint8'),'P'); f=[v for c in PAL for v in c]; q.putpalette(f+[0]*(768-len(f))); q.save(path,transparency=0)
opslaan(o,U+'sauna_yeti_ek.png')
def op(img,bg):
    if img.mode=='P':
        a=np.asarray(img); rgba=np.asarray(img.convert('RGBA')).copy(); rgba[...,3]=np.where(a==0,0,255); img=Image.fromarray(rgba)
    b=Image.new('RGBA',img.size,bg+(255,)); b.alpha_composite(img.convert('RGBA')); return b.convert('RGB')
ek=Image.open(U+'sauna_yeti_ek.png'); r6=Image.open('sprite_r6/sauna_yeti_r6.png')
op(ek,(255,255,255)).resize((512,512),0).save(U+'sauna_yeti_8x.png')
# ---- controles
P=np.array(PAL); Lp=P@[.299,.587,.114]
print('palet:'); [print('  %2d %s %s L%d hue%d n=%d'%(k,CH[k],PAL[k],Lp[k],colorsys.rgb_to_hsv(*[v/255 for v in PAL[k]])[0]*360,(o==k).sum())) for k in range(16)]
t=lambda X,Y: not(0<=X<64 and 0<=Y<64) or o[Y,X]==0
rand=lambda X,Y: o[Y,X]>0 and any(t(X+dx,Y+dy) for dx,dy in N4)
STEEN={10,13,14,15}
bijsteen=lambda X,Y: any(o[Y+dy,X+dx] in STEEN for dy in (-1,0,1) for dx in (-1,0,1))
print('  lichte kleur (4/5/6/9/12) op de buitenrand:',[(X,Y) for Y in range(64) for X in range(64) if rand(X,Y) and o[Y,X] in (4,5,6,9,12)])
print('  zwart binnen de figuur (niet bij stenen/emmer):',[(X,Y) for Y in range(64) for X in range(64) if o[Y,X]==1 and not rand(X,Y) and not bijsteen(X,Y) and Y>20])
print('  2x2 lijnblokken (l/K):',[(X,Y) for Y in range(63) for X in range(63) if all(o[Y+j,X+i] in (1,2) for i in (0,1) for j in (0,1))])
em=o[11:20,26:43]; print('  emmer hout 9/8/7:',[(em==k).sum() for k in (9,8,7)],'band s/g/c:',[(o[16:20,26:43]==k).sum() for k in (3,10,13)])
# ---- vel.png
n=Image.open('natief.png').convert('RGB')
def modelcrop(X0,Y0,X1,Y1,s):
    return n.crop((int(round(MX0+X0*F)),int(round(MY0+Y0*F)),int(round(MX0+X1*F)),int(round(MY0+Y1*F)))).resize(((X1-X0)*s,(Y1-Y0)*s),Image.NEAREST)
_m=np.asarray(Image.open('model.png').convert('RGB')).copy(); _m[_m.max(2)<12]=255     # zwarte balken van het Gemini-plaatje wit
_m=Image.fromarray(_m); P5=1408/240; _w=Image.new('RGB',(int(64*F*P5),int(64*F*P5)),(255,255,255))
_w.paste(_m,(-int((MX0-1)*P5+4.5),-int((MY0-1)*P5+5))); mod=_w.resize((512,512),Image.LANCZOS)
def zoom(X0,Y0,X1,Y1,s):
    out=[]
    for img in (r6,ek):
        out.append(op(img.crop((X0,Y0,X1,Y1)),(255,255,255)).resize(((X1-X0)*s,(Y1-Y0)*s),0))
    out.append(modelcrop(X0,Y0,X1,Y1,s)); return out
Z1=zoom(25,10,44,21,16); Z2=zoom(20,18,42,34,16)
fase2=Image.open('../sneeuwmonster_fase2/af/sneeuwmonster2.png')
rij=[('r6',r6),('ek',ek),('fase 2',fase2),('Skinguin',Image.open('../skinguin/af/skinguin.png')),('Dundragoon',Image.open('../dundragoon/af/dundragoon.png'))]
Wd=3*512+2*20+20; Hh=24+512+30+Z1[0].height+30+Z2[0].height+30+2*(64+40)+20
V=Image.new('RGB',(Wd,Hh),(255,255,255)); d=ImageDraw.Draw(V)
for i,(tt,img) in enumerate((('r6',op(r6,(255,255,255)).resize((512,512),0)),('eindkeuring',op(ek,(255,255,255)).resize((512,512),0)),('model',mod))):
    V.paste(img,(10+i*532,24)); d.text((10+i*532+4,6),tt,fill='black')
y=24+512+30
for tt,Z in (('emmer 16x: r6 | ek | model',Z1),('gezicht 16x: r6 | ek | model',Z2)):
    d.text((10,y-18),tt,fill='black')
    x=10
    for z in Z: V.paste(z,(x,y)); x+=z.width+16
    y+=Z[0].height+30
for j,bg in enumerate(((246,244,236),(40,44,56))):
    V.paste(Image.new('RGB',(Wd,64+30),bg),(0,y-6))
    for i,(tt,img) in enumerate(rij):
        V.paste(op(img,bg),(10+i*120,y)); d.text((10+i*120,y+66),tt,fill=(0,0,0) if j==0 else (230,230,230))
    y+=64+40
V.save(U+'vel.png'); print('vel.png',V.size)
