# Pinsir-evolutie r11 (laatste serieuze poging; Jordi: "Ik wil dat je nog een hele serieuze poging doet om er iets van te maken,
# anders schrap ik dit idee").
# Basis = sprite_r10/pinsir_evo_r10.png (oog A). BEVROREN (script-check, diff 0): arm, verre arm, been, ver been, staart, kaken,
# mond, romp, gezicht/ogen van r10, silhouet van de kop (behalve 1-px stekelpunten, zie STEKELS).
# Model = overnemen, nooit hertekenen: vorm, plaats en aantal uit het bevroren model (referenties/gemini_gekozen_r4B.png, registratie
# van sprite_r1: cel 974/64 modelpx, x31, y134, rij 13). Geen extra zwart.
# Wat r11 anders doet dan r10: VLAKKEN in plaats van celmediaan.
#  1. KOPSCHILD: per cel de modelklasse met de meeste pixels (na een modusfilter van 11 modelpx tegen Gemini-ruis), beperkt tot
#     3 vlakken + hooglicht: lichte afschuining (c, hooglicht d linksvoor), egaal middenvlak (b), donkere onderkant (L); daarna
#     tintvlekjes < 3 px opgeheven en de bovenrand als doorlopende lichte afschuining (1 px onder de omtrek).
#  2. STEKELS + KEGELS: plek en maat = modelmasker (r10-silhouet), opbouw naar Gen 3 (Tyranitar/Cacturne/Pinsir): punt 1 px zwart,
#     lichte flank links/boven (c), donkere flank rechts/onder (K), binnenin de gemeten modeltoon (b/a).
#  3. RUGDOORNS naast het schild: silhouet = modelmasker (dekking >= 0,35; r10 had daar de r8-rugrand die 1-4 px breder was dan
#     het model), zelfde stekelopbouw.
#  4. DEKSCHILD (Jordi: "je mag daar meer van het model afwijken zodat het naar een sprite vertaalt"): één bolle vorm (licht
#     linksboven, schaduwsikkel rechtsonder, diepe schaduw op de omgeslagen rand), modelvlekken versimpeld tot een paar grote
#     schorsvlekken met eigen schaduw (Shuckle/Beautifly: vlek volgt de bolling, één tint donkerder dan zijn ondergrond).
# Bouwen: cd pinsir_evo && python3 sprite_r11/bouw.py [raster]
import sys, numpy as np
from PIL import Image
from scipy import ndimage
UIT='sprite_r11'
CH='.KLabcdopqrsvwxT'; C={c:i for i,c in enumerate(CH)}
R10P='sprite_r10/pinsir_evo_r10.png'
R10=np.asarray(Image.open(R10P)).astype(int)
PAL=Image.open(R10P).getpalette()[:48]
ZONE=np.load('sprite_r10/zone.npy')                      # kopzone van r10
DEEL=np.load('sprite_r8/r7_delen.npy')
H=W=64; yy,xx=np.mgrid[:H,:W]
N4=((-1,0),(1,0),(0,-1),(0,1))
# ---------------- palet: alleen de dekschildtinten o/x/w/v (komen buiten het dekschild niet voor) ----------------
# tinten van het modelschild (licht (183,142,104), midden (141,104,73)/(111,74,44), vlek (62,37,19)) met Gen 3-stappen (±33):
DEKPAL={'o':(200,154,104),'x':(164,118,74),'w':(124,84,50),'v':(86,52,28)}   # L 153 / 119 / 86 / 55; s (66,36,18) L 40 blijft
for k,rgb in DEKPAL.items(): PAL[3*C[k]:3*C[k]+3]=list(rgb)
# ---------------- model ----------------
CEL=974/64; MX0,MY0,DY=31,134,13
A=np.asarray(Image.open('referenties/gemini_gekozen_r4B.png').convert('RGB')).astype(float)
LUM=A.mean(2); FG=A.min(2)<215
KL=np.zeros(LUM.shape,int); KL[FG]=4                     # 1 lijn <22 | 2 zeer donker <40 | 3 donker <54 | 4 midden | 5 licht >=80 | 6 hooglicht >=122
KL[FG&(LUM<54)]=3; KL[FG&(LUM<40)]=2; KL[FG&(LUM<22)]=1; KL[FG&(LUM>=80)]=5; KL[FG&(LUM>=122)]=6
KM=np.stack([ndimage.uniform_filter((KL==k).astype(float),11) for k in range(7)]).argmax(0)   # modusfilter 11 modelpx
def cel(j,i,shr=0.1):
    ya,yb=MY0+(j-DY)*CEL,MY0+(j+1-DY)*CEL; xa,xb=MX0+i*CEL,MX0+(i+1)*CEL; d=CEL*shr
    return int(round(ya+d)),int(round(yb-d)),int(round(xa+d)),int(round(xb-d))
def klasse(j,i):
    ya,yb,xa,xb=cel(j,i); f=np.bincount(KM[ya:yb,xa:xb].ravel(),minlength=7)/max((yb-ya)*(xb-xa),1)
    return 1 if f[1]>=0.40 else int(np.argmax(f[2:7])+2)
def licht(j,i):                                           # aandeel licht (>=80) in de cel: voor de stekelflanken
    ya,yb,xa,xb=cel(j,i,0); b=KL[ya:yb,xa:xb]; return (b>=5).mean() if b.size else 0
COV=np.zeros((H,W))
for j in range(H):
    for i in range(W):
        ya,yb,xa,xb=cel(j,i,0); b=FG[max(ya,0):max(yb,0),max(xa,0):max(xb,0)]; COV[j,i]=b.mean() if b.size else 0
lab,_=ndimage.label(FG&~(FG&(LUM<22)))                    # modelvlakken tussen de zwarte lijnen; 12 = kopschild (zie sprite_r6)
def vlak(j,i):
    ya,yb,xa,xb=cel(j,i,0); b=lab[ya:yb,xa:xb].ravel(); b=b[b>0]; return int(np.bincount(b).argmax()) if b.size else 0
# ---------------- bevroren ----------------
GEZICHT={(15,26),(16,26),(17,26),(14,27),(15,27),(16,27),(17,27),(18,27),(19,27),(20,27),(21,27),(22,27),(23,27),(24,27),
         (15,28),(16,28),(17,28),(18,28),(19,28),(20,28),(21,28),(22,28),(23,28),(24,28),(23,26)}   # r10 STAP 'gezicht' + OOG_A
GZ=np.zeros((H,W),bool)
for x,y in GEZICHT: GZ[y,x]=True
BEVROREN=np.isin(DEEL,['arm','arm_ver','been','been_ver','staart','romp','kop'])&~ZONE   # arm/been/staart/romp/kaken/mond
SCHILD10=np.isin(R10,[C['o'],C['x'],C['w'],C['v']])        # het r10-ovaal (o/x/w/v komen alleen daar voor)
def opslaan(q,path):
    p=Image.fromarray(q.astype('uint8'),'P'); p.putpalette(PAL+[0]*(768-len(PAL))); p.save(path,transparency=0)
def vlekjes(q,mask,minsz=3,vast=None):
    """tintvlekjes < minsz px (8-samenhangend: een schuine rand is een vorm) binnen mask opheffen: ze krijgen de meest
    voorkomende buurtint (geen K/0)."""
    for _ in range(8):
        n=0
        for t in sorted(set(q[mask].ravel())-{0,C['K']}):
            lb,k=ndimage.label((q==t)&mask,structure=np.ones((3,3)))
            for m in range(1,k+1):
                M=lb==m
                if M.sum()>=minsz or (vast is not None and (M&vast).any()): continue
                for y,x in zip(*np.where(M)):
                    nb=[q[y+dy,x+dx] for dy,dx in N4 if mask[y+dy,x+dx] and q[y+dy,x+dx] not in (0,t,C['K'])]
                    if nb: q[y,x]=max(sorted(set(nb)),key=nb.count); n+=1
        if not n: break
    return q
def stekel(q,pix,toon):
    """Gen 3-stekel: punt (>=3 lege 4-buren) K, donkere flank (lege buur rechts/onder) K, lichte flank (lege buur links/boven) c,
    binnenin de gemeten modeltoon."""
    sil=q>0
    for y,x in pix:
        leeg=[not sil[y+dy,x+dx] for dy,dx in N4]       # boven, onder, links, rechts
        if sum(leeg)>=3: q[y,x]=C['K']
        elif leeg[1] or leeg[3]: q[y,x]=C['K']
        elif leeg[0] or leeg[2]: q[y,x]=C['c']
        else: q[y,x]=C[toon(y,x)]
    return q
# ======================= 1. KOP =======================
TINT={1:'L',2:'L',3:'a',4:'b',5:'c',6:'d'}
# KOPSCHILD-vlakken: benoemde correcties op de klassenkaart, per cel gemeten (licht% in sprite_r11/NOTITIES.md)
KOPVLAK={(17,21):'d',(18,21):'d',                     # hooglicht: lichtste plek van de afschuining (licht 88 / 95 %)
         (32,23):'c',(33,23):'c',                     # lichte rand rechtsboven van het schild (59 / 63 %), loopt door in (34-35,24) en (35,25)
         (14,25):'b',                                 # onder de lichte onderrand (licht 0 %): middenvlak, geen losse lichte pixel
         (13,24):'b',(15,25):'c',(16,25):'c',         # lichte onderrand loopt diagonaal van de punt naar het gezicht (licht 30 / 45 / 87 %)
         (37,21):'L'}                                 # donkere kam naast K3 (licht 0 %)
def kop():
    q=R10.copy()
    # silhouet = r10; 1-px punten: S5 (32,13) en S6 (38,13) (model: punt x32,3-33,2 en x37,9-38,6, beide in één cel)
    PUNT_WEG=[(33,13)]
    for x,y in PUNT_WEG: q[y,x]=0
    KS=np.zeros((H,W),bool)
    for j,i in zip(*np.where(ZONE&(q>0)&~GZ)):
        k=klasse(j,i); KS[j,i]=vlak(j,i)==12
        q[j,i]=C[TINT[k]]
        if KS[j,i]: q[j,i]=C[{1:'L',2:'L',3:'L',4:'b',5:'c',6:'d'}[k]]   # kopschild: 3 vlakken + hooglicht
    sil=q>0
    for j,i in zip(*np.where(ZONE&sil&~GZ)):
        if any(not sil[j+dy,i+dx] for dy,dx in N4): q[j,i]=C['K']
    return q,KS,PUNT_WEG
# STEKELS op kop en kam: plek en maat = r10-silhouet (= modelmasker, dekking >= 0,35); per pixel de modelmeting
# (dekking%/licht%, licht = aandeel modelpixels >= 80) in sprite_r11/NOTITIES.md. Opbouw naar Gen 3 (Tyranitar/Cacturne/Pinsir):
# punt 1 px K, lichte flank links (c), donkere flank rechts (K = flank + omtrek), 3 breed: middelste pixel b (S5) of de lichte
# flank in het midden met een donkerbruine selout links (S6, model: zwarte lijn links), voet loopt over in schild/kam.
# Geen stekel van 2 px is meer helemaal zwart.
KOPSTEKELS={
 'S1':{(15,19):'K',(15,20):'c'},                                        # licht 47 %
 'S2':{(18,18):'K',(18,19):'c',(19,19):'K'},                            # licht 20 / 32 %
 'S3':{(23,16):'K',(23,17):'c',(24,17):'K',(23,18):'c',(24,18):'a',(25,18):'K',(23,19):'c',(24,19):'a'},   # 33 / 67 / 79 %
 'S4':{(26,15):'K',(26,16):'c',(27,16):'K',(26,17):'c',(27,17):'b',(28,17):'K'},                        # 38 / 35 %
 'S5':{(32,13):'K',(32,14):'c',(33,14):'K',(32,15):'c',(33,15):'b',(34,15):'K',(32,16):'c',(33,16):'b',(34,16):'K',
       (32,17):'c',(33,17):'a',(34,17):'a'},                            # 35 / 36 / 64 / 33 %
 'S6':{(38,13):'K',(38,14):'K',(38,15):'c',(39,15):'K',(37,16):'a',(38,16):'c',(39,16):'K',(37,17):'c',(38,17):'b',(39,17):'K',
       (37,18):'a',(38,18):'b',(39,18):'K'},                            # (38,14) licht 26 %: 1 px breed -> deel van de punt
 'S7':{(44,18):'K',(43,19):'c',(44,19):'a',(43,20):'c',(44,20):'K',(43,21):'c',(44,21):'K'}}            # 21 / 51 / 47 %
PUNT_WEG=[(33,13)]                                                       # S5-punt 1 px (model x32,3-33,2: één cel)
# KEGELS op schild en kam (lichte kegels in de donkere kam; licht% per cel): K1 (28,20) 66, (28,21) 42 | K2 (31,20) 65,
# (30,21) 71, (31,21) 40, (30,22) 65, donkere flank (32,20) 10, (32,21) 0, (31,22) 0 | K3 (36,19) 41, (35,20) 71, (35,21) 31,
# donkere flank (36,20) 28, (36,21) 0 | lichte bovenrand van de rugplaat (30,18) 26, (31,18) 33 (model y17,25-18,0)
KEGELS={'K1':{(28,20):'c',(29,20):'a',(28,21):'c',(29,21):'b'},
        'K2':{(31,20):'c',(32,20):'a',(30,21):'c',(31,21):'c',(32,21):'a',(30,22):'c',(31,22):'a'},
        'K3':{(36,19):'c',(37,19):'a',(35,20):'c',(36,20):'a',(35,21):'c',(36,21):'a'},
        'plaat':{(30,18):'c',(31,18):'c'}}
# KOPSCHILD-vlakken: benoemde correcties op de klassenkaart, per cel gemeten (licht% in sprite_r11/NOTITIES.md)
KOPVLAK={(17,21):'d',(18,21):'d',                     # hooglicht: lichtste plek van de afschuining (licht 88 / 95 %)
         (32,23):'c',(33,23):'c',                     # lichte rand rechtsboven van het schild (59 / 63 %), loopt door in (34-35,24) en (35,25)
         (14,25):'b',                                 # onder de lichte onderrand (licht 0 %): middenvlak, geen losse lichte pixel
         (13,24):'b',(15,25):'c',(16,25):'c',         # lichte onderrand loopt diagonaal van de punt naar het gezicht (licht 30 / 45 / 87 %)
         (37,21):'L'}                                 # donkere kam naast K3 (licht 0 %)
def kop():
    q=R10.copy()
    for x,y in PUNT_WEG: q[y,x]=0
    KS=np.zeros((H,W),bool)
    for j,i in zip(*np.where(ZONE&(q>0)&~GZ)):
        k=klasse(j,i); KS[j,i]=vlak(j,i)==12
        q[j,i]=C[TINT[k]]
        if KS[j,i]: q[j,i]=C[{1:'L',2:'L',3:'L',4:'b',5:'c',6:'d'}[k]]   # kopschild: 3 vlakken + hooglicht
    sil=q>0
    for j,i in zip(*np.where(ZONE&sil&~GZ)):
        if any(not sil[j+dy,i+dx] for dy,dx in N4): q[j,i]=C['K']
    return q,KS
def kop_af():
    q,KS=kop()
    VAST=np.zeros((H,W),bool)
    for d in list(KOPSTEKELS.values())+list(KEGELS.values())+[KOPVLAK]:
        for (x,y),ch in d.items(): assert ZONE[y,x] and q[y,x]>0,(x,y); q[y,x]=C[ch]; VAST[y,x]=True
    # lichte afschuining langs de bovenrand van het kopschild: de pixel onder de omtrek
    for j,i in zip(*np.where(KS&~GZ&~VAST&(q!=C['K']))):
        if q[j-1,i] in (0,C['K']) and q[j,i]!=C['d']: q[j,i]=C['c']
    q=vlekjes(q,ZONE&~GZ,vast=VAST|GZ)               # tintvlekjes < 3 px weg; benoemde pixels (en wat eraan vastzit) blijven
    return q,KS,VAST
# ======================= 2. DEKSCHILD-GEBIED: silhouet, rugrand, rugdoorns =======================
# Model (rooster 30x, sprite_r11/NOTITIES.md): het schild loopt rechts door tot de buitenomtrek (smalle omgeslagen rand achter een
# naad); r10/r8 had daar een donkere 'rugrand' in lijftinten en een silhouet dat 1-2 px breder was dan het model. Nu:
# silhouet rechts = modelmasker (dekking >= 0,35), schildvlak = modelschild (vlak 35 + gesloten omtrek, >= 50 % van de cel).
_hull=ndimage.binary_fill_holes(ndimage.binary_closing(lab==35,iterations=8))
HULL=np.zeros((H,W))
for j in range(18,50):
    for i in range(30,62):
        ya,yb,xa,xb=cel(j,i,0); HULL[j,i]=_hull[ya:yb,xa:xb].mean()
OMTREK_S=(R10==C['s'])&(xx>=35)&~BEVROREN                  # r10: lichte-kant-omtrek van het schild in donkerbruin (selout) blijft
RZ=(xx>=44)&(yy>=19)&(yy<=45)&~ZONE&~BEVROREN&~OMTREK_S
# vanaf rij 29 is alles binnen het modelmasker rechts van het ovaal schild (omgeslagen rand); rij 23-28: donkere rug (model)
SH=(((HULL>=0.5)&(COV>=0.35)&(xx>=37)&(yy>=24)&(yy<=46))|SCHILD10|((COV>=0.35)&RZ&(yy>=29)))&~BEVROREN&~ZONE&~OMTREK_S
# rugdoorns, gemeten op het model (punt): RD1 (48,3 24,0) RD2 (51,3 29,2) RD3 (52,5 33,2) RD4 (54,5 37,0)
# opbouw Tyranitar: punt 1 px K, lichte flank linksboven c, donkere flank rechtsonder K, voet loopt over in de schildrand
RUGDOORNS={'RD1':{(48,24):'K',(47,25):'c',(48,25):'K'},
           'RD2':{(51,29):'K',(50,30):'c',(51,30):'K',(50,31):'c',(51,31):'K'},
           'RD3':{(52,33):'K',(51,34):'c',(52,34):'K'},
           'RD4':{(54,37):'K',(53,37):'c',(53,38):'K'}}
DOORN=np.zeros((H,W),bool)
for _d in RUGDOORNS.values():
    for (_x,_y) in _d: DOORN[_y,_x]=True
SH&=~DOORN
def gebied(q):
    q=q.copy()
    SIL=((COV>=0.35)&RZ)|(SH&RZ)
    for d in RUGDOORNS.values():
        for (x,y) in d: SIL[y,x]=True
    q[RZ]=0; q[SIL]=C['L']
    fig=q>0
    for y,x in zip(*np.where(SIL&~SH)):                     # rugrand boven het schild (model: donker, x44-48 y20-28)
        q[y,x]=C['K'] if any(not fig[y+dy,x+dx] for dy,dx in N4) else C['L']
    for d in RUGDOORNS.values():
        for (x,y),ch in d.items(): q[y,x]=C[ch]
    return q,SIL
# ======================= 3. DEKSCHILD =======================
def bol(q):
    """één bolle vorm (Heracross/Ledian): omtrek (K tegen de achtergrond, s tegen rugrand/lijf), lichte rand linksboven o,
    basis x, schaduwsikkel w, omgeslagen rand v langs de schaduwkant (model: smalle strook achter de naad); hooglicht d."""
    q=q.copy(); fig=q>0
    IN=SH|OMTREK_S|DOORN
    RAND=np.zeros((H,W),bool)
    for y,x in zip(*np.where(SH)):
        if any(not IN[y+dy,x+dx] for dy,dx in N4):
            RAND[y,x]=True; q[y,x]=C['K'] if any(not fig[y+dy,x+dx] for dy,dx in N4) else C['s']
    BIN=SH&~RAND
    def SCH(y,x,k):                                      # k stappen naar rechts/onder ligt de schaduwkant (rand, geen lichte omtrek)
        return any(not BIN[y+dy*k,x+dx*k] and not OMTREK_S[y+dy*k,x+dx*k] for dy,dx in ((0,1),(1,0),(1,1)))
    for y,x in zip(*np.where(BIN)):
        if SCH(y,x,1): t='v'                                # omgeslagen rand / diepe schaduw
        elif not BIN[y-1,x] or not BIN[y,x-1]: t='o'        # lichte rand langs boven/links
        elif SCH(y,x,2): t='w'                              # schaduwsikkel (1 px; 2 px maakte het schild te donker)
        else: t='x'
        q[y,x]=C[t]
    for x,y in HOOGLICHT: assert BIN[y,x]; q[y,x]=C['d']
    return q
HOOGLICHT=[(39,26),(40,26),(39,27)]                          # glans op de bolling linksboven (model: lichtste tan x38-41 y25-28)
# vlekken: ellipsen langs de schildas (model: strepen schuin naar rechtsonder, richting (0,43 0,90))
AS=np.array([0.43,0.90]); DW=np.array([0.90,-0.43])
def ellips(cx,cy,lang,breed):
    u=(xx+0.5-cx)*AS[0]+(yy+0.5-cy)*AS[1]; v=(xx+0.5-cx)*DW[0]+(yy+0.5-cy)*DW[1]
    return (u/lang)**2+(v/breed)**2<=1
VLEKKEN={ # A: de vijf hoofdvlekken van het model (streep links, streep midden, twee middenvlekken, grote vlek onderaan)
 'A':[(39.6,29.0,3.2,1.1),(43.2,28.6,3.2,1.1),(41.6,34.6,2.6,1.3),(45.6,34.4,2.4,1.1),(47.4,40.6,3.2,1.9)],
          # B: vier grotere ronde schorsvlekken (Beautifly/Shuckle: groot, weinig, met zoom en schaduw)
 'B':[(40.2,29.2,2.8,1.6),(44.8,30.6,2.4,1.3),(42.8,35.4,2.3,1.7),(46.9,40.6,3.0,2.0)]}
def vlek_tinten(q,var):
    """vlek = één stap donkerder dan zijn ondergrond (x -> v, w/v -> s); rechterrand van de vlek s (eigen schaduw);
    B: linkerrand w (zoom in middenbruin, zoals de modelvlekken en Beautifly). Lichte rand o en hooglicht blijven vrij."""
    q=q.copy(); base=q.copy(); M=np.zeros((H,W),bool)
    for e in VLEKKEN[var]: M|=ellips(*e)
    M&=np.isin(base,[C['x'],C['w'],C['v']])&SH
    for y,x in zip(*np.where(M)):
        q[y,x]=C['v'] if base[y,x]==C['x'] else C['s']
    for y,x in zip(*np.where(M)):
        if not M[y,x+1] and M[y,x-1]: q[y,x]=C['s']                                 # eigen schaduw rechts
        elif var=='B' and not M[y,x-1] and M[y,x+1] and base[y,x]==C['x']: q[y,x]=C['w']   # zoom links
    return q,M
def bouw(var):
    q,KS,VAST=kop_af()
    q,SIL=gebied(q)
    q=bol(q)
    q,M=vlek_tinten(q,var)
    binnen=SH&np.isin(q,[C['x'],C['w'],C['v'],C['s']])
    q=vlekjes(q,binnen)                                     # losse tintpixels in het schild (8-samenhangend < 3) opheffen
    return q,dict(KS=KS,VAST=VAST,SIL=SIL,M=M)
if __name__=='__main__':
    OUT={}
    for v in 'AB':
        q,info=bouw(v); OUT[v]=(q,info); opslaan(q,UIT+'/pinsir_evo_r11_%s.png'%v)
        im=Image.open(UIT+'/pinsir_evo_r11_%s.png'%v); assert im.info.get('transparency')==0 and (np.asarray(im)==q).all()
        d=int((q[BEVROREN]!=R10[BEVROREN]).sum()); g=int((q[GZ]!=R10[GZ]).sum())
        print('%s: kleuren %d | diff bevroren delen %d | diff gezicht %d'%(v,len(set(q.ravel())),d,g))
    if 'raster' in sys.argv:
        for v in 'AB':
            q=OUT[v][0]; print(v); print('    '+''.join(str(x%10) for x in range(8,60)))
            for Y in range(12,48): print('%2d  '%Y+''.join(CH[q[Y,X]] for X in range(8,60)))
# ======================= VEL =======================
if __name__=='__main__' and 'raster' not in sys.argv:
    sys.path.insert(0,'gereedschap')
    from PIL import ImageDraw
    from vel import rgbp, model_crop
    def ref(n,bg=(255,255,255)):
        d='../../../../graphics/pokemon/'+n+'/'
        a=np.asarray(Image.open(d+'anim_front.png'))[:64,:64]
        P=[tuple(map(int,l.split())) for l in open(d+'normal.pal').read().split('\n')[3:] if l.strip()][:16]
        o=np.zeros((64,64,3),'uint8'); o[:]=bg
        for k in range(1,16): o[a==k]=P[k]
        return Image.fromarray(o)
    def raster(im,z,x0,y0,al=0.22):
        g=np.asarray(im).astype(float)
        for x in range(0,g.shape[1],z): g[:,x]=g[:,x]*(1-al)+np.array([0,120,255])*al
        for y in range(0,g.shape[0],z): g[y,:]=g[y,:]*(1-al)+np.array([0,120,255])*al
        im=Image.fromarray(g.astype('uint8')); d=ImageDraw.Draw(im)
        for X in range(0,g.shape[1]//z,2): d.text((X*z+2,1),str(X+x0),fill=(255,0,255))
        for Y in range(0,g.shape[0]//z,2): d.text((1,Y*z+2),str(Y+y0),fill=(255,0,255))
        return im
    A_,B_=UIT+'/pinsir_evo_r11_A.png',UIT+'/pinsir_evo_r11_B.png'
    rows=[]
    # 1. hele sprite 6x: r11 A | r11 B | r10 | model
    z=6; box=(0,8,64,64); w,h=(box[2]-box[0])*z,(box[3]-box[1])*z
    r=Image.new('RGB',(4*(w+8),h+14),'white'); d=ImageDraw.Draw(r); d.text((2,1),'hele sprite 6x: r11 A | r11 B | r10 | model (zelfde maat)',fill=(0,0,0))
    for i,im in enumerate([rgbp(A_).crop(box).resize((w,h),Image.NEAREST),rgbp(B_).crop(box).resize((w,h),Image.NEAREST),
                           rgbp(R10P).crop(box).resize((w,h),Image.NEAREST),model_crop(*box,z)]): r.paste(im,(i*(w+8),14))
    rows.append(r)
    # 2. kop 16x: r11 | model
    z=16; box=(9,12,46,30); w,h=(box[2]-box[0])*z,(box[3]-box[1])*z
    r=Image.new('RGB',(2*(w+8),h+14),'white'); d=ImageDraw.Draw(r); d.text((2,1),'kop 16x: r11 (A en B gelijk) | model met spriteraster',fill=(0,0,0))
    r.paste(raster(rgbp(A_).crop(box).resize((w,h),Image.NEAREST),z,box[0],box[1]),(0,14)); r.paste(raster(model_crop(*box,z),z,box[0],box[1]),(w+8,14))
    rows.append(r)
    # 3. dekschilden 12x: A | B | r10 | model ; referenties 6x
    z=12; box=(34,21,57,48); w,h=(box[2]-box[0])*z,(box[3]-box[1])*z
    r=Image.new('RGB',(4*(w+8),h+14),'white'); d=ImageDraw.Draw(r); d.text((2,1),'dekschild 12x: r11 A (modelstrepen, 5 vlekken) | r11 B (4 grote vlekken met zoom) | r10 | model',fill=(0,0,0))
    for i,im in enumerate([rgbp(A_).crop(box).resize((w,h),Image.NEAREST),rgbp(B_).crop(box).resize((w,h),Image.NEAREST),
                           rgbp(R10P).crop(box).resize((w,h),Image.NEAREST),model_crop(*box,z)]): r.paste(raster(im,z,box[0],box[1]) if i<3 else im,(i*(w+8),14))
    rows.append(r)
    REFS=[('beautifly',(28,12,62,42)),('shuckle',(8,28,42,58)),('heracross',(16,20,50,52)),('pinsir/mega',(40,8,64,36)),('ledian',(6,14,40,44))]
    zz=6; r=Image.new('RGB',(sum((b_[2]-b_[0])*zz+8 for _,b_ in REFS),36*zz+14),'white'); d=ImageDraw.Draw(r)
    d.text((2,1),'gebruikte referenties 6x: Beautifly (grote vlekken met zoom) | Shuckle (vlek volgt de bolling) | Heracross (schaduwkant) | Mega Pinsir (weinig grote vlakken) | Ledian (lichte rand)',fill=(0,0,0)); x=0
    for n,b_ in REFS:
        im=ref(n).crop(b_); im=im.resize((im.width*zz,im.height*zz),Image.NEAREST); r.paste(im,(x,14)); x+=im.width+8
    rows.append(r)
    # 4. 1x en 2x naast Gen 3 op wit en donker
    G3=['pinsir','heracross','tyranitar','aggron']
    r=Image.new('RGB',(2*(6*68+6*132)+40,2*140+16),'white'); d=ImageDraw.Draw(r); d.text((2,1),'1x en 2x op wit en donker: r11 A, r11 B, Pinsir, Heracross, Tyranitar, Aggron',fill=(0,0,0))
    for k,bg in enumerate(((255,255,255),(40,48,56))):
        y=16+k*140; x=0
        ims=[rgbp(A_,bg),rgbp(B_,bg)]+[ref(n,bg) for n in G3]
        bgim=Image.new('RGB',(r.width,136),bg); r.paste(bgim,(0,y))
        for im in ims: r.paste(im,(x,y+36)); x+=68
        x+=20
        for im in ims: r.paste(im.resize((128,128),Image.NEAREST),(x,y+4)); x+=132
    rows.append(r)
    Wv=max(x.width for x in rows); Hv=sum(x.height+10 for x in rows)
    v=Image.new('RGB',(Wv,Hv),'white'); y=0
    for x in rows: v.paste(x,(0,y)); y+=x.height+10
    v.save(UIT+'/vel.png'); print('vel',v.size)
