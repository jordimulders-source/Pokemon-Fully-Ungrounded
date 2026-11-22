# Pinsir-evolutie r2 (op r1; mond en kaken van r1 bevroren). Wijzigingen r2: lijf als platen (model.platen) onder y36, zwart
# weegt 1,0 i.p.v. 1,3 (model: echt zwart L<12 = ±21 % van de figuur), dekschild meer donkere tekening, stekels opgeschoond, ogen.
# Basis r1: MODEL OVERNEMEN. Het 1024-model (bevroren r4B) wordt per spritecel (974/64 = 15,22 modelpx) gereduceerd:
# de modelklasse met de meeste pixels wint (zwart weegt 1,3x zodat de modellijnen blijven). Daarna alleen technische opschoning
# en benoemde reparaties (mond, ogen); elke stap geteld. Bouwen: cd pinsir_evo && python3 sprite_r2/bouw.py [kaal|toon]
import sys, numpy as np
sys.path.insert(0,'gereedschap'); from model import *; from gemeen import *
UIT='sprite_r2'
R1=np.asarray(__import__('PIL.Image',fromlist=['Image']).open('sprite_r1/pinsir_evo_r1.png')).astype(int)
CEL=974/64; MX0,MY0=31,134; DY=13          # modeluitsnede: x31.., y134.. ; in de sprite rij 13-61
ALPHA=0.35                                 # silhouet: cel hoort bij de figuur bij >= 35 % modeldekking (dunne stekels, zaagtanden en klauwen blijven)
a,c,fg=klassen()
# punt 1 (poten/onderlijf): onder sprite-y36 (model y >= 484) is het lijf opgebouwd uit modelplaten: elke door zwarte modellijnen
# omsloten plaat = 1 vlak in de band van zijn mediane modelhelderheid, licht (5) alleen op de modelglans (helderheid >= max(95, mediaan+20)).
c2,_,_=platen(a,c,fg)
YC=int(MY0+(36-DY)*CEL)
cm=c.copy(); cm[YC:]=c2[YC:]
# punt 3: zwart weegt 1,0 (r1: 1,3); de modellijnen zijn echt zwart (L<12), maar dik (±0,66 spritepixel), dus 1,3 gaf 31 % zwart
r,fr=reduceer(cm,fg,MX0,MY0,CEL,64,49,1.0,ALPHA)
# in de platenzone (y>=36): vlak = grootste niet-zwarte plaatklasse van de cel; lijn = waar de middellijn (skelet) van een zwarte
# modellijn door de cel loopt (>= 9 skeletpixels; een cel is 15 px) of waar het model >= 70 % zwart is. Zo worden de plaatranden
# doorlopende 1-px lijnen op de modellijnen i.p.v. losse brokken (meerderheid per cel verloor ze).
sk=skeletlijnen(c,MX0,MY0,CEL,64,49)
for j in range(36-DY,49):
    for i in range(64):
        if not r[j,i]: continue
        f=fr[j,i]
        if f[1]>=0.7 or sk[j,i]>=9: r[j,i]=1
        else:
            h=f.copy(); h[:2]=0; r[j,i]=int(h.argmax())
o=np.zeros((64,64),int); o[DY:DY+49]=r
# punt 4: stekelpunten. De kleine modelstekels op kopschild en rug zijn 1-2 spritepx breed en vielen onder de 35 %-drempel weg;
# boven y21 telt een cel die direct op de figuur staat al mee bij >= 25 % modeldekking (alleen de stekels van het model).
ff=fr.sum(2)
for _ in range(2):
    for Y in range(20,12,-1):
        for X in range(64):
            if o[Y,X]==0 and ff[Y-DY,X]>=0.25 and o[Y+1,X]>0: o[Y,X]=1
kaal=o.copy(); opslaan(kaal,UIT+'/kaal.png')
if len(sys.argv)>1 and sys.argv[1]=='kaal': toon(o); sys.exit()
tel={}
def stap(n,v,o): tel[n]=tel.get(n,0)+int((v!=o).sum())
N4=((-1,0),(1,0),(0,-1),(0,1)); N8=[(dy,dx) for dy in (-1,0,1) for dx in (-1,0,1) if dy or dx]
def mat(k): return 'L' if k in LIJF else 'K' if k in KAAK else 'S' if k in SCHILD else 'T' if k in (12,13) else 'Z' if k==1 else ''
def P(o,Y,X): return o[Y,X] if 0<=Y<64 and 0<=X<64 else 0
GEZICHT=np.zeros((64,64),bool); GEZICHT[DY+13:DY+23,15:25]=True     # ogen + mond: stap 4, uit het model per pixel
# --- 1. tintvlekjes < 3 px (4-samenhangend) nemen de meest voorkomende buurtint van hetzelfde materiaal aan (ruis van de reductie) ---
v=o.copy()
for _ in range(3):
    for k in list(LIJF|KAAK|SCHILD):
        lab,n=label(o==k,False)
        for i in range(1,n+1):
            m=lab==i
            if m.sum()>=3: continue
            for Y,X in np.argwhere(m):
                if GEZICHT[Y,X]: continue
                nb=[P(o,Y+dy,X+dx) for dy,dx in N8]
                zelf=[q for q in nb if q!=k and mat(q)==mat(k)]
                if zelf: o[Y,X]=max(set(zelf),key=zelf.count)
stap('1 tintvlekjes',v,o)
# --- 1b. lijf: draadjes van 1 px breed (eigen tint <= 2 van de 3x3, een andere lijftint >= 4) nemen die tint aan, zodat de
#         pantserplaten als vlakken lezen (ruis van de reductie op de gestreepte modeltextuur) ---
v=o.copy()
for _ in range(2):
    w=o.copy()
    for Y,X in zip(*np.where(np.isin(w,(2,3,4,5)))):
        if GEZICHT[Y,X]: continue
        q=[P(w,Y+dy,X+dx) for dy in (-1,0,1) for dx in (-1,0,1)]
        cnt={k:q.count(k) for k in (2,3,4,5)}
        if cnt[w[Y,X]]<=2:
            k=max(cnt,key=cnt.get)
            if cnt[k]>=4: o[Y,X]=k
stap('1b lijf draadjes',v,o)
# --- 2. losse zwarte stukjes (8-cluster <= 3 px) die niet aan de achtergrond grenzen -> buurtint (ruis van de reductie) ---
v=o.copy()
lab,n=label(o==1,True)
for i in range(1,n+1):
    m=lab==i
    if m.sum()>3: continue
    pts=np.argwhere(m)
    if any(P(o,Y+dy,X+dx)==0 for Y,X in pts for dy,dx in N8): continue
    for Y,X in pts:
        if GEZICHT[Y,X]: continue
        nb=[P(o,Y+dy,X+dx) for dy,dx in N8 if P(o,Y+dy,X+dx)>1]
        if nb: o[Y,X]=max(set(nb),key=nb.count)
stap('2 losse zwarte pixels',v,o)
# --- 3. dekschild: schorsvlekken als minder, grotere vlekken op de modelplekken (GEMINI.md poedelmot: patroon op 64 px wordt dambord).
#        Per cel het modelaandeel vlek/midden/licht binnen het schild, 3x3 gewogen gemiddeld (midden 4x), drempels; vlekjes < 3 px weg. ---
v=o.copy()
SM=np.isin(o,list(SCHILD))
fs=np.zeros((64,64,3)); fs[DY:DY+49]=fr[...,9:12]
tot=fs.sum(2)+1e-9; pv=fs[...,0]/tot; pm=fs[...,1]/tot; pl=fs[...,2]/tot
def glad(q):
    Q=np.pad(q*SM,1); W=np.pad(SM.astype(float),1); s=np.zeros_like(q); w=np.zeros_like(q)
    for dy in (-1,0,1):
        for dx in (-1,0,1):
            g=4 if dy==dx==0 else 1
            s+=g*Q[1+dy:65+dy,1+dx:65+dx]; w+=g*W[1+dy:65+dy,1+dx:65+dx]
    return s/np.maximum(w,1e-9)
gv,gm,gl=glad(pv),glad(pm),glad(pl)
keus=np.full((64,64),10); keus[gl>=0.30]=11; keus[gv>=0.50]=9     # midden als grond, vlek/licht waar het model ze duidelijk heeft (3 varianten bekeken, deze lijkt het meest op het model)
o[SM]=keus[SM]
for k in (9,11):
    lab,n=label(o==k,False)
    for i in range(1,n+1):
        if (lab==i).sum()<3: o[lab==i]=10
stap('3 dekschild vlekken',v,o)
# --- 4. mond (Pinsir-mond van het model): bij 15 modelpx per spritepixel lopen de 5 tandrijen van het model dicht (kaal: 4 vage
#        crème vlekjes). Gemeten modelaandeel tand per cel: tanden in x17 (linkerkolom), x19-20 (rechterkolom), scheiding x18,
#        rijen 30-33; zwart kader x16 / x22, boven y29, onder y34-35; x21 = grijze wang binnen het kader (model).
#        Opbouw zoals de Gen 3-Pinsir (tanden en zwarte scheidingen om en om): 3 tandrijen (y30, 32, 34) i.p.v. 5; onderste rij in
#        tandschaduw 13 (model: onderste tanden kleiner en grijzer). Het kader loopt daardoor 1 rij lager (y35) dan de modeltanden. ---
v=o.copy()
for X in range(17,22): o[29,X]=1; o[35,X]=1
for Y in range(30,35):
    o[Y,16]=1; o[Y,22]=1; o[Y,21]=4
    for X in range(17,21): o[Y,X]=1
    if Y in (30,32,34):
        t=13 if Y==34 else 12
        o[Y,17]=t; o[Y,19]=t; o[Y,20]=t
# ogen (model: crème spleetjes onder de kopschildrand; gemeten x16.2-16.7 y26.8-28.2 links, x20.9-23.5 y27.7-28.7 rechts):
# links (16,27) = kaal; rechts 3 px (21-23,28): de kaal hield er 2 (rechterpunt 27 % dekking viel weg) -> (23,28) erbij.
o[27,16]=12; o[28,21]=12; o[28,22]=12; o[28,23]=12
stap('4 mond',v,o)
# --- 5. buitenlijn (Gen 3): elke randpixel (achtergrond als 4-buur) wordt lijn; schaduwkant (achtergrond onder of rechts) zwart,
#        lichtkant (achtergrond alleen boven/links) gekleurde selout in de donkerste tint van het materiaal (kaak 6, schild 9, lijf 3).
#        Een losse seloutpixel tussen zwart op de rand wordt zwart (nooit om en om). ---
SEL={'K':6,'S':9,'L':3}
def rand(o):
    f=o>0; uit=[]
    for Y,X in zip(*np.where(f)):
        k=o[Y,X]
        bg=[not f[Y+dy,X+dx] if 0<=Y+dy<64 and 0<=X+dx<64 else True for dy,dx in N4]   # boven, onder, links, rechts
        if not any(bg): continue
        if k==1: continue
        n=1 if (bg[1] or bg[3] or mat(k) not in SEL) else SEL[mat(k)]
        if n!=k: uit.append((Y,X,n))
    for Y,X,k in uit: o[Y,X]=k
    f=o>0; Pf=np.pad(f,1)
    R={(X,Y) for Y,X in zip(*np.where(f)) if not all(Pf[Y+1+dy,X+1+dx] for dy,dx in N4)}
    for X,Y in sorted(R):
        if o[Y,X] not in (3,6,9): continue
        nb=[o[Y+dy,X+dx] for dx in (-1,0,1) for dy in (-1,0,1) if (dx or dy) and (X+dx,Y+dy) in R]
        if 1 in nb and not any(q==o[Y,X] for q in nb): o[Y,X]=1
v=o.copy(); rand(o); stap('5 buitenlijn',v,o)
# --- 6. binnenlijnen (Gen 3: binnenlijn in de donkere tint van het vlak, zwart alleen waar materialen of de donkere lijfmassa
#        samenkomen). Zwarte modellijn binnenin (geen achtergrond in de 8-buren), buiten de mond/ogen: grenzen alle niet-zwarte buren
#        aan lichter lijf (3/4/5) -> 2; alleen kaak -> 6; alleen schild -> 9. Lijn blijft op zijn modelplek. ---
v=o.copy()
for Y,X in zip(*np.where(o==1)):
    if GEZICHT[Y,X]: continue
    nb=[P(v,Y+dy,X+dx) for dy,dx in N8]
    if 0 in nb: continue
    q=[k for k in nb if k!=1]
    if not q: continue
    if all(k in (3,4,5) for k in q): o[Y,X]=2
    elif all(k in LIJF for k in q) and sum(k in (3,4,5) for k in q)>=2: o[Y,X]=2   # r2: plaatrand tussen donkere massa en lichtere plaat -> donkerste lijftint
    elif all(k in KAAK for k in q): o[Y,X]=6
    elif all(k in SCHILD for k in q): o[Y,X]=9
stap('6 binnenlijnen',v,o)
# --- 6b. punt 3 (zwart gemeten): model zwart (L<25) = 22,7 % van de figuur. Zwarte binnenpixel (geen achtergrond in de 8-buren) waar
#         het model in die cel < 50 % zwart heeft = randgeval van de reductie -> de donkerste lijftint (2) of, in kaak/schild, hun
#         donkerste tint. Lijnen met >= 50 % modelzwart blijven zwart. ---
v=o.copy()
for Y,X in zip(*np.where(o==1)):
    if GEZICHT[Y,X] or Y-DY<0 or Y-DY>=49: continue
    nb=[P(v,Y+dy,X+dx) for dy,dx in N8]
    if 0 in nb or (Y>=36 or fr[Y-DY,X,1]>=0.5): continue    # platenzone: lijnen komen uit het skelet
    q=[k for k in nb if k>1]
    if not q: continue
    o[Y,X]=6 if all(k in KAAK for k in q) else 9 if all(k in SCHILD for k in q) else 2
stap('6b zwart -> donkerste tint (model < 50 % zwart)',v,o)
# --- 7. controle-ronde: na stap 5/6 nog losse zwarte pixels binnenin (geen zwarte 8-buur, geen achtergrond) -> buurtint ---
v=o.copy()
for Y,X in zip(*np.where(o==1)):
    if GEZICHT[Y,X]: continue
    nb=[P(o,Y+dy,X+dx) for dy,dx in N8]
    if 0 in nb or 1 in nb: continue
    o[Y,X]=max(set(nb),key=nb.count)
stap('7 losse zwarte pixels (controle)',v,o)
rand(o)
# --- 7b. punt 4: rugstekels en kopschildstekels (y <= 20, horizontale loop van de figuur <= 3 px = een stekel uit het model) krijgen
#         één vaste opbouw zoals de modelstekels (lichte linkerflank, donkere rechterflank): achtergrond rechts of boven-rechts
#         (schaduwkant, punt) -> zwart; achtergrond links -> selout 3; binnenin -> 4 (belichte stekeltint). Vorm = model. ---
v=o.copy()
for Y in range(13,21):
    X=0
    while X<64:
        if v[Y,X]==0: X+=1; continue
        X1=X
        while X1<64 and v[Y,X1]>0: X1+=1
        if X1-X<=3:
            for x in range(X,X1):
                if v[Y,x] not in LIJF and v[Y,x]!=1: continue
                if P(v,Y,x+1)==0 or P(v,Y-1,x+1)==0 and P(v,Y-1,x)==0 and x==X1-1: o[Y,x]=1
                elif P(v,Y,x-1)==0: o[Y,x]=3
                else: o[Y,x]=4
        X=X1
stap('7b stekels',v,o)
# --- 8. klauwen (poten, y >= 52): de model-klauwen zijn belichte pantsertinten met een zwarte lijn; op 15 modelpx per spritepixel
#        werd een klauw vaak geheel zwart (lijn won). Zwarte cel binnenin (niet aan de rand: de onderrand blijft zwart, schaduwkant)
#        met >= 35 % belichte lijftint in het model -> de grootste lijftint van het model in die cel. ---
v=o.copy()
for Y,X in zip(*np.where(o==1)):
    if Y<52 or Y-DY>=49: continue
    f=fr[Y-DY,X]
    if f[3:6].sum()<0.35: continue
    if any(P(v,Y+dy,X+dx)==0 for dy,dx in N4): continue
    o[Y,X]=int(np.argmax(f[2:6])+2)
stap('8 klauwen',v,o)
# --- 9. bevroren (coördinator: "de mond en de kaken zijn goed"): kaakpixels van r1 + 1 px eromheen en het gezichtsvak (x13-24,
#        y26-36) komen 1-op-1 uit r1 ---
from scipy import ndimage
FROZ=ndimage.binary_dilation(np.isin(R1,list(KAAK)),structure=np.ones((3,3)))
FROZ[26:37,13:25]=True
v=o.copy(); o[FROZ]=R1[FROZ]; stap('9 bevroren uit r1 (mond, kaken)',v,o)
# --- 10. punt 5, ogen (Jordi: "ogen zijn ook gewoon een rij witte pixels"). Model (gemeten op 8x): boze, schuine ogen onder de
#         kopschildrand. Links: crème van (16,27) schuin omlaag naar (17,28), zwart (17,27) erboven-rechts (wenkbrauw). Rechts: klein
#         stukje (21,28) + hoofdstuk (22-23,28), hoofdstuk hoger aan de buitenkant (schuin omlaag naar het midden), zwarte
#         wenkbrauwband y27, donkere inkeping rechtsonder in het hoofdstuk (pupil). Opbouw zoals Gen 3-Pinsir (wit, zwarte pupil in een
#         onderhoek, zwarte wenkbrauw die aan de binnenkant op het oog drukt), 2 rijen hoog (y27-28, niet y29: dan smelt het oog met de mondrand) zodat de pupil past. ---
v=o.copy()
for X,Y,k in [
    (16,27,12),            # links oogwit (model crème)
    (16,28,12),            # links oogwit, 2e rij (nieuw; model: gezicht 3)
    (17,27,1),             # links wenkbrauw (model zwart)
    (17,28,1),             # links pupil rechtsonder (model: klein crème stukje, daarnaast zwart)
    (21,28,1),             # rechts: wenkbrauwpunt drukt aan de binnenkant op het oog (model: klein crème stukje)
    (22,27,12),(23,27,12), # rechts oogwit bovenrij (model: zwarte wenkbrauwband; het hoofdstuk begint op y27,7) - oog 2x2 zoals Gen 3-Pinsir
    (22,28,12),            # rechts oogwit (model crème)
    (23,28,1),             # rechts pupil rechtsonder (model: donkere inkeping rechtsonder in het hoofdstuk)
    (22,26,1),(23,26,1),(24,26,1),  # rechts wenkbrauwband 1 rij omhoog mee met het oog (model: zwarte band direct boven het oog; was lijf 5)
    ]:
    o[Y,X]=k
stap('10 ogen',v,o)
opslaan(o,UIT+'/pinsir_evo_r2.png')
if len(sys.argv)>1 and sys.argv[1]=='toon': toon(o)
print('afwijkingen van de kale reductie per stap:'); [print('  %-36s %d'%(k,v)) for k,v in tel.items()]
OG=np.zeros((64,64),bool); OG[26:30,15:25]=True
print('anders dan r1:',int((o!=R1).sum()),'| bevroren zone (zonder ogen) diff met r1:',int((o[FROZ&~OG]!=R1[FROZ&~OG]).sum()))
print('totaal anders dan kaal:',int((o!=kaal).sum()),'van',int((o>0).sum()),'| silhouet-diff met kaal r2:',int(((o>0)!=(kaal>0)).sum()),'| met r1:',int(((o>0)!=(R1>0)).sum()),[(int(x),int(y)) for y,x in zip(*np.where((o>0)!=(R1>0)))])
