# Kricketune-evolutie r1: MODEL OVERNEMEN. Natief raster 99x99 (pitch 10,24), figuur 75x85 -> 56x64 door 19 kolommen en 21 rijen
# te schrappen (GEMINI.md, Gengas/Alphyena). Geschrapte rij/kolom valt samen met de buur die er het meest op lijkt (achtergrond
# verliest, oog/hemd winnen; schrap.py), zodat 1-px antennes en randen niet breken. Elke pixel blijft een modelpixel.
# Daarna alleen palet, technische opschoning en benoemde reparaties; elke stap geteld.
# Bouwen: cd kricketune_evo && python3 sprite_r1/bouw.py [kaal|toon]
import sys, numpy as np
sys.path.insert(0,'gereedschap'); from gemeen import *; import schrap as S
from PIL import Image
UIT='sprite_r1'
a,c,L=klassen()
S.PRIO={11:4,5:4,4:4}
s,rows,cols=S.schrap_merge(c)
KM={0:0,1:1,2:2,3:3,4:5,5:6,6:7,7:8,8:9,9:10,10:11,11:12}   # modelklasse -> paletindex
o=np.zeros((64,64),int); H,W=s.shape
o[Y0:Y0+H,X0:X0+W]=np.vectorize(KM.get)(s)
kaal=o.copy(); opslaan(kaal,UIT+'/kaal.png')
if len(sys.argv)>1 and sys.argv[1]=='kaal': toon(o); sys.exit()
tel={}
def stap(n,v,o): tel[n]=tel.get(n,0)+int((v!=o).sum())
N4=((-1,0),(1,0),(0,-1),(0,1))
# --- 1. buitenlijn: elke randpixel (achtergrond als 4-buur) die geen lijn is. Pak/hand/snor/benen: zwart rondom (zoals het model).
#        Rood: schaduwkant (achtergrond rechts of onder) zwart, lichtkant (alleen links/boven) donkerrood 7 (model: selout r1 links
#        langs de kop en antennes). ---
def rand(o):
    f=o>0; uit=[]
    for Y,X in zip(*np.where(f)):
        k=o[Y,X]
        if k in (1,7): continue
        bg=[not f[Y+dy,X+dx] if 0<=Y+dy<64 and 0<=X+dx<64 else True for dy,dx in N4]   # boven, onder, links, rechts
        if not any(bg): continue
        if k in ROOD and not (bg[1] or bg[3]):
            # dunne rode streng (antenne): rood is maar 1 px dik tussen achtergrond en lijn -> rood blijft, selout komt erbuiten
            # (de reductie maakte de 3-px modelstreng K|rood|K 2 px; zo wordt hij weer selout|rood|K)
            if bg[0] and Y+1<64 and o[Y+1,X] in (1,7): uit.append((Y-1,X,7)); continue
            if bg[2] and not bg[0] and X+1<64 and o[Y,X+1] in (1,7): uit.append((Y,X-1,7)); continue
            n=7
        else: n=1
        if n!=k: uit.append((Y,X,n))
    for Y,X,k in uit: o[Y,X]=k
v=o.copy(); rand(o); stap('buitenlijn',v,o)

# --- 2. ogen (toegestane afwijking 2): Kricketune-ogen pixel voor pixel uit graphics/pokemon/kricketune/anim_front.png (frame 1) op de
#        plek van de modelogen. Dichtbij: kt x31-34,y17-22 -> +1,-5 (glans en pupil vallen op glans/pupil van het model); veraf:
#        kt x24-27,y20-23 -> +1,-6. Alleen de oogpixels (kt-index 4 zwart, 5 donker, 6 grijsbruin, 7 wit). Modeloogpixels die buiten het
#        Kricketune-oog vallen (grijsbruin, wit, donker, zwarte kern) krijgen de kopkleur van hun rode buren. ---
from PIL import Image as _I
KT=np.asarray(_I.open('../../../../graphics/pokemon/kricketune/anim_front.png')).astype(int)
KTM={4:1,5:2,6:12,7:6}
v=o.copy()
OOG=[((31,35,17,23),(1,-5),(33,36,12,18)),((24,28,20,24),(1,-6),(25,29,14,18))]
for (kx0,kx1,ky0,ky1),(dx,dy),(bx0,bx1,by0,by1) in OOG:
    gezet=set()
    for y in range(ky0,ky1):
        for x in range(kx0,kx1):
            if KT[y,x] in KTM: o[y+dy,x+dx]=KTM[KT[y,x]]; gezet.add((y+dy,x+dx))
    for y in range(by0,by1):
        for x in range(bx0,bx1):
            if (y,x) in gezet or v[y,x] not in (1,2,3,6,12): continue
            if all(v[y+ey,x+ex]>0 for ey,ex in N4) and (v[y,x] in (12,6) or any(v[y+ey,x+ex] in (12,6) for ey,ex in N4)):
                nb=[o[y+ey,x+ex] for ey,ex in N4 if o[y+ey,x+ex] in (8,9,10,11)]
                o[y,x]=max(set(nb),key=nb.count) if nb else 9
stap('ogen (Kricketune)',v,o)
# --- 3. vinger (toegestane afwijking 1): de stok is een vinger in de handtinten. Bij het schrappen kreeg hij knikken (helling 1 onderaan,
#        lijn onderbroken); opnieuw gelegd als rechte lijn op de modellijn: tip (4-5,0), daarna per rij zwart | handtint midden | zwart,
#        midden van x5 (y1) naar x13 (y13) (helling 2:3 zoals het model, 0,6). Tweede vinger en hand blijven zoals de reductie. ---
v=o.copy()
MX={1:5,2:6,3:6,4:7,5:8,6:8,7:9,8:10,9:10,10:11,11:12,12:12,13:13}
for y in range(0,11): o[y,0:13]=0
o[0,4]=1; o[0,5]=1
for y,m in MX.items():
    if y>=11: o[y,max(0,m-3):m-1]=0
    o[y,m-1]=1; o[y,m]=3; o[y,m+1]=1 if o[y,m+1]!=3 else 3
stap('vinger',v,o)

# --- 4. (UIT in r1, alleen met argument 'donkerrood') binnenlijnen in het rood (Gen 3: binnenlijn in een donkere tint van het vlak waar vorm over vorm valt): zwarte modellijnen die
#        alleen rood scheiden (geen achtergrond als 4-buur, alle niet-zwarte 8-buren rood) -> donkerrood 7. Zwart blijft waar rood aan
#        pak/hand/snor/hemd grenst en op de buitenrand. Het model is 31 % zwart (Gen 3 ±12-19 %); op 64 px wordt dat een zwart net. ---
ZWARTE_BINNENLIJNEN='donkerrood' not in sys.argv   # r1: zwart (model, en Kricketune heeft zwarte binnenlijnen); 'donkerrood' = proef
v=o.copy()
for _ in range(3):
    w=o.copy(); P=np.pad(w,1)
    for Y,X in zip(*np.where(w==1)):
        n4=[P[Y+1+dy,X+1+dx] for dy,dx in N4]
        if 0 in n4: continue
        n8=[P[Y+1+dy,X+1+dx] for dy in (-1,0,1) for dx in (-1,0,1) if dy or dx]
        if 0 in n8: continue
        rest=[q for q in n8 if q!=1]
        if ZWARTE_BINNENLIJNEN: continue
        if rest and all(q in ROOD for q in rest) and sum(q in ROOD for q in n4)>=2: o[Y,X]=7
stap('binnenlijnen rood -> donkerrood',v,o)
# --- 5. rood naar 3 tinten + lijn: modeltint r2 (diepe schaduw, 140,40,40) valt samen met de lijntint 7 (Gen 3: donkerste tint is
#        lijn en kernschaduw tegelijk); r3/r4/r5 = schaduw/midden/licht. ---
v=o.copy(); o[o==8]=7; stap('rood r2 -> lijntint',v,o)

# --- 6. snorkrul: bij het schrappen viel kolom 20 (de 1-px opening tussen hand en krul) weg en rij 23 (boog van de krul) samen met
#        rij 24, zodat krul en hand één zwarte balk werden. Rij 18 opnieuw uit model-rij 23+24: hand-rand x18 | opening | krul K m K. ---
v=o.copy()
o[18,19]=0; o[18,20]=1; o[18,21]=3; o[18,22]=1
stap('snorkrul (opening hand | krul)',v,o)
# --- 6b. einde rechter antenne (model x70-72 y22-23: rood tot vlak voor de punt): rij 23 viel bij het schrappen weg, de punt werd
#         zwart. Rood terug op (56,17) (57,17) uit model-rij 23, selout erboven op (56,16) (57,16) (lichtkant). ---
v=o.copy()
o[17,56]=9; o[17,57]=9; o[16,56]=7; o[16,57]=7
stap('einde rechter antenne',v,o)
# --- 7. ontkorrelen rood: tintvlekjes < 3 px (4-samenhangend) van schaduw/midden (9/10) en losse 1-px hooglichtjes (11) nemen de
#        meest voorkomende rode buurtint aan; 2-px hooglichtjes blijven (glans). Lijnen (zwart, donkerrood) blijven. ---
v=o.copy()
OOGZONE=np.zeros((64,64),bool); OOGZONE[12:19,24:37]=True
for _ in range(2):
    for k in (9,10,11):
        lab,n=label(o==k,acht=False)
        for i in range(1,n+1):
            mm=lab==i; sz=mm.sum()
            if sz>=3 or (k==11 and sz==2): continue
            for Y,X in np.argwhere(mm):
                nb=[o[Y+dy,X+dx] for dy,dx in N4 if o[Y+dy,X+dx] in (9,10,11) and o[Y+dy,X+dx]!=k]
                if nb: o[Y,X]=max(set(nb),key=nb.count)
stap('ontkorrelen rood',v,o)
# --- 8. losse lijnpixels: donkerrood (7) of zwart (1) zonder lijnbuur (8-buren zonder 1/7) en zonder achtergrond, buiten de ogen:
#        midden in rood -> rode buurtint, midden in pak -> pak. ---
v=o.copy()
for Y,X in zip(*np.where(np.isin(o,(1,7)))):
    if OOGZONE[Y,X]: continue
    P=np.pad(o,1); nb8=[P[Y+1+dy,X+1+dx] for dy in (-1,0,1) for dx in (-1,0,1) if dy or dx]
    if 0 in nb8 or 1 in nb8 or 7 in nb8: continue
    r=[q for q in nb8 if q in (9,10,11)]; p=[q for q in nb8 if q in PAK]
    if len(r)>=len(p) and r: o[Y,X]=max(set(r),key=r.count)
    elif p: o[Y,X]=max(set(p),key=p.count)
stap('losse lijnpixels',v,o)
# --- 9. buitenrand: geen donkerrood-selout tussen zwart (om en om): losse 7 op de rand met zwart aan beide kanten -> zwart ---
v=o.copy()
f=o>0; P=np.pad(f,1)
R={(X,Y) for Y,X in zip(*np.where(f)) if not all(P[Y+1+dy,X+1+dx] for dy,dx in N4)}
for X,Y in sorted(R):
    if o[Y,X]!=7: continue
    nb=[o[Y+dy,X+dx] for dx in (-1,0,1) for dy in (-1,0,1) if (dx or dy) and (X+dx,Y+dy) in R]
    if 1 in nb and 7 not in nb: o[Y,X]=1
stap('buitenrand: geen om en om',v,o)

# --- 10. rokpanden en been (onderdelen die bij het schrappen wegvielen; terug op hun modelplek):
#   a. linker rokpand: de rode voering langs de buitenrand (model: doorlopend K | voering | pak) viel weg in y41-46 (rand werd selout
#      of pak). Voering terug op x22 (rood licht 10) met zwarte rand op x21 (y41-43 nieuw, +3 px silhouet).
#   b. rechter rokpand: voering (model-kolom 66) viel weg in y53-54 (kolom geschrapt, zwart won): x53 -> rood 9.
#   c. linkerbeen y51-53: modelkolom 34 (vulling) geschrapt, het been was alleen omlijning (K K); zoals y54-57: x28 K | x29 pak | x30 K. ---
v=o.copy()
for y in range(41,47): o[y,21]=1; o[y,22]=10
for y in (53,54): o[y,53]=9
for y in (51,52,53): o[y,28]=1; o[y,29]=2; o[y,30]=1
o[50,29]=2
stap('rokpanden (voering) en linkerbeen',v,o)

zonder=o.copy()
# --- 11. KLEDING (toegestane afwijking 3, Jordi: "is teveel kleding, maar die kan je in een sprite ook wat meer lichaamsvorm geven").
#        Alleen kleur, geen vorm: silhouet, kleurzones en onderdelen blijven. Het jasje over borst, schouders en mouwen krijgt volume
#        zoals stof die strak om een lijf zit: per jasdeel (gescheiden door de zwarte modellijnen) een geblurd masker -> normaal ->
#        licht van linksboven; lichtkant pak 2 -> 3, sterkste licht 3 -> 4 (nieuwe pak-lichttint). De rokpanden (vanaf y44) blijven
#        vlak donker: los hangende stof. Zonder deze stap: kricketune_evo_r1_zonder_kleding.png. ---
def blur(m,sg):
    r=int(3*sg); k=np.exp(-np.arange(-r,r+1)**2/(2*sg*sg)); k/=k.sum()
    p=np.pad(m,r); p=np.apply_along_axis(lambda q:np.convolve(q,k,'same'),0,p); p=np.apply_along_axis(lambda q:np.convolve(q,k,'same'),1,p)
    return p[r:-r,r:-r]
v=o.copy()
J=np.isin(o,(2,3)); J[:22,:]=False; J[44:,:]=False; J[:,49:]=False; J[:24,:20]=False
lab,n=label(J,acht=False)
for i in range(1,n+1):
    mm=lab==i
    if mm.sum()<6: continue
    b=blur(mm.astype(float),1.3); gy,gx=np.gradient(b); sc=(gx+gy)/np.sqrt(2)
    for Y,X in np.argwhere(mm):
        if sc[Y,X]>0.07 and o[Y,X]==3: o[Y,X]=4
        elif sc[Y,X]>0.025 and o[Y,X]==2: o[Y,X]=3
# losse 1-px lichtvlekjes (< 2 px) terug naar de buurtint (geen ruis)
for k in (3,4):
    lb,nn=label((o==k)&(v!=k),acht=False)
    for i in range(1,nn+1):
        mm=lb==i
        if mm.sum()<2:
            for Y,X in np.argwhere(mm): o[Y,X]=v[Y,X]
stap('kleding: volume jasje (licht linksboven)',v,o)
opslaan(zonder,UIT+'/kricketune_evo_r1_zonder_kleding.png')
opslaan(o,UIT+('/kricketune_evo_r1.png' if ZWARTE_BINNENLIJNEN else '/proef_donkerrood.png'))
print('afwijkingen van de kale reductie per stap:'); [print('  %-44s %d'%(k,v)) for k,v in tel.items()]
print('zonder kleding: anders dan kaal',int((zonder!=kaal).sum()),'| kleding-stap',int((o!=zonder).sum()),'px')
print('totaal anders dan kaal:',int((o!=kaal).sum()),'| silhouet-diff:',int(((o>0)!=(kaal>0)).sum()),'| figuur',int((o>0).sum()),'px')
if len(sys.argv)>1 and sys.argv[1]=='toon': toon(o)
