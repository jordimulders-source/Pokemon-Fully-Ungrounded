# Sneeuwmonster fase 2 eindkeuring (schaduw + belijning + kleurtinten, Dragonfly Cave) op sprite_r4.
# Niets hertekend: alleen tinten van bestaande pixels (index) en paletwaarden. Silhouet, ogen en mond: index-diff 0 (assert).
# Gebruik: cd sneeuwmonster_fase2 && python3 eindkeuring/bouw.py
import sys, colorsys, numpy as np
from PIL import Image
sys.path.insert(0,'gereedschap'); from gemeen import MX0,MY0,F,label; from klassen import klassen
U='eindkeuring/'
im=Image.open('sprite_r4/sneeuwmonster2_r4.png'); base=np.asarray(im).astype(int)
p=im.getpalette(); PAL_OUD=[tuple(p[3*i:3*i+3]) for i in range(16)]
# 0 transp | 1 K | 2 l lijn | 3 s schaduw | 4 m midden | 5 h licht | 6 w hoog | 7-9 hout | 10-11 grijs (band, ogen) | 12 steen | 13-15 gloed r/o/y
PAL=list(PAL_OUD)
# K1: outline base / binnenlijnen L100 -> L90 = de lijntint van fase 1 (eindkeuring fase 1); Gen 3 _gba: Glalie 52526a L84, Seel 415283 L82, Absol 5a5a83 L94 (DC regel 4)
PAL[2]=(62,96,140)
# K2: sneeuwramp naar de tint van fase 1 (hue ~210 i.p.v. 190-206 die naar de lichte kant groener wordt), helderheid gelijk
PAL[3]=(120,156,190)   # L149 (was (118,158,186))
PAL[4]=(162,191,222)   # L186 (was (160,194,214))
PAL[5]=(208,226,244)   # L222 = fase 1 m (was (204,228,240))
PAL[6]=(244,250,255)   # L248 = fase 1 w (was (240,250,252), hue 190)
# K3: gloed minder fel, richting de modelgloed (model: rood/oranje mediaan (211,83,50), geel (245,191,81))
PAL[14]=(232,124,44)   # was (240,136,40)
PAL[15]=(244,192,80)   # was (248,208,64)
o=base.copy(); stappen={}
def zet(stap,lijst,nieuw,van):
    for X,Y in lijst:
        assert base[Y,X] in van,(stap,(X,Y),base[Y,X])
        o[Y,X]=nieuw; stappen.setdefault(stap,[]).append((X,Y))
# ---- belijning (DC: buitenlijn 1 px, zwart alleen als outline shadow op de buitenrand, binnenlijnen niet zwart)
zet('B1 kop rechts: dubbele rand weg',[(48,22)],3,{2})                       # l tussen h en K, model L194
zet('B2 hand: zwarte binnenlijn -> lijntint',[(41,46),(42,47),(51,46),(50,47)],2,{1})   # handrand over het lijf (binnenlijn)
zet('B3 hand rechts: lijnklontje',[(51,44)],4,{2})                           # 2x2 lijn tegen de buitenlijn, model L173
zet('B4 elleboog rechts: dubbele rand weg',[(54,37),(54,38)],3,{2})          # l naast zwart, model L180/178
zet('B5 rechtsonder: zwart klontje in de buitenlijn',[(51,50)],3,{1})        # 2 px dikke zwarte hoek, model L122
zet('B6 tussen de voeten: zwart binnen de figuur',[(28,53)],2,{1})           # K op K (2 px), binnenlijn wordt lijntint
zet('B7 linkerarm onder: lijnklontje',[(10,43)],3,{2})                       # l boven de zwarte onderrand, model L102
zet('B8 linkervoet: dubbele onderrand weg',[(18,55),(19,55),(20,55),(21,55)],4,{2})  # l boven K (2 px), model L243/244/198/189
zet('B9 outline highlights kop linksboven',[(21,15),(22,15),(20,16)],3,{2})   # DC: shadow/outline-highlight-tint op de meest belichte lijn (model L215/218/209)
zet('B9 outline highlights schouder links',[(9,35),(8,36)],3,{2})            # model L230/252
# ---- stenen: gloed volgens het gloedaandeel van het model per spritepixel (r3 legde rood al vanaf 8 %; daardoor 55 % gloed tegen 28 % in het model)
a,c,L=klassen(); H,W=c.shape; yy,xx=np.mgrid[0:H,0:W]
Xm=np.floor((xx-MX0)/F).astype(int); Ym=np.floor((yy-MY0)/F).astype(int)
GL={}
for Y in range(33,51):
    for X in range(17,31):
        m=(Xm==X)&(Ym==Y); cc=c[m]
        if np.isin(cc,[1,5,6,7]).mean()>0.3: GL[(X,Y)]=(np.isin(cc,[6,7]).mean(),(cc==7).mean())
STEENZ=lambda X,Y: 17<=X<=30 and 33<=Y<=50
for (X,Y),(g,ye) in sorted(GL.items()):
    v=base[Y,X]
    if v not in (13,14,15): continue
    rand=any(base[Y+dy,X+dx] not in (1,12,13,14,15,10,11) for dx,dy in ((1,0),(-1,0),(0,1),(0,-1)))
    if g>=0.55: n=15 if ye>0.10 else 14
    elif g>=0.35: n=14
    elif g>=0.15: n=13
    else: n=1 if rand else 12
    if n!=v: zet('S1 stenen: gloed volgens model',[(X,Y)],n,{v})
# ---- bevroren zones: index-diff 0
assert ((base>0)==(o>0)).all(),'silhouet'
MOND={(20,24),(21,25),(22,26),(23,26),(24,25),(25,25),(26,25),(27,25),(28,26),(29,26),(30,26),(31,26),(32,26),(33,26),(34,25),(35,24)}
def ogen(X,Y): return (20<=X<=25 and 18<=Y<=24) or (29<=X<=36 and 19<=Y<=24)
D=[(int(X),int(Y)) for Y,X in np.argwhere(o!=base)]
for f,n in ((ogen,'ogen'),(lambda X,Y:(X,Y) in MOND,'mond')):
    d=[q for q in D if f(*q)]; assert not d,(n,d); print('diff %-8s 0 px (assert)'%n)
print('diff silhouet 0 px (assert)')
for k in (1,7,8,9,10,11,12,13): assert PAL[k]==PAL_OUD[k]
print('RGB ogen (K, g, G) en mond-index ongewijzigd; mond verandert alleen via paletkleur 2 (K1)')
for s,l in stappen.items(): print('%-48s %2d px %s'%(s,len(l),l))
print('totaal index-diff',len(D),'px')
def opslaan(o,path):
    q=Image.fromarray(o.astype('uint8'),'P'); f=[v for c in PAL for v in c]; q.putpalette(f); q.save(path,transparency=0)
opslaan(o,U+'sneeuwmonster2_ek.png')
Image.open(U+'sneeuwmonster2_ek.png').convert('RGBA').resize((512,512),Image.NEAREST).save(U+'sneeuwmonster2_8x.png')
# ---- controles
P=np.array(PAL); Lm=P@[.299,.587,.114]
print('palet:'); [print('  %2d %s L%d hue%d n=%d'%(k,PAL[k],Lm[k],colorsys.rgb_to_hsv(*[v/255 for v in PAL[k]])[0]*360,(o==k).sum())) for k in range(16)]
st=o[33:51,17:31]; print('stenen: gloed',np.isin(st,[13,14,15]).sum(),'donker',np.isin(st,[1,12]).sum(),'(r4: 41 / 46)')
N4=((1,0),(-1,0),(0,1),(0,-1))
t=lambda X,Y: not(0<=X<64 and 0<=Y<64) or o[Y,X]==0
rand=lambda X,Y: o[Y,X]>0 and any(t(X+dx,Y+dy) for dx,dy in N4)
zw=[(X,Y) for Y in range(64) for X in range(64) if o[Y,X]==1 and not rand(X,Y) and not ogen(X,Y) and not STEENZ(X,Y) and not Y<20]
print('  zwart binnen de figuur buiten ogen/stenen/emmernaad:',zw)
print('  lichte kleur (4/5/6) op de buitenrand:',[(X,Y) for Y in range(64) for X in range(64) if rand(X,Y) and o[Y,X] in (4,5,6)])
for k in (3,4,5,6):
    lab,n=label(o==k,acht=True); kl=[tuple(int(v) for v in np.argwhere(lab==i)[0][::-1]) for i in range(1,n+1) if (lab==i).sum()<3]
    print('  vlekjes <3 px tint %d: %s'%(k,kl))
# ---- vel.png: r4 | ek | model (8x), daaronder 1x (en 2x) op licht en donker naast fase 1 en de maatstaf
from PIL import ImageDraw
sys.path.insert(0,'gereedschap'); from gemeen import model_op_schaal
def op(img,bg):
    if img.mode=='P':
        a=np.asarray(img); rgba=np.asarray(img.convert('RGBA')).copy(); rgba[...,3]=np.where(a==0,0,255); img=Image.fromarray(rgba)
    b=Image.new('RGBA',img.size,bg+(255,)); b.alpha_composite(img.convert('RGBA')); return b.convert('RGB')
r4=Image.open('sprite_r4/sneeuwmonster2_r4.png'); ek=Image.open(U+'sneeuwmonster2_ek.png')
_m=Image.open('model.png').convert('RGB'); _w=Image.new('RGB',(int(64*F),int(64*F)),(255,255,255)); _w.paste(_m,(-int(MX0),-int(MY0))); mod=_w.resize((512,512),Image.LANCZOS)
V=Image.new('RGB',(3*512+40,512+30+2*(128+20)+20),(255,255,255)); d=ImageDraw.Draw(V)
for i,(t,img) in enumerate((('r4',op(r4,(255,255,255)).resize((512,512),0)),('eindkeuring',op(ek,(255,255,255)).resize((512,512),0)),('model',mod))):
    V.paste(img,(i*532,24)); d.text((i*532+4,6),t,fill='black')
fase1=Image.open('../sneeuwmonster/af/sneeuwmonster.png')
rij=[('r4',r4),('ek',ek),('fase 1',fase1),('Skinguin',Image.open('../skinguin/af/skinguin.png')),('Dundragoon',Image.open('../dundragoon/af/dundragoon.png')),('Zapacha',Image.open('../viscacha/af/viscacha.png')),('Glalie gba',Image.open('../../../../graphics/pokemon/glalie/anim_front_gba.png').crop((0,0,64,64)))]
for j,bg in enumerate(((246,244,236),(40,44,56))):
    y=24+512+20+j*(128+20)
    V.paste(Image.new('RGB',(V.width,128+16),bg),(0,y-8))
    for i,(t,img) in enumerate(rij):
        x=10+i*212 if i<3 else 10+3*212+(i-3)*90; V.paste(op(img,bg),(x,y+32))
        if i<3: V.paste(op(img,bg).resize((128,128),0),(x+70,y))
        d.text((x,y+100),t,fill=(0,0,0) if j==0 else (230,230,230))
V.save(U+'vel.png'); print('vel.png',V.size)
