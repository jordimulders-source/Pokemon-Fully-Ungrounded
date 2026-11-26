# Sneeuwmonster eindkeuring (schaduw + belijning + kleurtinten, Dragonfly Cave) op sprite_r10.
# Niets hertekend: alleen tinten van bestaande pixels (index) en paletwaarden. Silhouet, ogen, knopen en kuif: index-diff 0 (assert).
# Gebruik: cd sneeuwmonster && python3 eindkeuring/bouw.py
import sys, numpy as np
from PIL import Image, ImageDraw
sys.path.insert(0,'gereedschap'); import gemeen
from gemeen import X0,Y0,U0,V0,S,MODEL,label
U='eindkeuring/'
im=Image.open('sprite_r10/sneeuwmonster_r10.png'); base=np.asarray(im).astype(int)
p=im.getpalette(); PAL_OUD=[tuple(p[3*i:3*i+3]) for i in range(10)]
# 0 transp | 1 K | 2 l lijn (outline base) | 3 s schaduw | 4 m midden | 5 w licht | 6-8 steen | 9 outline highlight / donkerste schaduw
PAL=list(PAL_OUD)
PAL[2]=(62,96,140)    # stap K1: outline base donkerder (L118 -> L91): DC regel 4 "outlines must be reasonably dark"; modellijnen L~85; Absol 526262 L93, Dewgong 415283 L82
PAL[4]=(208,226,244)  # stap K2: middentint L230 -> L223, stap licht->midden 19 -> 26 (Absol ffffff/dedeee: 32)
PAL[9]=(128,164,198)  # stap K3: modelblauw L162 -> L157, tint gelijk getrokken met de sneeuwramp (hue 203 -> 209)
o=base.copy(); stappen={}
def zet(stap,lijst,nieuw,van=None):
    for X,Y in lijst:
        if van is not None: assert base[Y,X] in van,(stap,(X,Y),base[Y,X])
        o[Y,X]=nieuw; stappen.setdefault(stap,[]).append((X,Y))
# B1 dubbele lijn rechts op de kop (lijntint naast de zwarte outline shadow) -> schaduwtint: buitenlijn 1 px
zet('B1 kop rechts dubbele lijn weg',[(40,22),(40,28),(40,29)],3,{2})
# B2 nek links: zwarte binnenpixel (geen buitenrand) -> outline base; uiteinde van de nekplooi taps in tint 9
zet('B2 nekplooi links',[(23,31)],2,{1}); zet('B2 nekplooi links',[(24,31)],9,{2})
# B3 rechterflank: lijntint naast zwart (2 px dikke rand) -> tint 9: model heeft hier armlijn + dunne lichte strook (natief L 80-200), buitenlijn blijft 1 px zwart
zet('B3 rechterflank (arm buitenkant)',[(41,34),(42,35),(43,36),(43,37),(44,38),(44,39),(44,40),(44,41)],9,{2})
zet('B3 rechterflank (arm buitenkant)',[(43,35)],9,{3})      # los s-pixel tussen de lijn en zwart, sluit aan
zet('B3 rechterflank (arm buitenkant)',[(43,38)],3,{2})      # tweede lijnpixel op rij 38 -> schaduw (lijn 1 px)
# B4 rechterarm: lijn begint taps (model L222 op het beginpunt)
zet('B4 armlijn rechts taps',[(36,36)],9,{2})
# B5 linkerarm: klontje lijntint bovenop de arm (19,37) -> middentint (lijn 1 px, sluit aan op m eronder)
zet('B5 linkerarm klontje',[(19,37)],4,{2})
# B6 rechtervoet: bovenlijn loopt taps uit naar rechts (model L168-172); los lijnpixel naast zwart rechtsonder -> schaduw
zet('B6 voet rechts',[(38,48),(39,48)],9,{2}); zet('B6 voet rechts',[(41,47)],3,{2})
# B7 outline highlights (DC: "on the outlines in the very most highlighted parts ... on the inside"): kop linksboven
zet('B7 outline highlights kop',[(23,18),(22,19),(22,20)],9,{2})
# S1 schaduwsikkel onder de kop links: twee losse m-pixels (22,28),(24,29) -> sikkel volgens de modelhelderheid (model L 215 / 209)
zet('S1 sikkel onder de kop links',[(22,28)],3,{4}); zet('S1 sikkel onder de kop links',[(25,30)],4,{3})
# ---- bevroren zones: index-diff 0
fg0=base>0; fg1=o>0; assert (fg0==fg1).all(),'silhouet'
def kuif(X,Y): return Y<=17
def ogen(X,Y): return 21<=X<=26 and 21<=Y<=27 or 29<=X<=34 and 21<=Y<=28
def knopen(X,Y): return 23<=X<=29 and 33<=Y<=46
def jordizone(X,Y): return 21<=X<=28 and 47<=Y<=50
D=[(int(X),int(Y)) for Y,X in np.argwhere(o!=base)]
for f,n in ((kuif,'kuif'),(ogen,'ogen'),(knopen,'knopen'),(jordizone,'r10-zone linksonder')):
    d=[q for q in D if f(*q)]; assert not d,(n,d); print('diff %-20s 0 px (assert)'%n)
print('diff silhouet (alpha)    0 px (assert)')
# RGB-diff van steen en ogen: hun indices (1,5,6,7,8) houden dezelfde paletkleur
for k in (1,5,6,7,8): assert PAL[k]==PAL_OUD[k]
print('RGB ogen+knopen-stenen: K/w/d/p/g ongewijzigd (assert); l en m in kuif/rand van oog- en knoopvakken veranderen alleen via het palet')
for s,l in stappen.items(): print('%-34s %2d px %s'%(s,len(l),l))
print('totaal index-diff',len(D),'px')
def opslaan(o,path,pal=PAL):
    q=Image.fromarray(o.astype('uint8'),'P'); f=[v for c in pal for v in c]; q.putpalette(f+[0]*(768-len(f))); q.save(path,transparency=0)
opslaan(o,U+'sneeuwmonster_ek.png')
# voorstel (niet de hoofdversie): kuif is bevroren, maar heeft zwart/lijn om en om op de rand -> variant ter keuze voor Jordi
v=o.copy(); v[15,27]=2; v[12,30]=2; opslaan(v,U+'variant_kuif_zonder_om_en_om.png')
# ---- controles
P=np.array(PAL); Lm=P@[.299,.587,.114]
print('palet:'); [print('  %d %s L%d n=%d'%(k,PAL[k],Lm[k],(o==k).sum())) for k in range(10)]
for k in (2,3,4,5,9):
    lab,n=label(o==k,acht=True); kl=[tuple(int(t) for t in np.argwhere(lab==i)[0][::-1]) for i in range(1,n+1) if (lab==i).sum()<3]
    kl=[q for q in kl if not (kuif(*q) or ogen(*q) or knopen(*q) or jordizone(*q))]
    print('  vlekjes <3 px (8-buren) tint %d buiten bevroren zones: %s'%(k,kl))
rand=lambda X,Y: o[Y,X]>0 and any(o[Y+dy,X+dx]==0 for dy,dx in ((-1,0),(1,0),(0,-1),(0,1)))
dik=[(X,Y) for Y in range(64) for X in range(64) if o[Y,X]==2 and not rand(X,Y) and any(o[Y+dy,X+dx]==1 and rand(X+dx,Y+dy) for dy,dx in ((0,-1),(0,1),(-1,0),(1,0))) and not (kuif(X,Y) or ogen(X,Y) or knopen(X,Y) or jordizone(X,Y))]
print('  binnenlijnpixels l tegen de zwarte buitenlijn (eindpunten van binnenlijnen):',dik)
zw=[(X,Y) for Y in range(64) for X in range(64) if o[Y,X]==1 and not rand(X,Y) and not (ogen(X,Y) or knopen(X,Y))]
print('  zwart binnen de figuur buiten ogen/knopen:',zw)
# om-en-om: buitenlijnpixel waarvan beide buren op de rand (8-buren, ook buitenlijn) de andere lijnsoort hebben
om=[]
for Y in range(64):
    for X in range(64):
        if rand(X,Y) and o[Y,X] in (1,2):
            nb=[o[Y+dy,X+dx] for dy in (-1,0,1) for dx in (-1,0,1) if (dy or dx) and rand(X+dx,Y+dy) and o[Y+dy,X+dx] in (1,2)]
            if len(nb)>=2 and all(t!=o[Y,X] for t in nb): om.append((X,Y,'K' if o[Y,X]==1 else 'l'))
print('  enkel lijnpixel tussen de andere lijnsoort op de buitenrand:',om)
