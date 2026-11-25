# Gaucho-Lotad r1: kale reductie (half2t.py, fase OY=1 OX=1, exact 2x2 -> 43x41) + technische opschoning + Lotad-oog.
# Elke stap telt hoeveel pixels hij verandert t.o.v. de kale reductie.
import sys, numpy as np; from PIL import Image
from half2t import reduceer, plaats, LIJN
from gemeen import opslaan, PAL, NAAM
OY,OX=1,1
o,mat,oogb=reduceer(OY,OX)
# ---- r2-reparaties in reductiecoordinaten (spritepixel (j,i) = modelblok rijen 2j+1..2j+2, kolommen 2i+1..2i+2) ----
import half2t as H2
c_,t_=H2.c,H2.t; r2tel={}
def nat2spr(v,u): return (v-1)//2,(u-1)//2
# R3 onder de snavel: in fase OY=1 vallen mondlijn (modelrijen 70-71) en kinlijn (74-75) met de kop ertussen (72-73) over
#    elkaars blokken -> 2 px zwart. In de zone rij 34-37 / kolom 42-58 de blokken van fase OY=0 (rijen 2j..2j+1) nemen:
#    rij 35 = mondlijn, 36 = kop, 37 = kinlijn; elke pixel blijft een 2x2-modelblok.
o0,mat0,_=reduceer(0,OX); v_=o.copy()
for j in range(34,38):
    for i in range(42,59):
        if o0[j,i]>0 and o[j,i]>0: o[j,i]=o0[j,i]; mat[j,i]=mat0[j,i]
r2tel['R3 mond/kin (fase-0-blokken)']=int((o!=v_).sum())
# R4 hoedrand links: lijnpixels in de zone vervangen door de gemeten modellijnen (zwart of hoed-lijntoon, natief u76-104, v36-47),
#    elk naar zijn eigen spritepixel; tussenpixels die geen modellijn hebben krijgen de meest voorkomende hoedtoon uit de buren.
v_=o.copy(); zone=[(j,i) for j in range(18,24) for i in range(37,52)]
lijnnat=[(v,u) for v in range(36,48) for u in range(76,105) if c_[v,u]==1 or (c_[v,u]==2 and t_[v,u]==2)]
doel={nat2spr(v,u) for v,u in lijnnat}; DUN=False
# Waar lijn A (kroon -> linksonder) en lijn B (randlijn vanaf de linkerpunt) samenkomen, ligt B 2 px dik (rij 32 x13-16 boven
# rij 33 x15-24). Alleen de hoekpixel x15,y32 (reductie j21,i42) weg: B wordt een doorlopende trap 2-2-10, A eindigt op x16,y32.
doel.discard((21,42))
def ncomp(P):
    P=set(P); n=0
    while P:
        n+=1; st=[P.pop()]
        while st:
            y,x=st.pop()
            for dy in (-1,0,1):
                for dx in (-1,0,1):
                    q=(y+dy,x+dx)
                    if q in P: P.remove(q); st.append(q)
    return n
def samenhangend(P,_n=[None]): return ncomp(P)==ncomp(doel)
# 1 px dik (Dundragoon-boor): hoekpixel met een horizontale en een verticale lijnbuur weg zolang de lijn samenhangend blijft
for p in sorted(doel):
    y,x=p; h=[(y,x+d) for d in (-1,1) if (y,x+d) in doel]; vv=[(y+d,x) for d in (-1,1) if (y+d,x) in doel]
    if DUN and h and vv and samenhangend(doel-{p}): doel=doel-{p}
def rand(j,i): return any(not(0<=j+dy<o.shape[0] and 0<=i+dx<o.shape[1]) or o[j+dy,i+dx]==0 for dy,dx in ((-1,0),(1,0),(0,-1),(0,1)))
for j,i in zone:
    if o[j,i] in (1,2) and mat[j,i] in (1,2) and not rand(j,i) and (j,i) not in doel:
        nb=[o[j+dy,i+dx] for dy in (-1,0,1) for dx in (-1,0,1) if (dy or dx) and o[j+dy,i+dx] in (3,4,5)]
        if nb: o[j,i]=max(set(nb),key=nb.count)
for j,i in doel:
    if (j,i) in zone and o[j,i]>0 and not rand(j,i): o[j,i]=2; mat[j,i]=2
r2tel['R4 hoedrandlijn (modelpixels)']=int((o!=v_).sum())
# R2a kraag: scheidingslijnen tussen de bladpunten uit de lijnkaart van het model (lijnkaart.py: kraagpixel >= 22 donkerder dan
#    de mediaan van zijn 5x5-kraagomgeving, dun), alleen strepen van >= 3 samenhangende modelpixels (kortere = textuur);
#    elke modellijnpixel naar zijn eigen spritepixel als 1 px binnenlijn in de donkere kraagtint (6), alleen op kraagvlak, niet op de rand.
from lijnkaart import lijnkaart
_,lk=lijnkaart(); lab_,n_=H2.clusters(lk); gr_=np.bincount(lab_.ravel())
v_=o.copy()
for v,u in zip(*np.where(lk&(gr_[lab_]>=3))):
    j,i=nat2spr(v,u)
    if 0<=j<o.shape[0] and 0<=i<o.shape[1] and o[j,i] in (7,8,9) and not rand(j,i): o[j,i]=6
r2tel['R2a kraaglijnen (modelpixels)']=int((o!=v_).sum())
print('r2-reparaties:',r2tel)
(o,mat,oogb),info=plaats(o,mat,oogb)
KLEIN=len(sys.argv)>2 and sys.argv[2]=='klein'
if KLEIN:
    from schrap import schrap
    ys,xs=np.where(oogb); 
    (o,mat,oogb),wx,wy=schrap([o,mat,oogb],3,3,beschermd_x=range(xs.min()-1,xs.max()+2),beschermd_y=range(ys.min()-1,ys.max()+2))
    print('geschrapt kolommen (plek, verschil met buur):',wx,'rijen:',wy)
kaal=o.copy(); opslaan(kaal,'kaal_klein.png' if KLEIN else 'kaal.png')
tel={}
def stap(n,v): tel[n]=tel.get(n,0)+int((v!=o).sum())
N4=((-1,0),(1,0),(0,-1),(0,1)); N8=[(dy,dx) for dy in (-1,0,1) for dx in (-1,0,1) if dy or dx]
def g(y,x): return o[y,x] if 0<=y<64 and 0<=x<64 else 0
TERRA={2,3,4,5}; KRAAG={6,7,8,9}; SNAVEL={6,10,11}; POOT={6,3,4,5}
SEL={2:2,3:2,4:6,5:6,6:2}   # selout (lichte kant) per materiaal
# 1. buitenlijn: rand naar achtergrond rechts/onder = zwart; links/boven = selout (lijntoon van het materiaal). Zwart blijft.
v=o.copy(); nieuw=[]
def eigen_mat(y,x):
    if mat[y,x]>=2: return mat[y,x]
    ms=[mat[y+dy,x+dx] for dy,dx in N8 if 0<=y+dy<64 and 0<=x+dx<64 and mat[y+dy,x+dx]>=2]
    return max(set(ms),key=ms.count) if ms else 1
for y,x in zip(*np.where(o>0)):
    bgR=g(y,x+1)==0; bgD=g(y+1,x)==0; bgL=g(y,x-1)==0; bgU=g(y-1,x)==0
    if not(bgR or bgD or bgL or bgU): continue
    if bgR or bgD:
        if o[y,x]!=1: nieuw.append((y,x,1))
    else:   # alleen achtergrond boven/links: lichte kant -> selout, ook als het model daar zwart heeft (DC; zoals de maatstaf-sprites)
        nieuw.append((y,x,SEL.get(eigen_mat(y,x),1)))
for y,x,k in nieuw: o[y,x]=k
stap('buitenlijn',v)
# 2. binnenlijnen: zwart dat niet aan de achtergrond grenst. Tussen twee materialen (vorm over vorm: hoed/kop, kin, mond) blijft zwart;
#    binnen één materiaal (rand-/kroonlijn hoed, kraagpunten) -> lijntoon van dat materiaal (DC: binnenlijnen niet zwart).
v=o.copy(); nieuw=[]
for y,x in zip(*np.where(o==1)):
    if any(g(y+dy,x+dx)==0 for dy,dx in N8): continue
    ms={mat[y+dy,x+dx] for dy,dx in N8 if v[y+dy,x+dx]!=1 and mat[y+dy,x+dx]>=2}
    if len(ms)==1: nieuw.append((y,x,LIJN[ms.pop()]))
for y,x,k in nieuw: o[y,x]=k
stap('binnenlijnen',v)
# 3. ontkorrelen: tintvlekjes < 3 px (4-samenhangend; lijntonen 1/2/6 niet) -> meest voorkomende buurtint uit dezelfde groep
def label(m):
    lab=np.zeros(m.shape,int); n=0
    for y in range(64):
        for x in range(64):
            if m[y,x] and not lab[y,x]:
                n+=1; st=[(y,x)]
                while st:
                    a,b=st.pop()
                    if 0<=a<64 and 0<=b<64 and m[a,b] and not lab[a,b]: lab[a,b]=n; st+=[(a+dy,b+dx) for dy,dx in N4]
    return lab,n
GROEP={3:TERRA,4:TERRA,5:TERRA,7:KRAAG,8:KRAAG,9:KRAAG,10:SNAVEL,11:SNAVEL}
def ontkorrel():
    for k,grp in GROEP.items():
        lab,n=label(o==k)
        for i in range(1,n+1):
            m=lab==i
            if m.sum()>=3: continue
            if oogb[m].any(): continue
            buur=[o[y+dy,x+dx] for y,x in zip(*np.where(m)) for dy,dx in N4 if 0<=y+dy<64 and 0<=x+dx<64 and o[y+dy,x+dx] in grp and o[y+dy,x+dx] not in (k,1,2,6)]
            if buur: o[m]=max(set(buur),key=buur.count)
v=o.copy(); ontkorrel(); ontkorrel(); stap('ontkorrelen',v)
# 3b. losse tintpixel (geen gelijke 8-buur) -> meest voorkomende 8-buurtint uit dezelfde groep (geen lijntonen)
v=o.copy()
for y,x in zip(*np.where(np.isin(o,list(GROEP)))):
    if oogb[y,x]: continue
    k=o[y,x]; nb=[g(y+dy,x+dx) for dy,dx in N8]
    if k in nb: continue
    kand=[b for b in nb if b in GROEP[k] and b not in (1,2,6)]
    if kand: o[y,x]=max(set(kand),key=kand.count)
stap('losse tintpixels',v)
# 4. losse lijnpixels midden in een vlak (geen lijnbuur in 8 richtingen, geen achtergrond) -> meest voorkomende buurtint
v=o.copy()
for y,x in zip(*np.where(np.isin(o,[1,2,6]))):
    nb8=[g(y+dy,x+dx) for dy,dx in N8]
    if 0 in nb8: continue
    if not any(k in (1,2,6) for k in nb8):
        nb=[g(y+dy,x+dx) for dy,dx in N4]; o[y,x]=max(set(nb),key=nb.count)
stap('losse lijnpixels',v)
# 5. ogen: Lotad-oog 1-op-1 (graphics/pokemon/lotad/anim_front_gba.png). Nabij oog (x31-33,y40-42):
#    rij 40 lichtblauw x3, rij 41 wit-zwart-wit, rij 42 lichtblauw-wit-lichtblauw. Ver oog: wit (23,41) + lichtblauw (24,41).
#    Geplaatst op het midden van de oogvakken van het model (oogb), links = ver oog.
v=o.copy()
lab,n=label(oogb); cs=[]
for i in range(1,n+1):
    ys,xs=np.where(lab==i); cs.append((xs.mean(),ys.mean(),len(xs)))
cs.sort()
ver,nab=cs[0],cs[-1]
cx,cy=int(round(nab[0])),int(round(nab[1]))
OOG=[[13,13,13],[12,1,12],[13,12,13]]
for j in range(3):
    for i in range(3): o[cy-1+j,cx-1+i]=OOG[j][i]
fx,fy=int(round(ver[0])),int(round(ver[1]))
o[fy,fx]=12; o[fy,fx+1]=13
print('nabij oog midden',(cx,cy),'ver oog',(fx,fy))
stap('ogen (Lotad)',v)
if __name__=='__main__':
    uit=sys.argv[1] if len(sys.argv)>1 else 'lotad_gaucho.png'
    opslaan(o,uit); print("plaats (y0,x0,Y0,X0):",info)
    ys,xs=np.where(o>0); print(uit,'maat',xs.max()-xs.min()+1,'x',ys.max()-ys.min()+1,'px',(o>0).sum(),'kleuren incl. transparant',len(set(o.ravel())))
    print('afwijkingen van de kale reductie per stap:',tel,'totaal verschil',int((o!=kaal).sum()))
