# Pitahaya-draak fase 3, r5: benoemde reparaties van de keurder op r4 (basis ../sprite_r4/pitahaya3_r4[_zonder_tong].png).
# Elke wijziging met stapnaam -> <uit>_afwijkingen.txt. Gebruik: python3 maak_r5.py BASIS.png UIT.png [--buik]
import sys,numpy as np; sys.path.insert(0,'.'); sys.path.append('../sprite_r2')
from PIL import Image; from tekstraster import CH,zet_rijen,schrijf
B=Image.open(sys.argv[1]); o=np.asarray(B).astype(int).copy(); r4=o.copy(); pal=B.getpalette(); LOG=[]
def meld(naam,voor):
    d=list(zip(*np.where(o!=voor)))
    for y,x in d: LOG.append((naam,x,y,CH[voor[y,x]],CH[o[y,x]]))
    print('%-92s %3d px'%(naam,len(d)))
def stap(naam,x0,rijen):
    voor=o.copy(); zet_rijen(o,x0,rijen); meld(naam,voor)

# ---- 4. LIJF (eerst, zodat de handstappen erbovenop komen) --------------------------------------------------------------
# lijf5.py: g die niet op een lange modelrib ligt -> vulling; G/h modusfilter 3x3 (2x); ribben = skelet van de donkergroene
# modellijnen met >= 60 natieve px (r4: 25), alleen 8-samenhangende stukken >= 6 px (r4: 4); toonclusters < 3 px -> buren.
# Proef 25/4 vs 40/6 vs 60/6 op 1x/6x: 60/6 het rustigst, ribben van nek, borst, dij en staart blijven.
from lijf5 import lijf
U=np.zeros((64,64),bool); U[33:46,0:22]=True; U[33:50,27:41]=True   # verre arm en nabije arm/hand: eigen stappen
# Borst/schouder (x16-31, y26-40) met LMIN 60 (daar lagen de meeste korte stukjes), rest met LMIN 40 zodat dijrib x45 en de
# staartstrepen blijven (keurder: "Rib x45 y41-50 blijft").
voor=o.copy(); o40,_=lijf(o,U,LMIN=40,MINRIB=6); o60,_=lijf(o,U,LMIN=60,MINRIB=6)
o=o40.copy(); BORST=np.zeros((64,64),bool); BORST[26:41,16:32]=True; o[BORST]=o60[BORST]
meld('lijf: ribben alleen lange modellijnen (>=6 px), schaduwvlekken samengevoegd',voor)

# ---- 1. NABIJE ARM + HAND ---------------------------------------------------------------------------------------------
# meet.py (model per spritepixel, zwartfractie): elleboog-bovencontour zwart (29-31,35),(32-33,36); voorrand onderarm
# (32,37),(32,38),(31,39) zwart, daarna donkergroen (31,40)->(29,45); achterrand zwart (39,35-37),(38,38-39),(37,40),
# (36,41-42),(35,43-44); bovenarm tussen x34-38 alleen een zwakke lijn (D-'s' op (35,35)) -> donkergroen.
# Onderarm licht (H langs de voorrand, h, G als sikkel tegen de achterrand); lijf erachter rechts G.
# Hand: 3 klauwen hangend (keurder/model-lussen): x30 en x32 y45-47, x34 y45-46; donkergroen met lichte punt (h),
# tussenruimte G (lijf erachter), onderrand zwart op rij 48 (model D (29-31,48) zwart). Limoen (31-32,43),(31,44) weg.
stap('nabije arm: elleboog-/bovenarmcontour, lichte onderarm, voor- en achterrand',28,{
 34:'g',
 35:' ###    ggg#',
 36:'    ##gghhh#',
 37:'    #HhhhhG#G',
 38:'    #HhhhG#GG',
 39:'   #HhhhhG#GG',
 40:'   gHhhhG#GG',
 41:'  gHhhhG#GGG',
 42:'  gHhhhG#GG',
 43:' gHhhhG#GGG',
 44:' ghhhhG#GG',
})
stap('nabije hand: 3 hangende klauwen donkergroen met lichte punt',29,{
 45:'#gGgGg#GG',
 46:'#gGgGh#GG',
 47:'#hGhGG#GG',
 48:'####GG#',
})
# ---- 3. DIJVOORRAND ---------------------------------------------------------------------------------------------------
# model D: (40-41,40),(40,41),(39-40,42),(38-39,43),(38,44) donker, zwart (38,44-49) (zwartfractie 0,2-0,3).
stap('dijvoorrand doorgetrokken tot y40: donkergroen, zwart onderaan',38,{
 40:'  g',
 41:'  g',
 42:' g',
 43:' g',
 44:'g',
 45:'g',
})
# ---- 2. KEEL / ONDERKAAK ----------------------------------------------------------------------------------------------
# model: kaakonderrand 1 px zwart (12-16,30); kaakscharnier diagonaal (16,30),(17,29),(18,28); nekvoorrand (16,31),(17,32),
# (18,33) zwart (zwartfractie 0,3-0,4), daarachter donkergroene keelschaduw. Binnenste zwart -> g/G.
stap('keel: 1 px zwart aan de buitenrand, binnenste zwart naar donker-/middengroen',16,{
 29:'d g',
 31:' gG',
 32:' #gG',
 33:' #gg',
})
# ---- 5. VERRE HAND ----------------------------------------------------------------------------------------------------
# model A (10,44) G / D h-s, (12,44) G: klauwen niet limoen.
stap('verre hand: klauwen donkergroen/middentint',10,{44:'g G'})

# ---- 6. KOP: losse lichte pixels naar de meerderheid van hun buren -----------------------------------------------------
# licht = P,h,H,W,w met geen enkele gelijke 8-buur; oog (10,22-23), tanden, pitjes, hoornpunten (g) blijven.
voor=o.copy(); BEHOUD={(22,10),(23,10),(25,13)}
for y in range(13,30):
    for x in range(2,24):
        v=o[y,x]
        if v in (5,8,9,10,11) and (y,x) not in BEHOUD:
            nb=[o[y+dy,x+dx] for dy in (-1,0,1) for dx in (-1,0,1) if dy or dx]
            if v not in nb and 0 not in nb:
                k=[c for c in nb if c not in (0,1)]
                if k: o[y,x]=max(set(k),key=k.count)
meld('kop: losse lichte pixels naar buurmeerderheid',voor)
# 4-buren-controle (geen gelijke 4-buur): (2,25) P tussen zwart (model: roze snuitrand) -> p; (19,25) h tussen zwart en r
# (model: roze/rand, geen groen) -> d. Kolom 13 (y15-19) is d op de zwarte flaprand van het model: blijft.
stap('kop: losse lichte pixels (2,25) en (19,25)',2,{25:'p                d'})

# controle.py: losse G (48,43) uit de lijfstap -> h (buren h)
stap('opruimen: losse toonpixel (48,43)',48,{43:'h'})

# ---- BUIK (alleen met --buik, Jordi 17 nov) ----------------------------------------------------------------------------
if '--buik' in sys.argv:
    from buik import buik
    voor=o.copy(); o=buik(o); meld('buik in vruchtvleeskleuren (W/w) met losse zwarte pitjes (s)',voor)

n=(o!=r4).sum(); OUT=[a for a in sys.argv[1:] if not a.startswith('--')][1]
schrijf(o,pal,OUT); print(OUT,'totaal t.o.v. r4',n,'px')
with open(OUT[:-4]+'_afwijkingen.txt','w') as f:
    f.write('# %s: elke pixel die afwijkt van r4 (%s): stap | x | y | r4 -> r5 (tekens: %s)\n# totaal %d px\n'%(OUT,sys.argv[1],CH,n))
    for r in LOG: f.write('%s | %d | %d | %s -> %s\n'%r)
