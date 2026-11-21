# Swablu (onweerswolk) r3: Jordi over r2: "hoofd is nog steeds blurry, evenals de belijning van de bovenste donkere wolk en de voelsprieten,
# maar je hoeft alleen nog maar kleur, belijning, schaduw te fixen". Basis = r2; silhouet bevroren (alpha-diff 0); alleen kleur/lijn/schaduw.
# Draaien vanuit swablu_regional/: python3 sprite_r3/bouw.py
import sys, numpy as np
from PIL import Image
sys.path.insert(0,'gereedschap'); from klassen import klassen
import gemeen as G
from gemeen import overlap
a,c,L=klassen()
G.PAL=[(152,208,160),(13,17,24),
     (68,78,96),(96,108,126),(126,138,156),(164,176,192),(210,216,228),   # 2 wolk diep, 3 donker, 4 midden, 5 licht, 6 wit
     (68,90,110),(106,130,152),(150,174,194),                            # 7 vogel donker, 8 midden, 9 licht
     (200,158,40),(248,214,64),(255,246,160),                            # 10 oker, 11 geel, (12 lichtgeel: niet meer gebruikt)
     (214,220,230),(250,251,253)]                                        # 13 snavelwit, 14 glans
G.CH='.K01234abcoyYwW'
o=np.asarray(Image.open('sprite_r2/swablu_r2.png')).astype(int); start=o.copy()
tel={}
def zet(lijst,naam):
    v=o.copy()
    for X,Y,k in lijst:
        assert start[Y,X]!=0,(X,Y,'silhouet')     # nooit buiten het silhouet
        o[Y,X]=k
    tel[naam]=tel.get(naam,0)+int((v!=o).sum())
N4=((-1,0),(1,0),(0,-1),(0,1))
# ===== KOP =====
# Kopomlijning: één doorlopende zwarte lijn (model: zwarte rand rond de kop). Kruin links (24,24) (25,24) waren vogel donker, (26,23) vogel donker,
# (30,24) vogel donker -> zwart; linksboven liep de lijn via twee wolkpixels (23,25) (24,25): (23,25) -> zwart (diagonaal (22,26)-(23,25)-(24,24)),
# (24,25) -> kop midden (model v2w8: rand van de wolkbol, 1 px om de lijn strak te houden).
zet([(24,24,1),(25,24,1),(26,23,1),(30,24,1),(23,25,1),(24,25,8)],'kop: omlijning boven')
# Links van snavel en kin: lijn wisselde zwart/midden/diep/zwart ((21,29) (21,30) midden, (20,30)-(20,32) diep) -> één zwarte lijn
# (21,27)-(21,31) en (20,32)-(20,35); (20,30) (20,31) worden weer wolk licht zoals de bol ernaast (model K1w9, K1v2w7 = bol).
zet([(21,29,1),(21,30,1),(20,32,1),(20,30,5),(20,31,5)],'kop: lijn links van snavel')
# Snavel strak: bovenrand (22-24,27) en hoek (25,27) zwart (model: zwarte rand om de snavel), rechterrand (26,28) zwart (wit raakte de kop zonder lijn).
zet([(22,27,1),(23,27,1),(24,27,1),(25,27,1),(26,28,1)],'kop: snavelrand')
# Losse zwarte pixel onder de snavel (23,33): model K2v8 = kin -> kop midden.
zet([(23,33,8)],'kop: los zwart onder snavel')
# Onderrand kop/onderwolk (rij 37): wisselde vogel donker/diep/midden/zwart -> één lijn wolk diep (model: donkergrijze rand 'B' tussen lijf en
# onderwolk = gekleurde selout); (31,36) (32,36) waren diep maar zijn lijf (model v6w4) -> vogel donker (sikkel onderaan).
# De twee V-inkepingen (model zwart) worden één pixel diep op hun modelplek: (28,38) en (33,38); (29,38) -> wolk midden (top onderwolk).
zet([(x,37,2) for x in range(23,34)]+[(31,36,7),(32,36,7),(28,38,2),(29,38,4),(33,38,2)],'kop: onderrand')
# Kop-schaduw: sikkel rechtsonder in vogel donker staat al (toonstemming r2); hooglicht linksboven (vogel licht) blijft.
# ===== BOVENSTE DONKERE WOLK (achter/rechts van de kop) en wolkranden =====
# Lijn kop/donkere wolk: knik (34,27)(35,27)(34,28) -> (35,27) wordt wolkvulling; lijn loopt (33,26)(34,27)(34,28)(35,29)(35,30)(36,31).
# Bovenrand donkere wolk (36-40,26): zwart/diep/zwart -> één zwarte lijn (model: zwart/donkergrijs '#2' boven de wolk). Vulling één tint wolk diep.
zet([(35,27,2)]+[(x,26,1) for x in range(36,41)],'donkere wolk: lijn')
# Lichte bollen die tegen de donkere wolk of het lijf liggen kregen geen rand (wit tegen diep/vogel): de randpixel van de bol -> wolk midden (selout van de lichte bollen, zoals het model 'D' daar heeft).
v=[]
for Y,X in zip(*np.where(np.isin(start,[5,6]))):
    nb=[o[Y+dy,X+dx] for dy,dx in N4]
    if any(n in (7,8,9) for n in nb) or (26<=Y<=32 and 35<=X<=41 and any(n==2 for n in nb)): v.append((X,Y,4))
zet(v,'lichte bol: rand tegen donkere wolk/lijf')
# Rand lichte bollen rechts / onderwolk: één zwarte lijn; (38,39) was diep tussen zwart -> zwart.
zet([(38,39,1)],'rand bollen/onderwolk rechts')
# Rand linker bol / onderwolk: diagonale lijn wolk diep (19,35)(18,35)(17,35)(16,36)(15,36) (model: donkergrijze band); (16,35) midden -> bol licht, (16,36) midden -> diep.
zet([(16,35,5),(16,36,2)],'rand bol/onderwolk links')
# ===== VOELSPRIETEN =====
# Stelen: één kleur (vogel midden) als 1 px diagonaal, zwarte omlijning aan de schaduwkant; pixels die er al waren (silhouet bevroren) aan de lichtkant van
# de rechter steel worden selout vogel donker.
zet([(25,18,8),(25,19,8),(26,20,8),(26,21,8),(27,22,8),(27,23,8)],'sprieten: linker steel')
zet([(33,18,8),(32,19,8),(31,20,8),(30,21,8),(29,22,8),(31,19,7),(30,20,7),(29,21,7),(32,20,1),(33,20,1),(31,21,1)],'sprieten: rechter steel')
# Vonken: geel + één schaduwtint. Per pixel stemmen de gele modelpixels: oker (model L<180, de okerrand) of geel; meerderheid wint. Geen lichtgeel meer.
v=[]
for Y,X in zip(*np.where(np.isin(start,[10,11,12]))):
    ok=ge=0
    for u,vv,w in overlap(X,Y):
        if c[vv,u]==4:
            if L[vv,u]<180: ok+=w
            else: ge+=w
    v.append((X,Y,10 if ok>ge else 11))
zet(v,'vonken: geel/oker')
G.opslaan(o,'sprite_r3/swablu_r3.png')
G.rgb(o,(255,255,255)).resize((512,512),Image.NEAREST).save('sprite_r3/swablu_r3_8x.png')
print('stappen',tel); print('anders dan r2: %d px'%(o!=start).sum(),'| alpha-diff met r2:',int(((o>0)!=(start>0)).sum()),'| kleuren excl. transp.',len(set(o.ravel()))-1)
if 'toon' in sys.argv: G.toon(o,15,48,10,52)
