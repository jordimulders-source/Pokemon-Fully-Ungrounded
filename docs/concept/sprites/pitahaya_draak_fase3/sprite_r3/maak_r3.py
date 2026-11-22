# Pitahaya-draak fase 3, r3: benoemde reparaties op r2 (pitahaya3_r2.png als basis). Elke wijziging staat als rij-tekst met
# meting (lumroze.py / klas.py / masker.py op het model) in de commentaarregel; log -> pitahaya3_r3_afwijkingen.txt.
# Gebruik: python3 maak_r3.py BASIS.png UIT.png [--zonder-tong]
import sys,numpy as np; from PIL import Image; from tekstraster import CH,zet_rijen,schrijf
B=Image.open(sys.argv[1]); o=np.asarray(B).astype(int).copy(); r2=o.copy(); pal=B.getpalette()
ZT='--zonder-tong' in sys.argv
STAPPEN=[]; LOG=[]
def meld(naam,voor):
    d=list(zip(*np.where(o!=voor)))
    for y,x in d: LOG.append((naam,x,y,CH[voor[y,x]],CH[o[y,x]]))
    print('%-100s %3d px'%(naam,len(d)))
def stap(naam,x0,rijen): STAPPEN.append((naam,x0,rijen))

# ---- 1. KOP --------------------------------------------------------------------------------------------------------
# Model-helderheid roze (lumroze.py): kroon 140-152 op (7-10,17-19), snuitrug 141-149 op (3-4,23-24), voorhoofd 109-131,
# vouw voorhoofd/snuit rij 22 x4-7 (30% donkerroze, klas.py D3), snuitonderkant 98-103, oog (10,22)(10,23) wit, pupil (9,23),
# wenkbrauw/ooglijn (9,22) 50% zwart, (8,23) 40% zwart, (11,22) 70% donkerroze.
stap('kop: kroonhooglicht kleiner (alleen >=140 linksboven), rest middenroze',0,{
 16:'         pp',
 17:'      p p',
 18:'      p  pp',
 19:'      pPp',
 20:'      pppp',
})
# Snuitrug-hooglicht doorgetrokken van de punt (2,25) tot (6,23) (model 126-149, lichtste roze van de snuit; kleur mag
# afwijken: 4 varianten op 1x/2x naast het verkleinde model vergeleken, deze las het best als snuit). Vouw in middenschaduw r
# met donkerroze d op (7,22) waar hij de ooghoek raakt (model 101, 30% donker), zodat hij geen doorlopende vizierlijn wordt.
stap('kop: vouw voorhoofd/snuit, snuitrug licht, snuitrand zwart, oog wit|pupil|wit onder zwarte wenkbrauw',0,{
 22:'   #rrrdp#Wd',
 23:'   #PPPrd#Wr',
 24:'  #PPpprrr',
 25:' #Pppdpr',
 26:'   pprr',
})
for naam,x0,rijen in STAPPEN:
    voor=o.copy(); zet_rijen(o,x0,rijen); meld(naam,voor)

# ---- 2. LIJF: samenhangende vlakken i.p.v. losse hooglichtvlekken -----------------------------------------------------
# Toonkaart = volume uit het modelsilhouet (volume.py: afstand tot rand/zwarte modellijn -> bolle hoogte -> n.l, licht
# linksboven-voor) + 0,5 x de gladde modelhelderheid (houdt de lichtere modelmassa's: bovenarm, dij, staartrug).
# Alleen de vulpixels (G/h/H) van de grote lijfmassa, zonder de verre arm (die blijft schaduw zoals in r2);
# lijnen (#), ribben (g), roze en bracteeen ongewijzigd. Daarna clusters < 3 px naar de buurmeerderheid.
from lijf import per_pixel,vul,clusters
V=per_pixel()
m=np.isin(o,[6,7,8,9]); lab=np.zeros_like(o); n=0
for y in range(64):
    for x in range(64):
        if m[y,x] and not lab[y,x]:
            n+=1; st=[(y,x)]; lab[y,x]=n
            while st:
                a_,b_=st.pop()
                for dy,dx in ((1,0),(-1,0),(0,1),(0,-1)):
                    c_,d_=a_+dy,b_+dx
                    if 0<=c_<64 and 0<=d_<64 and m[c_,d_] and not lab[c_,d_]: lab[c_,d_]=n; st.append((c_,d_))
groot=max(range(1,n+1),key=lambda i:(lab==i).sum())
LZ=(lab==groot)&np.isin(o,[7,8,9]); LZ[33:46,0:22]=False; LZ[43:49,28:37]=False   # verre arm; nabije hand apart (stap 4)
voor=o.copy(); o=vul(o,V,LZ,pct=(35,82)); o=clusters(o,LZ); meld('lijf: volume-toonkaart G/h/H (35/47/18 %), clusters < 3 px weg',voor)
# ---- 3. RUGSTEKELS -------------------------------------------------------------------------------------------------
# 6 punten op de modelplekken (stekels.py r2 + rasteruitsneden 30x): punt S1 (32,15.9) S2 (38.8,16.3) S3 (44.3,20.2)
# S4 (48.3,25) S5 (50.8,31.7) S6 (52.5,35). In het model is elke stekel een doorn: lichtgroene bovenkant (linksboven),
# zwart/donkergroene onderrand (rechtsonder), donkere punt. r2 had ze helemaal donkergroen (las als donkere rand op het roze).
# Nu: punt + onderrand g, bovenkant/kern h; posities en silhouet uit r2 (alleen (31,15) en (37,16) weg: model achtergrond,
# klas.py B8/B8, zodat elke punt 1 px scherp is).
stap('rugstekels: lichte bovenkant, donkere punt en onderrand (6 doorns)',26,{
 15:'     .g',
 16:'   hhg     .g',
 17:'    g     hhg',
 18:'          hg',
 20:'                hhg',
 21:'              hhgg',
 24:'                      g',
 25:'                  hhhg',
 26:'                   gg',
 30:'                     hh',
 31:'                      hgg',
 32:'                      g',
 34:'                       hhhg',
 35:'                         gg',
})
for naam,x0,rijen in STAPPEN[-1:]:
    voor=o.copy(); zet_rijen(o,x0,rijen); meld(naam,voor)

# ---- 5. BEK / TAND ---------------------------------------------------------------------------------------------------
# Tand 1 onder de snuit (3,28): BEIDE modellen hebben hem (model.png en model_zonder_tong.png, uitsnede x 80-240 y 370-520
# op 3x: grijze tand op model x 97-113, y 413-430 in beide) -> in beide versies laten staan.
# Met tong: (9,29) is in het model vruchtvlees (klas.py W9), niet tong -> W. Zonder tong: onderste hoektand (6,30)
# (model_zonder_tong klas.py W7) wit, zoals (6,31).
if ZT: stap('bek zonder tong: onderste hoektand (6,30) wit',6,{30:'W'})
else: stap('bek met tong: (9,29) vruchtvlees i.p.v. tong',9,{29:'W'})
for naam,x0,rijen in STAPPEN[-1:]:
    voor=o.copy(); zet_rijen(o,x0,rijen); meld(naam,voor)

# ---- 4. NABIJE HAND -------------------------------------------------------------------------------------------------
# Model (lumgroen.py, x 28-36, y 42-49): handrug licht (rij 43: 128/109/123/124/120), vingers op x 31 (136/116) en x 34
# (117/100) met zwarte vingerlijnen ertussen (x 30 40%, x 32-33 30%), klauwpunten onderaan op (31,48) (104, 20% zwart) en
# (34,48) (108). r2 had rij 47 als H H g H g H H g H (gestreept). Nu: handrug als samenhangend vlak (licht linksboven),
# twee klauwen die versmallen naar 1 px (h H -> H -> H) met donker ertussen; punt A op de onderrand (model), punt B boven
# de zwarte onderrand (33-35,49).
stap('nabije hand: handrug als vlak, 2 klauwen als losse punten',28,{
 43:'GhhHHhhGG',
 44:'GhhHhhhGG',
 45:'GGhhhhhGG',
 46:'GGhHghHGG',
 47:'gg#H#gH#G',
 48:'g##H#gH#',
})
for naam,x0,rijen in STAPPEN[-1:]:
    voor=o.copy(); zet_rijen(o,x0,rijen); meld(naam,voor)

# ---- 6. OPRUIMEN (controle.py) ------------------------------------------------------------------------------------------
# dambord kroon (8-9,17-18): (9,18) P (model 145, hooglichtdrempel); losse H (20,46) na de lijfpass -> h (achterpoot, buren h/g).
stap('opruimen: dambord kroon, losse H',0,{18:'         P',46:'                    h'})
for naam,x0,rijen in STAPPEN[-1:]:
    voor=o.copy(); zet_rijen(o,x0,rijen); meld(naam,voor)

n=(o!=r2).sum(); schrijf(o,pal,sys.argv[2]); print(sys.argv[2],'totaal t.o.v. r2',n,'px')
with open(sys.argv[2][:-4]+'_afwijkingen.txt','w') as f:
    f.write('# %s: elke pixel die afwijkt van r2 (%s), per stap: stap | x | y | r2 -> r3 (tekens: %s)\n'%(sys.argv[2],sys.argv[1],CH))
    f.write('# totaal %d px (een pixel kan in twee stappen voorkomen; telt dan eenmaal)\n'%n)
    for r in LOG: f.write('%s | %d | %d | %s -> %s\n'%r)
