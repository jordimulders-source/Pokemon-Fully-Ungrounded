# Ronde 3 = r2 met drie benoemde reparaties van Claude (gezicht, stenen, vacht); de rest = r2.
# Gebruik vanuit sneeuwmonster_fase3: python3 sprite_r3/bouw.py
import sys, numpy as np; from PIL import Image; from collections import Counter
sys.path.insert(0,'gereedschap'); from gemeen import *; from gemeen import label; from klassen import klassen
o=np.asarray(Image.open('sprite_r2/sauna_yeti_r2.png')).astype(int).copy(); r2=o.copy(); log=[]
def zet(X,Y,t,why):
    if o[Y,X]!=t: log.append((int(X),int(Y),CH[o[Y,X]]+'>'+CH[t],why)); o[Y,X]=t
a,c,L=klassen(); r,g,b=a[...,0],a[...,1],a[...,2]
idx=spriteindex(); ok=idx>=0; I=idx[ok]; n=np.maximum(np.bincount(I,minlength=4096),1)
def frac(m): return (np.bincount(I,up(m)[ok].astype(float),minlength=4096)/n).reshape(64,64)
fg=o>0; N4=((1,0),(-1,0),(0,1),(0,-1))

# ---------- PALET: handen 1 tint + lijntint als donker; plek 12 = rood terug (fase 2) ----------
PAL3=list(PAL); PAL3[11]=(112,151,164)   # gemeten gemiddelde van de vlakke handcellen (model)
PAL3[12]=(216,72,32)                      # rood uit fase 2: buitenste gloedtint (rand)
for Y,X in zip(*np.where(o==12)): zet(X,Y,11,'P1')   # handlicht -> de ene handtint
CH3=CH[:12]+'r'+CH[13:]

# ---------- 1. GEZICHT: egaal vlak in de gemeten gezichtstint + schaduw rechts, daarop alleen ogen/leden/neus/mond ----------
face=(c==2)&(g-r>=20)&(L>=190)&(L<235)&(b-g<=16)          # gezichtscellen model (gem. 197,222,233)
schaduw=(c==2)&(g-r>=20)&(L>=150)&(L<200)&(b-g<=20)         # schaduwcellen in het gezicht (gem. 164,192,209)
ff=frac(face); sf=frac(schaduw)
GZ=np.zeros((64,64),bool)
for Y in range(22,32):
    xs=[X for X in range(23,40) if ff[Y,X]>=0.35]
    if xs: GZ[Y,min(xs):max(xs)+1]=True                     # per rij de gemeten spanwijdte, gaten dicht
for Y,X in zip(*np.where(GZ)):
    if o[Y,X] in (0,1,13,14,15) or o[Y,X] in HOUT: continue
    zet(X,Y,4 if (sf[Y,X]>=0.40 and X>=32) else 5,'G')     # vlak h, schaduw m alleen rechts (model)
OGEN={(26,23):2,(27,23):2,(28,23):2,(26,24):2,(27,24):6,(28,24):1,
      (32,23):2,(33,23):2,(34,23):2,(35,23):2,(33,24):6,(34,24):1,(35,24):2,
      (30,25):1,(27,27):2,(28,27):2,(29,27):2,(30,27):2,(31,27):2,(32,27):2,(33,26):1}   # = r1 (gemeten plekken)
for (X,Y),t in OGEN.items(): zet(X,Y,t,'G')
# losse schaduwpixels in het gezichtsvlak (<3 px) -> vlak
lab,nl=label((o==4)&GZ,acht=False)
for i in range(1,nl+1):
    pts=list(zip(*np.where(lab==i)))
    if len(pts)<3:
        for Y,X in pts: zet(X,Y,5,'G')

# ---------- 2. STENEN: 1 px rand (rood waar het model gloeit, anders zwart), 1 px naden oranje, geel 1-2 px ----------
gf=frac(np.isin(c,[6,7])); yf=frac(c==7); stf=frac(np.isin(c,[5,6,7]))
Lst=np.bincount(I,up(np.where(c==5,L,0))[ok],minlength=4096)/np.maximum(np.bincount(I,up(c==5)[ok].astype(float),minlength=4096),1)
Lst=Lst.reshape(64,64)
st=(stf>=0.45)&fg
labs,ns=label(st)
for i in range(1,ns+1):
    pts=[tuple(p) for p in zip(*np.where(labs==i))]; S=set(pts)
    rand={p for p in pts if any((p[0]+dy,p[1]+dx) not in S for dy,dx in N4)}
    d1={p for p in pts if p not in rand and any((p[0]+dy,p[1]+dx) in rand for dy,dx in N4)}
    diep={p for p in pts if p not in rand and p not in d1}
    naad={p for p in diep if gf[p]>=0.40}
    # een pixel naast de rand is naad als hij aan een diepe naad raakt (naad loopt door tot de rand), anders steen (geen band)
    naad|={p for p in d1 if gf[p]>=0.40 and any((p[0]+dy,p[1]+dx) in naad for dy,dx in N4)}
    for p in pts:
        Y,X=p
        if p in rand: t=12 if gf[p]>=0.40 else 1
        elif p in naad: t=14
        else: t=10 if Lst[p]>=50 else 13
        zet(X,Y,t,'S')
    heet=sorted([p for p in naad if yf[p]>=0.10],key=lambda p:-yf[p])[:2 if len(pts)>=50 else 1]
    for Y,X in heet: zet(X,Y,15,'S')
    # rand: rood mag niet als 2 px dikke band; rood rond een rood hoekje blijft 1 px (rand is per definitie 1 px)

# ---------- 3. VACHT kop/schouders/manen (X12-52, Y18-36, buiten gezicht/emmer/stenen): alleen doorlopende strengen ----------
zone=np.zeros((64,64),bool); zone[18:37,12:53]=True
GZ1=np.zeros((64,64),bool)
for dy,dx in N4: GZ1|=~np.roll(np.roll(fg,dy,0),dx,1)   # buitenlijn (selout) blijft
for (X,Y) in OGEN: GZ1[Y-1:Y+2,X-1:X+2]=True   # ogen/neus/mond + 1 px eromheen beschermd
vrij=zone&~GZ1&~st
vrijG=vrij.copy(); vrij&=~GZ&~np.isin(o,[0,1,7,8,9,10,12,13,14,15])
vrij[11:22,25:45]&=~np.isin(o[11:22,25:45],[7,8,9,10])
VLAK={4,5,6}
def burentint(Y,X):
    cc=Counter(o[Y+dy,X+dx] for dy,dx in N4 if o[Y+dy,X+dx] in VLAK)
    return cc.most_common(1)[0][0] if cc else 6
lab,nl=label(np.isin(o,[2,3])&vrij,acht=True)
for i in range(1,nl+1):
    pts=list(zip(*np.where(lab==i)))
    if len(pts)<4:                                          # streng van <4 px leest niet als lijn -> vlak
        for Y,X in pts: zet(X,Y,burentint(Y,X),'V')
for it in range(2):
    for k in VLAK:
        lab,nl=label((o==k)&vrijG,acht=False)
        for i in range(1,nl+1):
            pts=list(zip(*np.where(lab==i)))
            if len(pts)<3:
                for Y,X in pts:
                    cc=Counter(o[Y+dy,X+dx] for dy,dx in N4 if o[Y+dy,X+dx] in VLAK-{k})
                    if cc: zet(X,Y,cc.most_common(1)[0][0],'V')
zet(23,24,burentint(24,23) if o[24,23]==1 else o[24,23],'V')   # losse zwarte pixel bij de manenrand
if o[24,23]==1: zet(23,24,2,'V')

opslaan(o,'sprite_r3/sauna_yeti_r3.png',PAL3)
st2=np.isin(o,[12,13,14,15])|(st&(o==10))|(st&(o==1))
print('r2->r3',(o!=r2).sum(),'px',Counter(l[3] for l in log))
print('gloed (rood/oranje/geel) / steen:',np.isin(o,[12,14,15])[st].sum(),'/',st.sum(),Counter(CH3[v] for v in o[st]))
if len(sys.argv)>1: [print(l) for l in log]
