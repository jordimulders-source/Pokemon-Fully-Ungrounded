# Ronde 1: kale reductie met lijnoverdracht (zie NOTITIES). Gebruik vanuit sneeuwmonster_fase3: python3 sprite_r1/bouw.py
import sys, os, numpy as np; from PIL import Image
sys.path.insert(0,'gereedschap'); from gemeen import *; from gemeen import label; from klassen import klassen; from lijnen import lijnkaarten
a,c,L=klassen(); idx=spriteindex(); ok=idx>=0; I=idx[ok]; cu=up(c)[ok]; Lu=up(L)[ok]
n=np.bincount(I,minlength=4096).astype(float); n1=np.maximum(n,1)
lijncel=((cu==2)&(Lu<140))|((cu==8)&(Lu<105))|(cu==1)
def frac(m): return (np.bincount(I,m.astype(float),minlength=4096)/n1).reshape(64,64)
def meanL(m): s=np.bincount(I,Lu*m,minlength=4096); t=np.bincount(I,m.astype(float),minlength=4096); return (s/np.maximum(t,1)).reshape(64,64),(t/n1).reshape(64,64)
fg=frac(cu!=0)>=0.5
steen=frac(np.isin(cu,[5,6,7]))
Ls,ws=meanL((cu==2)&~lijncel); Lh,wh=meanL((cu==8)&~lijncel); Lw,ww=meanL(cu==3); Lst,_=meanL(cu==5)
wb=frac(cu==4); wk=frac(cu==1)
hd=frac((cu==3)&(Lu<90)); hm=frac((cu==3)&(Lu>=90)&(Lu<135)); hl=frac((cu==3)&(Lu>=135))
# vlaktint = meerderheid van de modeltonen (geen gemiddelde: harde tintgrenzen zoals het model, geen menglijn langs elke grens)
sn=(cu==2)&~lijncel
tS=frac(sn&(Lu<165)); tM=frac(sn&(Lu>=165)&(Lu<203)); tH=frac(sn&(Lu>=203)&(Lu<228)); tW=frac(sn&(Lu>=228))
hn=(cu==8)&~lijncel; tHa=frac(hn&(Lu<148)); tHb=frac(hn&(Lu>=148))
def sneeuwtint(Y,X): return 3+int(np.argmax([tS[Y,X],tM[Y,X],tH[Y,X],tW[Y,X]])) if ws[Y,X]>0 else 4
o=np.zeros((64,64),int)
for Y in range(64):
    for X in range(64):
        if not fg[Y,X]: continue
        if wb[Y,X]>=0.3: o[Y,X]=10; continue
        if ww[Y,X]>=0.3 and ww[Y,X]>=ws[Y,X]: o[Y,X]=7+int(np.argmax([hd[Y,X],hm[Y,X],hl[Y,X]])); continue
        if wh[Y,X]>=max(ws[Y,X],0.15): o[Y,X]=11 if tHa[Y,X]>=tHb[Y,X] else 12; continue
        o[Y,X]=sneeuwtint(Y,X)
kaal_vul=o.copy()
lk=lijnkaarten()
emmer=np.isin(o,[7,8,9,10])
# lijndikte uit de dekking: de modellijnen zijn 1 cel (0,4 px) en licht (L~124); een spritepixel met >=30 % lijndekking
# wordt lijntint, een dunnere aanraking de schaduwtint s. Zwarte binnenlijnen: >=30 % zwart = K, anders lijntint.
lf=frac(((cu==2)&(Lu<140))|((cu==8)&(Lu<105))); kf=frac((cu==1))
sl=(lk['sneeuw']>0)&~emmer
o[sl&(lf>=0.45)]=2; o[sl&(lf<0.45)&np.isin(o,[4,5,6])]=3
o[(lk['hand']>0)&np.isin(kaal_vul,[11,12])]=2
kl=(lk['K']>0)&~emmer
o[kl&(kf>=0.30)]=1; o[kl&(kf<0.30)]=2
# stenen: vorm = >=45% steenzone; facet grijs waar de donkere steen licht is; scheuren/rand uit de lijnoverdracht
# per steen (fase 2-methode): rand gloeit waar het model aan de rand gloeit, binnen de pixels met het hoogste
# gloedaandeel, zoveel als het modelaandeel; geel waar het model geel is; lichtste niet-gloeiende pixels = grijs facet.
gf=frac(np.isin(cu,[6,7])); yf=frac(cu==7); sf=frac(np.isin(cu,[1,5,6,7]))
st=(steen>=0.45)&fg
lab,nst=label(st)
info=[]
for i in range(1,nst+1):
    pts=list(zip(*np.where(lab==i)))
    rand=[p for p in pts if any(not (0<=p[0]+dy<64 and 0<=p[1]+dx<64) or lab[p[0]+dy,p[1]+dx]!=i for dy,dx in ((1,0),(-1,0),(0,1),(0,-1)))]
    binnen=[p for p in pts if p not in rand]
    share=sum(gf[p] for p in binnen)/max(1,sum(sf[p] for p in binnen))
    for p in pts: o[p]=13
    for p in rand: o[p]=14 if gf[p]>=0.50 else 1
    # scheuren: binnenpixels met >=40 % gloed (vormen in het model de naden tussen de brokken, zie NOTITIES)
    rang=[p for p in binnen if gf[p]>=0.40]; k=len(rang)
    for p in rang: o[p]=15 if (yf[p]>=0.20 and gf[p]>=0.55) else 14
    rest=[p for p in binnen if p not in rang]
    for p in rest:
        if Lst[p]>=50: o[p]=10      # grijs facet: de lichte bovenvlakken van de brokken (model L~70-80 tegen ~25)
    info.append((len(pts),len(rand),k,round(share,2)))
print('stenen',info)
kaal=o.copy(); e0=np.zeros_like(fg)
for dy,dx in ((1,0),(-1,0),(0,1),(0,-1)): e0|=~np.roll(np.roll(fg,dy,0),dx,1)
kaal[fg&e0&~np.isin(kaal,[14,15])]=1; opslaan(kaal,'sprite_r1/kaal.png')   # kale reductie (vlak + lijnoverdracht + stenen + buitenlijn)
# EMMER (beschermde zone X25-44, Y11-21): band 1 px per kolom op de rij met het grootste bandaandeel van het model
# (klasse band; X29 48/47 % -> 17 zoals X28; de band is 1,5-2 px dik en loopt van links 17 via 16 (X30-33, boven het
# lichte houten lipje) naar 17 en 18 rechts), hout = meerderheid van de drie modeltonen, duignaden op de gemeten pieken.
from naden import naad_kaart
nf,hf=naad_kaart()
BAND={27:17,28:17,29:17,30:16,31:16,32:16,33:16,34:17,35:17,36:17,37:17,38:18,39:18,40:18,41:18}
for Y in range(11,22):
    for X in range(25,45):
        if not fg[Y,X]: continue
        if o[Y,X]==10 and BAND.get(X)!=Y:
            if X in BAND and Y<BAND[X]: o[Y,X]=o[Y-1,X] if o[Y-1,X] in HOUT else 7   # boven de band = hout (houttint van de pixel erboven)
            else: o[Y,X]=7+int(np.argmax([hd[Y,X],hm[Y,X],hl[Y,X]])) if ww[Y,X]>=0.3 else kaal_vul[Y,X] if kaal_vul[Y,X]!=10 else 4
for X,Y0 in BAND.items():
    for Y in range(13,Y0):
        if o[Y,X] in SNEEUW: o[Y,X]=o[Y-1,X] if o[Y-1,X] in HOUT else 7
for X,Y in BAND.items():
    if fg[Y,X]: o[Y,X]=10
    # onder de band: donkere lijn + onderrand van de emmer; hout+zwart >=45 % = hout (zwart telt als donker hout, binnenlijn)
    for YY in (Y+1,Y+2):
        if fg[YY,X] and o[YY,X]!=1 and ww[YY,X]+wk[YY,X]>=0.45:
            o[YY,X]=7+int(np.argmax([hd[YY,X]+wk[YY,X],hm[YY,X],hl[YY,X]]))
NADEN=[30,33,36,39]   # pieken naden.py, >=3 px uit elkaar (fase 2-les "minder maar volledig")
for X in NADEN:
    for Y in range(13,BAND[X]):
        if o[Y,X] in (8,9): o[Y,X]=7
# GEZICHT (beschermde zone X24-39, Y20-29): lijnen alleen uit de gemeten modeldekking per spritepixel
# (dekking donker <80 en lijn 80-150, zie NOTITIES): donker >=15 % = K (pupillen, mondhoek), lijn >=40 % = lijntint,
# lijn 25-40 % = s; de rest de vlaktoon zonder lijnen. Geen lijntransfer hier (die gaf elke vachtstreng een pixel).
dk=frac(Lu<80); lj=frac((Lu>=80)&(Lu<150)); Lv,_=meanL(Lu>=150)
GZ=[(Y,X) for Y in range(20,30) for X in range(24,40)]
for Y,X in GZ:
    if o[Y,X] in (0,7,8,9,10,13,14,15) or kaal_vul[Y,X] not in SNEEUW: continue
    t=sneeuwtint(Y,X)
    if lj[Y,X]>=0.45: t=2
    elif lj[Y,X]>=0.25: t=3
    o[Y,X]=t
# ogen, neus, mond: per pixel op de gemeten modelplek (model -> sprite omgerekend, NOTITIES 'Gezicht')
GEZICHT={(26,23):2,(27,23):2,(28,23):2,            # linkerooglid (zwaar, model y214)
         (26,24):2,(27,24):6,(28,24):1,            # linkeroog: ooghoek, oogwit, pupil rechts (model kijkt naar rechts)
         (32,23):2,(33,23):2,(34,23):2,(35,23):2,  # rechterooglid
         (33,24):6,(34,24):1,(35,24):2,            # rechteroog: oogwit, pupil, ooghoek
         (30,25):1,                                # neus (donker stipje, model 688,236)
         (27,27):2,(28,27):2,(29,27):2,(30,27):2,(31,27):2,(32,27):2,(33,26):1}   # glimlach + donkere haak rechts omhoog
for (X,Y),t in GEZICHT.items(): o[Y,X]=t
# RUIS (Gen 3: geen tintvlakjes <3 px): alleen buiten gezicht/emmer/stenen. (a) vlaktint-vlekje <3 px (4-samenhangend)
# -> meest voorkomende vlaktint van de 4 buren; (b) lijnstukje (tinten l/s, 8-samenhangend) <3 px dat niet aan een andere
# lijn of de omlijning raakt -> vlaktint van de buren. Telling in NOTITIES.
from collections import Counter
beschermd=np.zeros((64,64),bool); beschermd[11:22,25:45]=True; beschermd[20:30,24:40]=True
beschermd|=np.isin(o,[13,14,15])|st
def burentint(Y,X,ok):
    c=Counter(o[Y+dy,X+dx] for dy,dx in ((1,0),(-1,0),(0,1),(0,-1)) if 0<=Y+dy<64 and 0<=X+dx<64 and o[Y+dy,X+dx] in ok)
    return c.most_common(1)[0][0] if c else None
VLAK={4,5,6,11,12}; ruis=[]
for it in range(2):
    for k in sorted(VLAK):
        lab,nl=label((o==k)&fg,acht=False)
        for i in range(1,nl+1):
            pts=list(zip(*np.where(lab==i)))
            if len(pts)<3 and not any(beschermd[p] for p in pts):
                for p in pts:
                    t=burentint(p[0],p[1],VLAK-{k})
                    if t: o[p]=t; ruis.append(('vlak',p))
    lab,nl=label(np.isin(o,[2,3])&fg,acht=True)
    for i in range(1,nl+1):
        pts=list(zip(*np.where(lab==i)))
        if len(pts)<3 and not any(beschermd[p] for p in pts):
            raakt=any(o[p[0]+dy,p[1]+dx]==1 for p in pts for dy in (-1,0,1) for dx in (-1,0,1))
            if raakt: continue
            for p in pts:
                t=burentint(p[0],p[1],VLAK)
                if t: o[p]=t; ruis.append(('lijn',p))
print('ruis opgeschoond',len(ruis),Counter(r[0] for r in ruis))
# buitenrand = omlijning
e=np.zeros_like(fg)
for dy,dx in ((1,0),(-1,0),(0,1),(0,-1)): e|=~np.roll(np.roll(fg,dy,0),dx,1)
rand=fg&e; o[rand&~np.isin(o,[14,15])]=1
# selout (zoals fase 2): buitenlijn aan de lichtkant (naar links of recht omhoog gericht) in de eigen donkere tint:
# sneeuw/hand -> lijntint, hout -> donker hout. Rechts en onder blijft zwart. Stenen houden hun rand.
selout=0
for Y,X in zip(*np.where(rand&(o==1))):
    dx=sum(ddx for ddy,ddx in ((1,0),(-1,0),(0,1),(0,-1)) if not (0<=Y+ddy<64 and 0<=X+ddx<64) or not fg[Y+ddy,X+ddx])
    dy=sum(ddy for ddy,ddx in ((1,0),(-1,0),(0,1),(0,-1)) if not (0<=Y+ddy<64 and 0<=X+ddx<64) or not fg[Y+ddy,X+ddx])
    if not (dx<0 or (dx==0 and dy<0)): continue
    binnen=[kaal_vul[Y+ddy,X+ddx] for ddy,ddx in ((1,0),(-1,0),(0,1),(0,-1)) if 0<=Y+ddy<64 and 0<=X+ddx<64 and fg[Y+ddy,X+ddx]]
    if st[Y,X] or any(st[Y+ddy,X+ddx] for ddy,ddx in ((1,0),(0,1)) if Y+ddy<64 and X+ddx<64): continue
    if any(b in HOUT|{10} for b in binnen): o[Y,X]=7; selout+=1
    elif any(b in SNEEUW|HAND for b in binnen): o[Y,X]=2; selout+=1
print('selout',selout)
opslaan(o,'sprite_r1/sauna_yeti_r1.png')
gl=np.isin(o,[14,15])&st; print('steen px',st.sum(),'gloed',gl.sum(),'%.0f%%'%(100*gl.sum()/max(1,st.sum())))
toon(o,10,62,0,64)
d=(o!=kaal)
zones={'emmer':(slice(11,22),slice(25,45)),'gezicht':(slice(20,30),slice(24,40))}
tel={}
for Y,X in zip(*np.where(d)):
    z='emmer' if 11<=Y<22 and 25<=X<45 and (kaal[Y,X] in HOUT|{10} or o[Y,X] in HOUT|{10}) else 'gezicht' if 20<=Y<30 and 24<=X<40 else 'omlijning (selout)' if (kaal[Y,X]==1 and o[Y,X] in (2,7)) else 'ruis/vacht'
    tel[z]=tel.get(z,0)+1
print('afwijkend van kaal per zone',tel,'totaal',d.sum())
if len(sys.argv)>1:
    from lijnen import lijnkaarten
    for (y0,y1,x0,x1) in ((16,29,12,26),(16,29,42,57),(33,51,10,47)):
        print('gloed% / lijnhits')
        for Y in range(y0,y1): print('%2d '%Y+' '.join(('%2d%s'%(min(99,gf[Y,X]*100),'*' if lk['gloed'][Y,X] else ' ')) if st[Y,X] else ' . ' for X in range(x0,x1)))
if len(sys.argv)>1 and sys.argv[1]=='emmer':
    for Y in range(15,20): print(Y,' '.join('%d:%02d/%02d/%02d/%02d'%(X,ww[Y,X]*99,wk[Y,X]*99,wb[Y,X]*99,ws[Y,X]*99) for X in range(26,43)))
