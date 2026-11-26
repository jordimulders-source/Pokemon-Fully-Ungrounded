# Eindkeuring (DC) gaucho-Lombre: basis ../sprite/r3/lombre_gaucho_r3_A.png -> lombre_gaucho_e.png
# Alleen uitvoering: palet (tinten/hue shift), schaduw uit de modelhelderheid (meet.py), omlijning volgens de DC-gids.
# Bevroren (diff 0, bewezen in controle.py): silhouet (alpha), kopvak x17-38 y22-35 (mond A5, ogen r3 A, kopcontour r2/r3).
import sys, os, numpy as np; from PIL import Image
H=os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0,H)
from meet import ML, MC
BRON=os.path.join(H,'..','sprite','r3','lombre_gaucho_r3_A.png')
im=Image.open(BRON); s0=np.array(im); s=s0.copy()
pal=np.array(im.getpalette()[:48]).reshape(16,3)
KOP=np.zeros((64,64),bool); KOP[22:36,17:39]=True
RED={2,3,4,5}; OLI={6,7,8,9,10}
f=s0>0; pd=np.pad(f,1)
UP=~pd[:-2,1:-1]; DN=~pd[2:,1:-1]; LF=~pd[1:-1,:-2]; RT=~pd[1:-1,2:]
RAND=f&(UP|DN|LF|RT)
tel={}; log=[]
def zet(lijst,v,naam):
    n=0
    for x,y in lijst:
        assert not KOP[y,x], ('bevroren',x,y)
        if s[y,x]!=v: s[y,x]=v; n+=1; log.append((naam,x,y))
    tel[naam]=tel.get(naam,0)+n
def mat(v): return 'r' if v in (3,4,5) else 'o' if v in (7,8,9,10) else 'c' if v in (12,13) else None
def buren_mat(arr,x,y):
    return {mat(arr[y+dy,x+dx]) for dy in (-1,0,1) for dx in (-1,0,1)}-{None}

# ---------- 3. Kleurtinten ----------
NIEUW={2:(108,44,30),3:(160,74,50),4:(204,114,80),5:(230,154,112),      # rood: stappen 33/40/35, hue 11->21
       6:(66,56,30),7:(110,98,58),8:(128,100,72),9:(156,142,86),10:(194,180,114),  # olijf: lijn wordt een echte outline base
       12:(180,150,86),13:(232,204,124),                                 # mond = snavel van de gaucho-Lotad (eindversie)
       14:(88,68,50)}                                                    # hoedband schaduw (was ongebruikt)
for k,v in NIEUW.items(): pal[k]=v

# ---------- 1. Schaduw (uit de modelhelderheid; meet.py) ----------
# De tinten volgen de kale reductie per pixel (ML = gemeten modelhelderheid; per index gelijk aan de tint). Twee pixelfouten
# van de kwantisering, gemeten op de modelkleur:
# S1 hoedband: het model heeft een eigen grijsbruine band (licht 115,92,67; schaduw ±75,59,43). Licht stond al apart (8),
#    de schaduw viel in olijf donker (7) en liep zo over in de hoedrand erachter ("hoedband leest drukker").
#    Band-schaduwpixels (model bruin: B > 0,5 R, in de band y14-17 x33-40) -> eigen bandschaduw 14.
band=[(x,y) for y in range(14,18) for x in range(33,41) if s0[y,x]==7 and MC[y,x][2]>0.5*MC[y,x][0]]
zet(band,14,'S1 hoedband schaduw 7->14 (model grijsbruin)')
# S2 nagel rechtervuist: model geel (184,150,82), in olijf licht (10) gekwantiseerd -> nageltint 12.
zet([(33,43)],12,'S2 nagel rechtervuist 10->12 (model geel)')

# ---------- 2. Belijning ----------
# B1 lichtkant van de olijf-buitenlijn in de eigen outline base (6) i.p.v. de schaduwtint (7);
#    outline highlight (7) alleen waar het vlak erbinnen het lichtst is (10) - gids: "outline highlight ... in the very most highlighted parts".
c6=[];c7=[]
for y,x in zip(*np.where(RAND&(s0==7)&(UP|LF)&~(DN|RT)&~KOP)):
    binnen=[s0[y+dy,x+dx] for dy,dx in ((1,0),(0,1),(1,1)) if s0[y+dy,x+dx]>1]
    (c7 if 10 in binnen else c6).append((x,y))
zet(c6,6,'B1 lichtkant olijf 7->6 (outline base)')
# B2 binnenlijnen binnen één onderdeel niet zwart en in de eigen lijntint (gids: binnenlijnen in de donkerste eigen tint)
c2=[];c6b=[]
for y,x in zip(*np.where(((s0==1)|(s0==2)|(s0==6))&~RAND&~KOP)):
    m=buren_mat(s0,x,y)
    if m=={'r'} and s0[y,x]!=2: c2.append((x,y))
    if m=={'o'} and s0[y,x]!=6 and not (y==21 and x in (21,22)): c6b.append((x,y))   # (21-22,21): onderkant hoedrand over de kop = vorm over vorm, blijft zwart
zet(c2,2,'B2 binnenlijn in rood -> rode lijn (2)')
zet(c6b,6,'B2 binnenlijn in olijf -> olijflijn (6)')

# B3 dubbele lijnen (2 px dik) -> 1 px (gids: "remove the clusters so that the outline is always one pixel wide").
#    De lijn die de grens tussen twee onderdelen is blijft (zwart = vorm over vorm); de tweede lijn krijgt de tint van het vlak ernaast.
zet([(29,39),(29,40),(29,41),(29,42)],9,'B3 dubbele lijn arm|band: band-kant -> bandtint (9)')
zet([(28,40),(28,41)],1,'B3 dubbele lijn arm|band: grens zwart (vorm over vorm)')
zet([(40,31),(41,31)],7,'B3 dubbele lijn kraag: bovenste lijn -> vlaktint (7)')
zet([(15,44),(16,44)],3,'B3 dubbele lijn onder vuist links -> vuisttint (3)')
zet([(39,47),(40,47)],7,'B3 dubbele lijn vest|dij: bovenste lijn -> vesttint (7)')
zet([(39,48),(40,48),(41,48)],1,'B3 dubbele lijn vest|dij: grens zwart (vorm over vorm, schaduwkant)')
zet([(47,52),(47,53)],7,'B3 dubbele buitenlijn rechts been: binnenste -> vlaktint (7)')
zet([(40,60)],3,'B3 dubbele lijn voet rechts -> voettint (3)')
# B4 lijn van de hoedband in één kleur (zwart, zoals de rest van die lijn en het model (52,43,27) / (1,3,0)).
zet([(33,14),(36,18)],1,'B4 hoedbandlijn olijflijn -> zwart (één lijn, één kleur)')

if __name__=='__main__':
    from uit import opslaan, preview
    pal0=np.array(im.getpalette()[:48]).reshape(16,3)
    out=os.environ.get('OUT',os.path.join(H,'lombre_gaucho_e.png'))
    opslaan(s,pal,out)
    if os.environ.get('PREV'): preview(s,pal,s0,pal0,os.environ['PREV'],Z=10,box=(9,4,55,64))
    for k,v in tel.items(): print('%-62s %d'%(k,v))
    print('totaal gewijzigde pixels', int((s!=s0).sum()), '| alpha-diff', int(((s>0)!=(s0>0)).sum()),
          '| kopvak-diff', int((s[KOP]!=s0[KOP]).sum()), '| kleuren incl. transparant', len(np.unique(s)))
