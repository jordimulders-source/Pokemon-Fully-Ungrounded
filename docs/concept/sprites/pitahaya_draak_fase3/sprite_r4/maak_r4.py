# Pitahaya-draak fase 3, r4: benoemde reparaties op r3 (basis ../sprite_r3/pitahaya3_r3[_zonder_tong].png).
# Elke wijziging met stapnaam -> <uit>_afwijkingen.txt. Gebruik: python3 maak_r4.py BASIS.png UIT.png [--zonder-tong]
import sys,numpy as np; from PIL import Image; from tekstraster import CH,zet_rijen,schrijf
B=Image.open(sys.argv[1]); o=np.asarray(B).astype(int).copy(); r3=o.copy(); pal=B.getpalette()
ZT='--zonder-tong' in sys.argv; LOG=[]
def meld(naam,voor):
    d=list(zip(*np.where(o!=voor)))
    for y,x in d: LOG.append((naam,x,y,CH[voor[y,x]],CH[o[y,x]]))
    print('%-96s %3d px'%(naam,len(d)))
def stap(naam,x0,rijen):
    voor=o.copy(); zet_rijen(o,x0,rijen); meld(naam,voor)

# ---- 1. BEK -----------------------------------------------------------------------------------------------------------
# vlees.py (vruchtvlees-/zwart-/achtergrondfractie per spritepixel), beide modellen gelijk: vlees >= 0,6 op (9-11,26),
# (8-11,27), (8-11,28), (9-10,29) (zonder tong ook (8,29)); (8,26) 0,2 vlees/0,3 zwart. Dat is ±15 px, 4 rijen hoog = wat
# r3 al had (oppervlak klopt), maar r3 had het vlees grijs (w) en een zwarte bovenlipbalk (8-12,25) waar het model 0-20 %
# zwart heeft (de modellijn is ±1/4 px dik, op de rijgrens 25/26). Nu: bovenlip donkerroze d (dunne lijn), vlees helder W met
# grijs w alleen in de bovenhoeken (schaduw onder de lip), 2 pitjes op de modelplekken van r2/r3.
stap('bek: bovenlip dunne donkerroze lijn i.p.v. zwarte balk, vruchtvlees helder wit',8,{
 25:'ddddd',
 26:'WWWW',
 27:'WsWW',
 28:'WWWs',
})

# ---- 2. KOPSCHUBBEN: groen op de punten van de flappen -------------------------------------------------------------------
# Model (rasteruitsnede 30x, x 2-22, y 11-25; klas.py): drie hoorns aan de rand: boven (10,15)->(15,13), links (3,19)->(7,16),
# achter (16,20)->(19,15); elk een blad met lichte bovenkant/linkerkant en zwarte onderrand. Binnenin: voorhoofdsblad
# (10-12,19)+(12,18)+(11,20) en wangblad (16-18,21-23), ook met donkere onderrand. r3 had ze als h/g-vlekken.
# Nu: lichte kant h, donkere rand en punt g, punt 1 px scherp; (11,13) en (10,14) weg (masker.py: alleen sprite, model
# achtergrond); (15,16) en (16,16) roze (model L5 / D1R1, geen groen).
stap('kopschubben: hoorns en bladen als punten met lichte kant en donkere rand/punt',0,{
 13:'           .hhg',
 14:'          .hhg',
 15:'          h gd    hg.',
 16:'     hg        pphh#',
 17:'    hg           hg',
 18:'    hg     pg    hg',
 19:'   hg    phhg',
 20:'           g',
 21:'                hhg',
 22:'                 hg',
 23:'                 g',
})

# ---- 3. LIJF ---------------------------------------------------------------------------------------------------------
# Overwegend middengroen h; schaduw G = laagste 30 % van de volume-toonkaart (r3, licht linksboven); licht H alleen binnen
# 2 px van een boven-/linkerrand (nek, rug, staartbovenkant) en in de hoogste 20 %; ribben g = skelet van de lange
# donkergroene modellijnen (lum < 80, >= 25 natieve px; ribben.py; 4 instellingen vergeleken op 6x, deze het rustigst),
# op spriteniveau verdund tot 1 px, stukjes < 4 px weg; daarna toonclusters < 3 px naar de buurmeerderheid.
# Verre arm en nabije hand niet (eigen stappen r3); buitenrand en zwarte lijnen niet.
sys.argv=[sys.argv[0]]+sys.argv[1:]
from lijf import per_pixel; from ribben import ribkaart; from lijf4 import lijf
U=np.zeros((64,64),bool); U[33:46,0:22]=True; U[43:49,28:37]=True
voor=o.copy(); o,_=lijf(o,per_pixel(),ribkaart(25,80)[0],U,minrib=4); meld('lijf: middengroen, licht langs boven/links, ribben als 1 px lijnen uit het model',voor)

# ---- 4. OPRUIMEN: losse groentonen (controle.py) naar de meerderheid van hun groene buren (klauwpunten verre arm blijven)
voor=o.copy()
for _ in range(3):
  for y in range(1,63):
    for x in range(1,63):
        v=o[y,x]
        if v in (7,8,9) and (y,x) not in ((44,10),(44,12)):
            nb=[o[y+dy,x+dx] for dy,dx in ((1,0),(-1,0),(0,1),(0,-1),(1,1),(1,-1),(-1,1),(-1,-1))]
            if v not in nb:
                g=[k for k in nb if k in (7,8,9)]
                if g: o[y,x]=max(set(g),key=g.count)
                elif 6 in nb: o[y,x]=6
meld('opruimen: losse groentonen naar buurmeerderheid',voor)

n=(o!=r3).sum(); OUT=[a for a in sys.argv[1:] if not a.startswith('--')][1]
schrijf(o,pal,OUT); print(OUT,'totaal t.o.v. r3',n,'px')
with open(OUT[:-4]+'_afwijkingen.txt','w') as f:
    f.write('# %s: elke pixel die afwijkt van r3 (%s): stap | x | y | r3 -> r4 (tekens: %s)\n# totaal %d px\n'%(OUT,sys.argv[1],CH,n))
    for r in LOG: f.write('%s | %d | %d | %s -> %s\n'%r)
