# Altaria (onweerswolk) r3: op het kop x1,5-dy10-model (model_kop/natief_kop15_dy10.png). Jordi: "let er bij altaria op dat het linkeroog ook
# zichtbaar moet zijn voor de sprite om mooi te worden, als dat niet past is het hoofd nog steeds te klein".
# Silhouet = r1-reductie op dat model (sprite_r3/basis.py -> basis_kop15.png), alpha nooit veranderd.
# Kleur: per spritepixel de MEEST VOORKOMENDE modeltoon in het 3x3-blok (modus i.p.v. gemiddelde: de bollen van het model blijven bollen:
# lichte kap, lijf, donkere onderboog), daarna alleen technisch opschonen. Keuring r2 (MOETEN 1-6) verwerkt, zie NOTITIES.md.
# Jordi: "iets minder detail is niet erg tov het model, zolang die niet blurry wordt" / "De belijning moet juist zachter en niet zwart" /
# "het ligt aan dat er meer dan 2 kleurtinten moeten zijn om minder blur te hebben".
import sys, numpy as np
sys.path.insert(0,'gereedschap'); sys.path.insert(0,'sprite_r3')
import gemeen as G; from gemeen import label
import basis as B; from basis import blok
from PIL import Image
UIT='sprite_r3'
# 0 transp | 1 pupil | wolk 2 selout L55, 3 donker L80, 4 midden L110, 5 licht L145, 6 hooglicht L191 |
# violet 7 selout L53, 8 donker L78, 9 midden L112, 10 licht L156 | 11 static (eigen cyaan) | 12 glans
PAL=[(152,208,160),(16,18,40),
     (34,62,96),(48,84,118),(70,114,148),(100,154,184),(150,206,224),
     (44,44,116),(66,68,160),(98,100,210),(144,146,236),
     (120,232,255),(240,244,255)]
G.PAL=PAL
WS,WD,WM,WL,WH=2,3,4,5,6; VS,VD,VM,VL=7,8,9,10; ST,GL,PU=11,12,1
VULW=[WD,WM,WL,WH]; VULV=[VD,VM,VL]
CH='.Ks0123vabcSW'
def toon(o,y0=4,y1=64,x0=0,x1=64):
    print('   '+''.join(str(x%10) for x in range(x0,x1)))
    for y in range(y0,y1): print('%2d '%y+''.join(CH[v] for v in o[y,x0:x1]))
a,c,L=B.a,B.c,B.L
bas=np.asarray(Image.open('sprite_r3/basis_kop15.png')).astype(int); fig=bas>0
KUIF=np.zeros((64,64),bool)
for Y,X in zip(*np.where(fig)): KUIF[Y,X]=B.kuif(X,Y) and bas[Y,X] in (1,6,7,8,9)
N4=((-1,0),(1,0),(0,-1),(0,1)); N8=[(dy,dx) for dy in (-1,0,1) for dx in (-1,0,1) if dy or dx]
def meest(l): return max(set(l),key=l.count)
tel={}
def stap(naam,v,o): tel[naam]=tel.get(naam,0)+int((v!=o).sum())
# --- modeltonen per natieve pixel (alleen indelen, niets getekend). Grenzen = dalen tussen de vier tonen van het model
#     (wolk: L44 / L72 / L122 / L186; violet: L64 / L107 / L140+lavendelwit). K = zwarte modellijn. ---
T=np.full(L.shape,-1); w=c==2; vi=(c==3)|(c==5)
T[w&(L<58)]=WD; T[w&(L>=58)&(L<100)]=WM; T[w&(L>=100)&(L<156)]=WL; T[w&(L>=156)]=WH
T[vi&(L<85)]=VD; T[vi&(L>=85)&(L<130)]=VM; T[vi&(L>=130)]=VL
T[c==1]=99
KMIN=2   # >=2 zwarte modelpixels in het blok = lijnkandidaat (alleen als hij doorloopt, zie stap 2)
# --- 1. modus per blok ---
o=np.zeros((64,64),int); K=np.zeros((64,64),bool)
for Y,X in zip(*np.where(fig)):
    u,v=blok(X,Y); b=T[v:v+3,u:u+3].ravel(); b=b[b>=0]
    nw=np.isin(b,VULW).sum(); nv=np.isin(b,VULV).sum()
    if (b==99).sum()>=KMIN or nw+nv==0: K[Y,X]=True
    grp=VULW if nw>=nv else VULV
    bb=[t for t in b if t in grp]+[(WD if grp is VULW else VD)]*int((b==99).sum())   # zwarte modellijn telt als donkerste vultint (onderboog)
    o[Y,X]=meest(bb) if bb else (WD if grp is VULW else VD)
kaal=o.copy()
# --- 2. naden: zwarte modellijnen (K) die als lijn doorlopen (8-samenhangend >= 3 px) worden selout van hun materiaal (geen zwart);
#        losse K-stippen verdwijnen in de modustint ---
lab,n=label(K,acht=True)
for i in range(1,n+1):
    m=lab==i
    if m.sum()<3: continue
    for Y,X in zip(*np.where(m)): o[Y,X]=WS if o[Y,X] in VULW else VS
stap('naden',kaal,o)
# --- 3. ontkorrelen: tintvlakjes < 4 px (hooglicht < 3) -> meest voorkomende buurtint van hetzelfde materiaal ---
def groep(k): return VULW if k in VULW else VULV if k in VULV else [k]
def ontkorrel(o):
    for k in VULW+VULV:
        lab,n=label(o==k,acht=False)
        for i in range(1,n+1):
            mm=lab==i
            if mm.sum()>=(3 if k==WH else 4): continue
            buur=[o[Y+dy,X+dx] for Y,X in zip(*np.where(mm)) for dy,dx in N4 if o[Y+dy,X+dx] in groep(k) and o[Y+dy,X+dx]!=k]
            if buur: o[mm]=meest(buur)
v=o.copy()
for _ in range(3): ontkorrel(o)
for _ in range(2):                      # uitsteeksels van 1 px (3 buren van een andere tint) gladstrijken
    for Y,X in zip(*np.where(np.isin(o,VULW+VULV))):
        k=o[Y,X]; nb=[o[Y+dy,X+dx] for dy,dx in N4]
        if nb.count(k)>1: continue
        for t in set(nb):
            if t!=k and t in groep(k) and nb.count(t)>=3: o[Y,X]=t; break
stap('ontkorrelen',v,o)
# --- 4. static: modelplekken (statisch() uit klassen.py, natief). Spritepixel = static als >= 2 static-modelpixels in het blok, plus blokken
#        met 1 die aan zo'n pixel grenzen (de lijn loopt door); 2x2-klontjes uitgedund (pixel met de minste modeldekking eruit);
#        stukjes < 4 px weg (Keuring MOET 6: weinig, langere zigzaglijnen, geen stukjes < 4 px). Eigen cyaan (11), niet de hooglichttint. ---
st=B.st; cnt=np.zeros((64,64),int)
for Y in range(64):
    for X in range(64):
        u,v=blok(X,Y)
        if 0<=u<st.shape[1]-2 and 0<=v<st.shape[0]-2: cnt[Y,X]=st[v:v+3,u:u+3].sum()
S=cnt>=2
S|=(cnt==1)&np.array([[any(cnt[Y+dy,X+dx]>=2 for dy,dx in N8) if 0<Y<63 and 0<X<63 else False for X in range(64)] for Y in range(64)])
for _ in range(2):
    for Y in range(63):
        for X in range(63):
            q=[(Y,X),(Y,X+1),(Y+1,X),(Y+1,X+1)]
            if all(S[p] for p in q): S[min(q,key=lambda p:cnt[p])]=False
lab,n=label(S,acht=True)
for i in range(1,n+1):
    if (lab==i).sum()<4: S[lab==i]=False
STAT=S.copy()
if __name__=='__main__':
    G.opslaan(o,UIT+'/tussen.png'); print(tel); toon(o)
    print('   '+''.join(str(x%10) for x in range(64)))
    for Y in range(14,62): print('%2d '%Y+''.join('S' if S[Y,X] else ('#' if fig[Y,X] else '.') for X in range(64)))
