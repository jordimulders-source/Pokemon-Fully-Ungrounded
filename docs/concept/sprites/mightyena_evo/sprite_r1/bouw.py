# Mightyena-evolutie r1: MODEL OVERNEMEN. Natief raster 99x99 (pitch 10,24), figuur 74x70 -> 64x61 door 10 kolommen en 9 rijen te
# schrappen (GEMINI.md, Gengas 74->64: elke pixel blijft een modelpixel; gezicht en klauwen nooit geschrapt). Daarna alleen palet,
# technische opschoning en benoemde reparaties; elke stap geteld. Bouwen: cd mightyena_evo && python3 sprite_r1/bouw.py [kaal]
import sys, numpy as np
sys.path.insert(0,'gereedschap'); from gemeen import *; from schrap import schrap
UIT='sprite_r1'
a,c,L=klassen()
# helderheid per natieve pixel mee schrappen (om D in twee tonen te splitsen)
s,rows,cols,_,_=schrap(c)
Ls=np.delete(np.delete(L,rows,0),cols,1)
o=np.zeros((64,64),int); H,W=s.shape
# klasse -> spritepalet: K zwart | N vacht donker | D vacht midden (<70) / vacht licht (>=70) | M grijs schaduw | G grijs midden
#                        | geel, rood | bek donker, bek midden, tand wit
m={1:1,2:2,4:5,5:6,6:9,7:10,8:11,9:12,10:13}
blok=np.zeros((H,W),int)
for k,v in m.items(): blok[s==k]=v
blok[(s==3)&(Ls<70)]=3; blok[(s==3)&(Ls>=70)]=4
o[Y0:Y0+H,X0:X0+W]=blok
kaal=o.copy(); opslaan(kaal,UIT+'/kaal.png')
if len(sys.argv)>1 and sys.argv[1]=='kaal':
    toon(o); sys.exit()

tel={}
def stap(n,v,o): tel[n]=tel.get(n,0)+int((v!=o).sum())
N4=((-1,0),(1,0),(0,-1),(0,1))
def fg(o): return o>0
# --- 1. buitenlijn: elke randpixel (achtergrond als 4-buur) wordt lijn. Vacht: zwart rondom (zoals Mightyena's zwarte vacht).
#        Grijs/bek: schaduwkant (achtergrond rechts of onder) zwart, lichtkant (alleen links/boven) gekleurde selout (4). ---
def rand(o,vacht=None):
    f=o>0; uit=[]
    for Y,X in zip(*np.where(f)):
        k=o[Y,X]
        if k==1: continue
        bg=[not f[Y+dy,X+dx] if 0<=Y+dy<64 and 0<=X+dx<64 else True for dy,dx in N4]   # boven, onder, links, rechts
        if not any(bg): continue
        isv=(k in VACHT) if vacht is None else (vacht[Y,X] or k in (2,3))
        if isv or bg[1] or bg[3]: n=1
        else: n=4
        if n!=k: uit.append((Y,X,n))
    for Y,X,k in uit: o[Y,X]=k
v=o.copy(); rand(o); stap('buitenlijn',v,o)
# --- materiaal: grote samenhangende donkere massa = zwarte vacht (manen, opgeheven poot, poten, staart);
#     kleine donkere clusters in het grijs = vlekken/tekening (uit het model) ---
dk=np.isin(o,(1,2,3,4)); lab,n=label(dk,acht=False)
VMASK=np.zeros((64,64),bool)
for i in range(1,n+1):
    if (lab==i).sum()>40: VMASK|=lab==i
VMASK&=np.isin(o,(2,3,4))
KOP=np.zeros((64,64),bool); KOP[:31,:23]=True        # kop: tekening (wenkbrauw, ooglijnen, bek) blijft zoals het model
def meerderheid(o,Y,X,toegestaan):
    nb=[o[Y+dy,X+dx] for dy,dx in N4 if o[Y+dy,X+dx] in toegestaan]
    return max(set(nb),key=nb.count) if nb else None
# --- 2. ontkorrelen vacht: losse 1-px tintjes (3/4) zonder gelijke 8-buur in de vacht nemen de buurtint aan; strengen (≥2 px) blijven ---
v=o.copy()
for k in (3,4):
    lab,n=label((o==k)&VMASK,acht=True)
    for i in range(1,n+1):
        mm=lab==i
        if mm.sum()>=2: continue
        Y,X=np.argwhere(mm)[0]; t=meerderheid(o,Y,X,{2,3,4}-{k})
        if t: o[Y,X]=t
stap('ontkorrelen vacht',v,o)
# --- 3. donkergrijze modelpixels (D) in het grijs: grenzen ze aan een vlek -> vlek (2), anders grijze schaduw (5) ---
v=o.copy()
GR=~VMASK&~KOP&(o>0)
for Y,X in zip(*np.where(GR&np.isin(o,(3,4)))):
    if any(o[Y+dy,X+dx]==2 for dy in (-1,0,1) for dx in (-1,0,1)): o[Y,X]=2
    else: o[Y,X]=5
stap('grijs: D naar vlek/schaduw',v,o)
# --- 4. ontkorrelen grijs: tintvlekjes < 3 px (5/6) nemen de buurtint aan ---
v=o.copy()
for _ in range(2):
    for k in (5,6):
        lab,n=label((o==k)&~KOP,acht=False)
        for i in range(1,n+1):
            mm=lab==i
            if mm.sum()>=3: continue
            for Y,X in np.argwhere(mm):
                t=meerderheid(o,Y,X,{5,6}-{k})
                if t: o[Y,X]=t
stap('ontkorrelen grijs',v,o)

# --- 5. bek: vorm, binnenkant en tong = model; alleen de tandjes (die bij verkleinen wegvallen) worden witte hoektanden van 1x2 px
#        zoals de Gen 3-Mightyena frame 2 (toegestane afwijking, Jordi "ga maar los"). Tandpixels van het model die geen hoektand
#        worden, krijgen de binnenkant van de bek (donker 11 / tong 12), zodat de bekopening de modelvorm houdt. ---
v=o.copy()
TAND=13; BD=11; TONG=12
for X,Y,k in [
    (3,22,TAND),(3,23,TAND),            # hoektand boven voor (model: voortanden x2-3)
    (7,22,TAND),(7,23,TAND),            # hoektand boven achter (model: tand x7, bleef al 1x2)
    (5,26,TAND),(5,27,TAND),            # hoektand onder voor (model: tand x4-5, bleef al 1x2)
    (10,25,TAND),(10,26,TAND),          # hoektand onder achter (model: tanden x10-11 y25-26)
    (2,22,3),(4,22,3),(5,22,3),(6,22,3),# bovenlip tussen/naast de hoektanden: snuittint (model: witte tandjesrij, valt weg)
    (4,23,BD),(5,23,BD),(5,25,BD),      # donkere bek achter/boven de voorste hoektanden
    (4,24,1),                           # onderlipje voor
    (8,22,BD),(8,23,TONG),(9,21,BD),(10,21,BD),(10,23,BD),(12,23,BD),(11,24,BD),  # overige modeltandjes -> bekbinnenkant
    (9,26,TONG),(6,27,BD),(7,27,BD),    # ondertandjes -> bekbinnenkant
    ]:
    o[Y,X]=k
stap('bek: hoektanden',v,o)
o[28,12]=2; tel['bek: los wit pixeltje onder de kaak (12,28) -> vacht']=1   # model: los wit pixeltje onder de kaak; op 1x een losse witte stip

# --- 6. kop ontkorrelen: grijze tintvlekjes < 3 px op de kop (model: korrelige vachttextuur) nemen de buurtint aan;
#        oog, wenkbrauw/ooglijnen (zwart), bek en snuit (vacht) blijven ---
v=o.copy()
KG=KOP&~VMASK
for _ in range(2):
    for k in (3,4,5,6):
        lab,n=label((o==k)&KG,acht=(k in (3,4)))
        for i in range(1,n+1):
            mm=lab==i
            if mm.sum()>=(2 if k in (3,4) else 3): continue
            for Y,X in np.argwhere(mm):
                if any(o[Y+dy,X+dx]==0 for dy,dx in N4): continue      # randpixel = lijn
                t=meerderheid(o,Y,X,{5,6}-{k})
                if t: o[Y,X]=t
stap('kop ontkorrelen',v,o)

# --- 7. lichtkant zonder zwart/selout om en om: zwarte randpixels van een grijs deel met de achtergrond alleen links/boven -> selout 4 ---
v=o.copy()
f=o>0
for _ in range(3):
  for Y,X in zip(*np.where(o==1)):
    if 14<=Y<=28 and X<=14: continue     # gezicht: ooglijn, snuit en bek blijven zoals het model
    b=[not f[Y+dy,X+dx] if 0<=Y+dy<64 and 0<=X+dx<64 else True for dy,dx in N4]
    if not any(b) or b[1] or b[3]: continue
    nb=[(o[Y+dy,X+dx],VMASK[Y+dy,X+dx]) for dy,dx in N4 if 0<=Y+dy<64 and 0<=X+dx<64]
    if any(q in GRIJS or (q==4 and not vm) for q,vm in nb) and not any(vm for q,vm in nb): o[Y,X]=4
stap('lichtkant selout',v,o)

# --- 8. volume (kleur, geen vorm; Gen 3): het model is op het lijf één vlak lichtgrijs. Licht linksboven per lijfdeel: de modellijnen
#        (zwart) scheiden schouder, borst, dij en poten; per deel een geblurd masker -> normaal -> Lambert met licht van linksboven.
#        Lichtkant van elke bolling -> hooglicht 7, schaduwkant -> 5 (sikkel). Alleen op 6 (en 5 -> nooit lichter dan het model maakt
#        hem: 5 blijft 5). Vlekken en lijnen blijven. ---
def gaussian_filter(m,sg):
    r=int(3*sg); k=np.exp(-np.arange(-r,r+1)**2/(2*sg*sg)); k/=k.sum()
    p=np.pad(m,r); p=np.apply_along_axis(lambda q:np.convolve(q,k,'same'),0,p); p=np.apply_along_axis(lambda q:np.convolve(q,k,'same'),1,p)
    return p[r:-r,r:-r]
v=o.copy()
LM=(~VMASK)&np.isin(o,(2,5,6,7))&(o>0)
LM[:13,:]=False                       # oren/voorhoofd: textuur van het model, geen extra hooglicht
bl=gaussian_filter(LM.astype(float),2.6); gy,gx=np.gradient(bl); sc=(gx+gy)/np.sqrt(2)
for Y,X in zip(*np.where(LM&(o==6))):
    if KOP[Y,X]: continue             # kop (gezicht): zoals het model
    if sc[Y,X]>0.04: o[Y,X]=7
    elif sc[Y,X]<-0.06: o[Y,X]=5
for _ in range(2):
    for k in (7,5,6):
        lab,n=label((o==k)&LM,acht=False)
        for i in range(1,n+1):
            mm=lab==i
            if mm.sum()>=3: continue
            for Y,X in np.argwhere(mm):
                t=meerderheid(o,Y,X,{5,6,7}-{k})
                if t: o[Y,X]=t
stap('volume (licht linksboven)',v,o)

# --- 9. manen: lichtkant van de modelstrengen (strengpixel 3 met donker of zwart links/boven) -> 4, zodat de zwarte vacht intern leest ---
v=o.copy()
for Y,X in zip(*np.where((o==3)&VMASK)):
    if Y<14 or X<22: continue
    if o[Y-1,X] in (1,2) or o[Y,X-1] in (1,2):
        if o[Y+1,X]==3 or o[Y,X+1]==3 or o[Y+1,X+1]==3: o[Y,X]=4
stap('manen: lichtkant strengen',v,o)
# --- 10. vlekken: 1-px vlekjes op het lijf die in het model 2-4 px waren (de rest viel weg bij het schrappen) krijgen hun tweede
#         pixel terug aan de kant waar het modelcluster lag (zwaartepunt), zodat ze geen ruis/dambord worden. ---
v=o.copy()
kr=[i for i in range(c.shape[0]) if i not in rows]; kk=[i for i in range(c.shape[1]) if i not in cols]
nl,_n=label(np.isin(c,(1,2)),acht=False)
lab,n=label((o==2)&~VMASK&~KOP,acht=False)
for i in range(1,n+1):
    mm=lab==i
    if mm.sum()!=1: continue
    Y,X=np.argwhere(mm)[0]; uu=kk[X-X0]; vv=kr[Y-Y0]
    if not nl[vv,uu] or (nl==nl[vv,uu]).sum()<2: continue
    cy,cx=np.argwhere(nl==nl[vv,uu]).mean(0); dy,dx=cy-vv,cx-uu
    cand=[(int(np.sign(dy)),0),(0,int(np.sign(dx)))] if abs(dy)>=abs(dx) else [(0,int(np.sign(dx))),(int(np.sign(dy)),0)]
    for ddy,ddx in cand:
        if (ddy or ddx) and o[Y+ddy,X+ddx] in (5,6,7): o[Y+ddy,X+ddx]=2; break
stap('vlekken: geschrapte vlekpixel terug',v,o)
# --- 11. losse zwarte pixels midden in een vlak (geen zwarte 8-buur, geen achtergrond), buiten oog en bek: vacht -> 2, grijs -> 5 ---
v=o.copy()
for Y,X in zip(*np.where(o==1)):
    if KOP[Y,X] and Y<=28: continue                    # gezicht: ooglijnen, neusgat, bekhoek blijven zoals het model
    P=np.pad(o,1); nb8=[P[Y+1+dy,X+1+dx] for dy in (-1,0,1) for dx in (-1,0,1) if (dy or dx)]
    if 0 in nb8 or 1 in nb8: continue
    o[Y,X]=2 if VMASK[Y,X] or sum(q in VACHT for q in nb8)>=4 else 5
stap('losse zwarte pixels',v,o)
# --- 12. buitenlijn opnieuw (latere stappen mochten geen lichte kleur op de rand laten) ---
v=o.copy(); rand(o,VMASK)
# losse seloutpixel tussen zwart op de rand (zou om en om geven) -> zwart
f=o>0; P=np.pad(f,1)
R={(X,Y) for Y,X in zip(*np.where(f)) if not all(P[Y+1+dy,X+1+dx] for dy,dx in N4)}
for X,Y in sorted(R):
    if o[Y,X]!=4: continue
    nb=[o[Y+dy,X+dx] for dx in (-1,0,1) for dy in (-1,0,1) if (dx or dy) and (X+dx,Y+dy) in R]
    if 1 in nb and 4 not in nb: o[Y,X]=1
stap('buitenlijn (controle)',v,o)
opslaan(o,UIT+'/mightyena_evo_r1.png')
print('afwijkingen van de kale reductie per stap:'); [print('  %-40s %d'%(k,v)) for k,v in tel.items()]
print('totaal anders dan kaal:',int((o!=kaal).sum()),'| silhouet-diff:',int(((o>0)!=(kaal>0)).sum()))
if len(sys.argv)>1 and sys.argv[1]=='toon': toon(o)
