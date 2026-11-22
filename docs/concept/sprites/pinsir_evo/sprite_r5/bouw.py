# Pinsir-evolutie r5: basis = r4_A (oog A bevroren, silhouet gelijk). Jordi op r4: "oog a is goed, hij is nog steeds super
# blurry, het ligt aan het feit dat er niet genoeg kleurtinten gebruikt worden en de lijnen te zacht zijn" · "en nee dat
# betekent niet meteen zwarte lijnen doen nu".
# 1. Volle palet (16 incl. transparant): lijf 5 tinten (lijn, schaduw, midden, licht, glans), kaak 4 (lijn + 3), dekschild 4
#    (lijn + 3). De tandschaduw (r4 index 13) vervalt: die pixels krijgen de lichte lijftint.
# 2. Hardere lijnen ZONDER extra zwart: zwart blijft alleen waar het in r4 al zit; nieuwe lijnen zijn de gekleurde lijntint van
#    het eigen onderdeel (Gen 3-selout), doorlopend:
#    a. buitenrand aan de lichtkant: de middentint-selout van r4 wordt de lijntint van het onderdeel (ook de kaakbovenrand);
#    b. binnenlijnen langs de modellijnen: waar de middellijn (skelet) van een zwarte modellijn door een spritecel loopt
#       (>= 11 skeletpixels per cel) en de pixel nog vulling is, wordt hij lijntint; alleen stukken van >= 3 px (geen puntjes);
#    c. waar lijf direct aan kaak of dekschild grenst zonder lijn ertussen: de lijfpixel wordt lijntint.
# 3. Kopschild-facetten uit het model, onderlijf rond de middelste hand / verre voet opgeschoond (onderlijf5.txt).
# Bouwen: cd pinsir_evo && python3 sprite_r5/bouw.py
import sys, numpy as np
sys.path.insert(0,'gereedschap'); from model import klassen, skeletlijnen
from PIL import Image, ImageDraw; from scipy import ndimage
UIT='sprite_r5'
R4=np.asarray(Image.open('sprite_r4/pinsir_evo_r4_A.png')).astype(int)
H=W=64; yy,xx=np.mgrid[:H,:W]
# ---------- palet (index: kleur, helderheid) ----------
PAL=[(120,200,160),(18,14,14),
     (44,34,30),                                  # 2 lijf lijn        36
     (90,76,66),(128,110,92),(170,148,120),(214,194,162),   # 3-6 lijf schaduw 77, midden 110, licht 146, glans 190
     (72,28,22),(118,52,38),(162,84,58),(206,130,94),       # 7-10 kaak lijn 41, donker 69, midden 101, licht 143
     (66,36,18),(104,62,30),(156,110,66),(210,166,110),     # 11-14 dekschild lijn 40, vlek 65, midden 111, licht 162
     (236,222,206)]                               # 15 oog/tand crème 221
LIJN={2:2,3:7,4:11}                                # materiaal -> lijntint
# r4 -> r5: lijf 2/3/4/5 -> schaduw/midden/licht/glans, kaak 6/7/8 -> 8/9/10, schild 9/10/11 -> 12/13/14, tand 12 -> 15, tandschaduw 13 -> lijf licht
MAP={0:0,1:1,2:3,3:4,4:5,5:6,6:8,7:9,8:10,9:12,10:13,11:14,12:15,13:5}
o=np.vectorize(MAP.get)(R4)
def mat_van(v): return 0 if v==0 else 1 if v==1 else 2 if v in (2,3,4,5,6) else 3 if v in (7,8,9,10) else 4 if v in (11,12,13,14) else 5
MAT=np.vectorize(mat_van)(o)
OOG=(xx>=14)&(xx<=25)&(yy>=26)&(yy<=28)            # bevroren (oog A)
MOND=(xx>=16)&(xx<=22)&(yy>=28)&(yy<=35)           # tanden/mond: niet aanraken
VAST=OOG|MOND
# ---------- model ----------
a,c,fg=klassen(); ML=a.mean(2); CEL=974/64; MX0,MY0=31,134; DY=13
S=skeletlijnen(c,MX0,MY0-DY*CEL,CEL,64,64)
mt=np.full((H,W),np.nan)
for Y in range(H):
    for X in range(W):
        j=Y-DY; ya,yb=int(round(MY0+j*CEL)),int(round(MY0+(j+1)*CEL)); xa,xb=int(round(MX0+X*CEL)),int(round(MX0+(X+1)*CEL))
        if yb<=0 or xb<=0: continue
        blk=ML[max(ya,0):yb,max(xa,0):xb]; ff=fg[max(ya,0):yb,max(xa,0):xb]&(blk>=25)
        if ff.sum()>=8: mt[Y,X]=blk[ff].mean()
N4=((-1,0),(1,0),(0,-1),(0,1))
def buren(Y,X,arr,nb=N4):
    return [arr[Y+dy,X+dx] if 0<=Y+dy<H and 0<=X+dx<W else 0 for dy,dx in nb]
# ---------- 3. kopschild-facetten uit het model ----------
# Kopschild = lijfpixels boven de ogen/rug (y <= 25, x <= 40). Model: lichte voorste facet linksboven (lichte richel van
# (12,22) naar (24,19)), donkerdere facetten rechts en aan de voorrand. Toon per cel uit het model, in 3 banden op de
# eigen toonverdeling van het kopschild (zo blijven de modelfacetten), daarna vlekjes < 3 px weg.
KS=(MAT==2)&(yy<=25)&(xx<=40)&(o!=1)&~VAST
mtg=ndimage.uniform_filter(np.where(np.isnan(mt),np.nanmean(mt),mt),5)   # gladgestreken: facetten, geen celruis
v=mtg[KS]; q1,q2=np.nanpercentile(v,[30,75])
for Y,X in zip(*np.where(KS)):
    m=mtg[Y,X]
    if np.isnan(m): continue
    o[Y,X]=3 if m<q1 else 4 if m<q2 else 5
# ---------- 3a. onderlijf opnieuw uit het model overgenomen (y >= 36) ----------
# Per spritecel de mediane helderheid van de niet-zwarte modelpixels -> 4 tonen (model: romp ±30, platen 55-75, glans > 88):
# < 40 schaduw, < 62 midden, < 88 licht, anders glans; verre ledematen één toon lager. Lijnen: waar de modellijn door de cel
# loopt (>= 9 skeletpixels): zwart als r4 daar al zwart had, anders de lijntint; r4-zwart zonder modellijn (< 5) wordt vulling.
# Buitenrand (vulpixel naast achtergrond) blijft r4 (zwart) / wordt in 2a selout.
VER=((xx<=24)&(yy>=40))|((xx>=21)&(xx<=31)&(yy>=45))
ZONE=(yy>=36)&(MAT==2)|((yy>=36)&(MAT==1))
Pr=np.pad(R4,1)
nrand=lambda Y,X: any(Pr[Y+1+dy,X+1+dx]==0 for dy in (-1,0,1) for dx in (-1,0,1))
MED=np.full((H,W),np.nan)
for Y,X in zip(*np.where(ZONE)):
    j=Y-DY; ya,yb=int(round(MY0+j*CEL)),int(round(MY0+(j+1)*CEL)); xa,xb=int(round(MX0+X*CEL)),int(round(MX0+(X+1)*CEL))
    blk=ML[ya:yb,xa:xb]; ff=fg[ya:yb,xa:xb]&(blk>=25)
    if ff.sum()>=20: MED[Y,X]=np.median(blk[ff])
n3a=0
for Y,X in zip(*np.where(ZONE)):
    if VAST[Y,X] or nrand(Y,X): continue
    if any(mat_van(o[Y+dy,X+dx]) in (3,4) for dy in (-1,0,1) for dx in (-1,0,1) if 0<=Y+dy<H and 0<=X+dx<W): continue
    if S[Y,X]>=9:
        nv=1 if R4[Y,X]==1 else 2
    elif np.isnan(MED[Y,X]):
        continue
    else:
        mm=MED[Y,X]; t=0 if mm<40 else 1 if mm<62 else 2 if mm<88 else 3
        if VER[Y,X]: t=max(t-1,0)
        nv=3+t
    if o[Y,X]!=nv: o[Y,X]=nv; n3a+=1
MAT=np.vectorize(mat_van)(o)
# ---------- 3b. onderlijf met de hand ----------
M5={'K':1,'L':2,'2':3,'3':4,'4':5,'5':6}            # schrijfwijze r4 (2-5) + L = lijntint
for ln in open(UIT+'/onderlijf5.txt'):
    if not ln.strip() or ln.startswith('#'): continue
    Y,X0,t=ln.split(); Y,X0=int(Y),int(X0)
    for i,ch in enumerate(t):
        X=X0+i; assert MAT[Y,X] in (1,2) and not VAST[Y,X],(ln,X)
        assert not (ch=='K' and o[Y,X]!=1),('geen nieuw zwart',ln,X)
        o[Y,X]=M5[ch]
# ---------- opruimen: tintvlekjes < 3 px ----------
def opruimen(o,groep,minpx=3,vast=VAST):
    for _ in range(5):
        n_ch=0
        for k in groep:
            lab,n=ndimage.label(o==k)
            for i in range(1,n+1):
                pts=np.argwhere(lab==i)
                if len(pts)>=minpx or any(vast[Y,X] for Y,X in pts): continue
                bb={}
                for Y,X in pts:
                    for v in buren(Y,X,o):
                        if v in groep and v!=k: bb[v]=bb.get(v,0)+1
                if bb:
                    nv=max(bb,key=bb.get)
                    for Y,X in pts: o[Y,X]=nv
                    n_ch+=1
        if not n_ch: break
    return o
o=opruimen(o,[3,4,5])
lab,n=ndimage.label(o==6)                            # glans: hooglicht mag 2 px, niet 1
for i in range(1,n+1):
    if (lab==i).sum()<2: o[lab==i]=5
# ---------- 2b. gaten in binnenlijnen dichten langs de modellijnen (lijntint, geen zwart) ----------
# Alleen bruggen: een vulpixel waar de modellijn door loopt (>= 7 skeletpixels in de cel) en die twee losse stukken lijn
# (zwart of lijntint) met elkaar verbindt, wordt lijntint. Herhaald, zodat gaten van 2-3 px ook dicht gaan. Geen losse
# nieuwe streepjes.
lijnmask=np.zeros((H,W),bool)
for _ in range(3):
    L=(o==1)|(o==2)
    lab,n=ndimage.label(L,structure=np.ones((3,3)))
    nieuw=[]
    for Y,X in zip(*np.where((S>=7)&(MAT==2)&~L&~VAST&(o>0))):
        if 0 in buren(Y,X,o): continue
        ids={lab[Y+dy,X+dx] for dy in (-1,0,1) for dx in (-1,0,1) if 0<=Y+dy<H and 0<=X+dx<W and lab[Y+dy,X+dx]>0}
        if len(ids)>=2: nieuw.append((Y,X))
    if not nieuw: break
    for Y,X in nieuw: o[Y,X]=2; lijnmask[Y,X]=True
# ---------- 2c. lijf direct tegen kaak/dekschild: lijfpixel wordt lijntint ----------
n2c=0
for Y,X in zip(*np.where((MAT==2)&(o!=1)&~VAST)):
    if any(mat_van(v) in (3,4) for v in buren(Y,X,o)) and o[Y,X]!=2: o[Y,X]=2; n2c+=1
# ---------- 2a. buitenrand: gekleurde selout in de lijntint van het onderdeel ----------
# Rand = vulpixel met achtergrond als 4-buur. Zwart blijft zwart. Klauwpunten (y >= 53) en dunne stekels (vulling <= 1 px
# breed in de rij) krijgen de schaduwtint i.p.v. de lijntint, anders verdwijnen ze in de omlijning.
n2a=0
for Y,X in zip(*np.where((o>1)&~VAST)):
    if 0 not in buren(Y,X,o): continue
    m=mat_van(o[Y,X])
    if m==5: continue
    rij=(o[Y,max(X-1,0)]>1)+(o[Y,min(X+1,63)]>1)
    dun=(rij==0) or Y>=53
    if m==2: nv=3 if dun else 2
    elif m==3: nv=8 if dun else 7
    else: nv=12 if dun else 11
    if dun and o[Y,X] in (5,6,10,14) and Y>=53: continue     # lichte klauwpunt blijft (r3/r4)
    if o[Y,X]!=nv: o[Y,X]=nv; n2a+=1
# ---------- dekschild: donkere rand aan de schaduwkant (4e schildtint) ----------
# Schildpixel met zwart/achtergrond rechts of onder (schaduwkant, binnen de zwarte omlijning) en zelf vlek of midden -> schildlijn.
for Y,X in zip(*np.where(np.isin(o,[12,13]))):
    r=o[Y,X+1] if X+1<W else 0; d=o[Y+1,X] if Y+1<H else 0
    if (r in (0,1) or d in (0,1)) and Y>=30: o[Y,X]=11
# ---------- laatste opruimronde: losse 1-px vultinten (lijntint telt als lijn en blijft) ----------
o=opruimen(o,[3,4,5,6],minpx=2)
o=opruimen(o,[8,9,10],minpx=2); o=opruimen(o,[12,13,14],minpx=2)
# buitenrand nog eens na de opruimronde: geen midden/lichte tint op de rand behalve klauwpunten (y >= 53)
Pz=np.pad(o,1)
for Y,X in zip(*np.where(np.isin(o,[4,5,6]))):
    if Y<53 and any(Pz[Y+1+dy,X+1+dx]==0 for dy,dx in N4): o[Y,X]=3
# ---------- opslaan + controles ----------
def opslaan(o,path):
    p=Image.fromarray(o.astype('uint8'),'P'); pal=[v for cc in PAL for v in cc]; p.putpalette(pal+[0]*(768-len(pal))); p.save(path,transparency=0)
opslaan(o,UIT+'/pinsir_evo_r5.png')
R4m=np.vectorize(MAP.get)(R4)
print('silhouet-diff met r4A:',int(((o>0)!=(R4>0)).sum()),'| ooggebied gelijk aan r4A:',int((o[OOG]!=R4m[OOG]).sum())==0,
      '| nieuw zwart:',int(((o==1)&(R4!=1)).sum()),'| zwart weg:',int(((o!=1)&(R4==1)).sum()))
print('kleuren incl. transparant:',len(set(o.ravel())),'| zwart %.1f%%'%(100*(o==1).sum()/(o>0).sum()),
      '| binnenlijnen (lijntint, 2b):',int(lijnmask.sum()),'| lijf tegen kaak/schild (2c):',n2c,'| buitenrand (2a):',n2a)
for nm,g in (('lijf',[2,3,4,5,6]),('kaak',[7,8,9,10]),('schild',[11,12,13,14])):
    print('%-6s'%nm,[(k,round(sum(PAL[k])/3),int((o==k).sum())) for k in g])
lab_t=0
per={}
for k in range(3,15):
    if k in (7,11): continue
    l,nn=ndimage.label(o==k); per[k]=sum(1 for i in range(1,nn+1) if (l==i).sum()<3); lab_t+=per[k]
print('vlekjes per tint (vulling):',per)
print('tintvlekjes < 3 px (vulling, lijntinten niet meegeteld):',lab_t)
if len(sys.argv)>1:
    CH='.KL2345abcdwvml T'
    CH='.KL2345pqrsuvwxT'
    for Y in range(12,62): print('%2d '%Y+''.join(CH[v] for v in o[Y]))
# ---------- vel ----------
sys.path.insert(0,'gereedschap'); from vel import rgbp, model_op_schaal
def gen3(s,bg):
    im=Image.open(f'../../../../graphics/pokemon/{s}/anim_front.png'); q=np.asarray(im)[:64]; pal=np.array(im.getpalette()[:48]).reshape(-1,3)
    img=np.zeros((64,64,3),'uint8'); img[:]=bg
    for k in range(1,16): img[q==k]=pal[k]
    return Image.fromarray(img)
v=Image.new('RGB',(3*520,14+512+20+150),'white'); d=ImageDraw.Draw(v)
for i,(nm,im) in enumerate((('r5',rgbp(f'{UIT}/pinsir_evo_r5.png')),('r4 A',rgbp('sprite_r4/pinsir_evo_r4_A.png')),('model',model_op_schaal()))):
    v.paste(im.resize((512,512),Image.NEAREST),(i*520,14)); d.text((i*520+2,0),nm+' 8x',fill=(0,0,0))
y=14+512+20
for j,bg in enumerate(((255,255,255),(40,48,56))):
    for i,im in enumerate([rgbp(f'{UIT}/pinsir_evo_r5.png',bg),rgbp('sprite_r4/pinsir_evo_r4_A.png',bg)]+[gen3(s,bg) for s in ('pinsir','heracross','scizor')]):
        v.paste(im,(i*70,y+j*70))
d.text((370,y+20),'1x: r5 | r4 A | Gen 3 Pinsir, Heracross, Scizor (wit / donker)',fill=(0,0,0))
v.save(f'{UIT}/vel.png'); print('vel',v.size)
