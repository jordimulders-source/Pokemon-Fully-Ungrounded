# Gaucho-Lotad r1: kale reductie (half2t.py, fase OY=1 OX=1, exact 2x2 -> 43x41) + technische opschoning + Lotad-oog.
# Elke stap telt hoeveel pixels hij verandert t.o.v. de kale reductie.
import sys, numpy as np; from PIL import Image
from half2t import reduceer, plaats, LIJN
from gemeen import opslaan, PAL, NAAM
OY,OX=1,1
o,mat,oogb=reduceer(OY,OX); (o,mat,oogb),info=plaats(o,mat,oogb)
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
    opslaan(o,uit)
    ys,xs=np.where(o>0); print(uit,'maat',xs.max()-xs.min()+1,'x',ys.max()-ys.min()+1,'px',(o>0).sum(),'kleuren incl. transparant',len(set(o.ravel())))
    print('afwijkingen van de kale reductie per stap:',tel,'totaal verschil',int((o!=kaal).sum()))
