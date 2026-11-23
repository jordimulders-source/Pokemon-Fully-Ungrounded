# r6.py: r6 = r5, met alleen de onderdelen die in vorm afwijken teruggezet naar het model.
# Bron = de verkleining van het model per spritepixel (meet6.npz: lijnaandeel + helderheid, gedeelde geometrie).
# Netjes maken = alleen tinten (3 per onderdeel uit de gemeten modelhelderheid), ruis en lijndikte. Niets getekend.
import numpy as np; from PIL import Image
from scipy import ndimage as nd
from meting_sprite import is_lijn, groep, GR
r5=Image.open('r5.png'); R5=np.asarray(r5).astype(int); S=R5>0
d=np.load('meet6.npz'); lf,hel=d['lf'],d['hel']; Z=np.load('../sprite/zone.npy')
TINT={'steen':(3,4,5),'licht':(12,13,14),'roze':(7,8,15),'blauw':(9,10,11)}
LIJN={'steen':2,'licht':4,'roze':6,'blauw':9}
rand=S&~nd.binary_erosion(S,structure=np.ones((3,3)))     # buitenrand: r5 houden (silhouet + omlijning bevroren)
# --- doelzones (koerswijziging Jordi): haar L/R, baard, riem, broek (dijen + voetballen), schouderballen rechts
DEEL={}
for k,n in ((2,'haar L'),(3,'haar R'),(4,'baard'),(10,'riem'),(12,'broek')): DEEL[n]=(Z==k)
sch=np.zeros_like(S); sch[19:29,38:49]=True; DEEL['schouder R']=sch&(Z==6)
DEEL['arm R']=(Z==8)
for n in DEEL: DEEL[n]=DEEL[n]&S&~rand
RIEM=[(112,3),(131,4),(999,5)]   # riem: lichte bovenkant (gemeten 133-151) / midden / onderkant (95-110)
O=R5.copy(); BRON={}   # BRON: per pixel 'L' lijn uit model, 'T' tint uit model, 'G' gesp-vervanging, 'R' ruis
for n,m in DEEL.items():
    ys,xs=np.where(m); vul=[]
    for y,x in zip(ys,xs):
        g=groep(y,x)
        if g is None: O[y,x]=1; BRON[y,x]='L'; continue
        if is_lijn(y,x): O[y,x]=LIJN[g] if lf[y,x]<0.8 else 1; BRON[y,x]='L'
        else: vul.append((y,x,g))
    for y,x,g in vul:   # vaste helderheidsgrenzen per materiaal (meting_sprite.GR): schaduw / midden / licht
        grens=RIEM if n=='riem' else GR[g][1]
        O[y,x]=next(i for t,i in grens if hel[y,x]<t); BRON[y,x]='T'
# --- omlijning van de teruggezette onderdelen: de ring van 1 px eromheen (in r5-onderdelen) krijgt lijn waar het model lijn heeft
DOEL0=np.zeros_like(S)
for m in DEEL.values(): DOEL0|=m
ring=nd.binary_dilation(DOEL0)&~DOEL0&S&~rand
for y,x in zip(*np.where(ring)):
    g=groep(y,x)
    if g and is_lijn(y,x) and O[y,x] not in (1,2,6,9):
        O[y,x]=LIJN[g] if lf[y,x]<0.8 else 1; BRON[y,x]='O'
# --- gesp weg (Jordi: "je mag de gesp trouwens bij rock en ijs weglaten"): riem loopt door. Gesp in het model:
# x 22-31, y 37-42 (+ onderrand y 43 x 26-29). Per kolom het riemprofiel van kolom 33 (eerste schone riemkolom rechts).
for y in range(37,43):
    for x in range(22,32):
        if Z[y,x]==10: O[y,x]=O[y,33]; BRON[y,x]='G'
for x in range(26,30):
    if Z[43,x]==10: O[43,x]=O[44,x]; BRON[43,x]='G'
# --- ruis: binnen de doelzones vlakjes < 3 px van één index (lijnkleuren 8-samenhangend, tinten 4-samenhangend)
# gaan op in de meest voorkomende buurkleur van hetzelfde materiaal. Zwart (1) en de buitenrand blijven.
DOEL=np.zeros_like(S)
for m in DEEL.values(): DOEL|=m
MAT={2:'steen',3:'steen',4:'steen',5:'steen',12:'licht',13:'licht',14:'licht',6:'roze',7:'roze',8:'roze',15:'roze',9:'blauw',10:'blauw',11:'blauw'}
SET={'steen':{2,3,4,5},'licht':{4,12,13,14},'roze':{6,7,8,15},'blauw':{9,10,11}}
for ronde in range(3):
    for k in sorted(set(O[DOEL].tolist())-{0,1}):
        st=np.ones((3,3)) if k in (2,4,6,9) else None
        lab,n=nd.label(O==k,structure=st)
        for i in range(1,n+1):
            c=lab==i
            if c.sum()>=3 or (k==14 and (c&np.isin(Z,[2,3])).any()) or not (c&DOEL).any(): continue   # hooglicht mag 2 px
            for y,x in zip(*np.where(c&DOEL)):
                g=next((g for g,t in SET.items() if k in t and (g!='steen' or k!=4 or Z[y,x] not in (2,3,4))),None)
                if g is None: continue
                nb=[O[y+dy,x+dx] for dy,dx in ((0,1),(0,-1),(1,0),(-1,0))]
                nb=[v for v in nb if v in SET[g] and v!=k]
                if nb: O[y,x]=max(set(nb),key=nb.count); BRON[y,x]='R'
# --- losse pixels (geen 8-buur met dezelfde index): ringpixel -> terug naar r5; in een doelzone -> meest voorkomende 8-buur van
# hetzelfde materiaal (anders meest voorkomende 8-buur)
for ronde in range(3):
    kand=DOEL|ring|nd.binary_dilation(O!=R5,structure=np.ones((3,3)))   # ook r5-pixels die door de terugzetting los kwamen
    for y,x in zip(*np.where(kand&S)):
        k=O[y,x]
        if k==0 or (k==14 and Z[y,x] in (2,3)) or any(O[y+dy,x+dx]==k for dy in (-1,0,1) for dx in (-1,0,1) if dy or dx): continue
        if BRON.get((y,x))=='O': O[y,x]=R5[y,x]; BRON.pop((y,x),None); continue
        nb=[O[y+dy,x+dx] for dy in (-1,0,1) for dx in (-1,0,1) if (dy or dx) and O[y+dy,x+dx]]
        g=[gg for gg,t in SET.items() if k in t]
        nbm=[v for v in nb if g and v in SET[g[0]]]
        if not nbm: nbm=nb
        O[y,x]=max(set(nbm),key=nbm.count); BRON[y,x]='R'
np.save('O.npy',O); np.save('doel.npy',DOEL)
import pickle; pickle.dump((BRON,{n:m for n,m in DEEL.items()}),open('bron.pkl','wb'))
p=Image.fromarray(O.astype('uint8'),'P'); p.putpalette(r5.getpalette()); p.save('stap2.png',transparency=0)
