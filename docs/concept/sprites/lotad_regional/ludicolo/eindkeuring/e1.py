# Eindkeuring (DC) gaucho-Ludicolo: basis ../sprite/r1/ludicolo_gaucho_0.png (Jordi: "de eerste") -> ludicolo_gaucho_e.png
# Alleen uitvoering: palet (tinten, hue shift; geel = lijntinten op Jordi's besluit), schaduw uit de modelhelderheid (meet.py),
# omlijning volgens de DC-gids. Bevroren (diff 0, bewezen in controle.py): silhouet (alpha) en het gezichtsvak x15-35 y22-34
# (ogen, snavel, mond, oogmasker); alleen de losse oogvarianten (oog.py) raken het rechteroog aan.
import sys, os, numpy as np; from PIL import Image
H=os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0,H)
from meet import ML, MC, BASIS
im=Image.open(BASIS); s0=np.array(im); s=s0.copy()
pal=np.array(im.getpalette()[:48]).reshape(16,3)
P=np.load(os.path.join(H,'..','sprite','r1','poncho_masker.npy'))          # ponchogebied van de maker (513 px)
GEZ=np.zeros((64,64),bool); GEZ[22:35,15:36]=True
RED={3,4,5,6,7}; OLI={9,10,11}; GEEL={12,13}
tel={}; log=[]
def zet(lijst,v,naam):
    n=0
    for x,y in lijst:
        assert not GEZ[y,x], ('bevroren gezicht',x,y)
        if s[y,x]!=v: s[y,x]=v; n+=1; log.append((naam,x,y))
    tel[naam]=tel.get(naam,0)+n
def nb8(y,x): return [(y+dy,x+dx) for dy in (-1,0,1) for dx in (-1,0,1) if (dy or dx) and 0<=y+dy<64 and 0<=x+dx<64]

# ---------- 3. Kleurtinten (palet) ----------
NIEUW={3:(128,54,38),   # rood diep      L 81 -> 74  (hue 11)
       4:(160,74,50),   # rood donker    = Lombre-schaduw, ongewijzigd (L 97, hue 13)
       5:(192,98,66),   # rood mdonker   L118 -> 122 (hue 15)
       6:(214,126,88),  # rood midden    L137 -> 148 (hue 18)
       12:(180,150,86), # geel donker  = mond/nagel midden gaucho-Lombre = snavel (180,150,86) gaucho-Lotad (Jordi: "zoals de rest van de lijn")
       13:(232,204,124)}# geel licht   = mond/nagel licht gaucho-Lombre = snavel (232,204,124) gaucho-Lotad
for k,v in NIEUW.items(): pal[k]=v

# ---------- 1. Schaduw ----------
# S1 slagschaduw onder de hoedrand (rechts van het gezicht) en de schouderstrook: in de kale reductie gestemd als rode LIJN (2),
#    als vlak van 2+ px dik. Model daar L 66-90 (111,51,39 e.d.) = de diepe schaduwtint, geen lijn. 2 -> rood diep (3), zodat
#    de lijntint alleen lijn is (gids: outline base = de lijn). Relatieve helderheid blijft: band (74) < rood donker (97) ernaast.
blok=np.zeros((64,64),bool)
for y in range(63):
    for x in range(63):
        if (s0[y:y+2,x:x+2]==2).all(): blok[y:y+2,x:x+2]=True
zet([(x,y) for y,x in zip(*np.where(blok&(ML>=66)&~GEZ))],3,'S1 slagschaduw als lijntint gestemd 2->3 (model L>=66)')

# ---------- 2. Belijning ----------
# B1 Jordi: "let op de zwarte lange verticale lijn in de poncho". Zwarte lijnen BINNEN de poncho (alle buren rood en binnen het
#    ponchomasker; niet tegen arm, voet, been, achtergrond) -> rode lijn (2). Zwart blijft waar vorm over vorm valt.
B1=[]
for y,x in zip(*np.where((s0==1)&P&~GEZ)):
    vals=[s0[q] for q in nb8(y,x)]
    if any(v==0 or v in OLI|GEEL|{8} for v in vals): continue
    if all(P[q] for q in nb8(y,x) if s0[q] in RED): B1.append((x,y))
zet(B1,2,'B1 zwarte binnenlijn in de poncho -> rode lijn (2)')

# B2 dubbele lijnen -> 1 px (gids: "remove the clusters so that the outline is always one pixel wide"). Na B1 lagen de nieuwe
#    rode binnenlijnen op een paar plekken naast een tweede lijn (de oude lijntint-strook naast de zwarte lijn, of de zwarte
#    armgrens). De lijn die de vorm draagt blijft; de tweede pixel krijgt de rode vlaktint die het dichtst bij de modelhelderheid ligt.
LUM={k:0.299*pal[k][0]+0.587*pal[k][1]+0.114*pal[k][2] for k in (3,4,5,6)}
def vlak(x,y): return min(LUM,key=lambda k:abs(LUM[k]-ML[y,x]))
for naam,lijst in (('B2 schouderlijn rechts: strook naast de lijn',[(43,37),(44,37),(42,38),(43,38)]),
                   ('B2 bladlijn links (x17-19): 2x2-knoop',[(18,42)]),
                   ('B2 bladlijn links langs de armgrens (x13-16)',[(14,42),(16,47),(16,49),(17,49)]),
                   ('B2 bladlijn midden (x31-35): tweede lijn',[(32,42),(33,45),(35,46)])):
    for x,y in lijst: zet([(x,y)],vlak(x,y),naam+' -> vlaktint (ML)')

# B3 dubbele lijnen in de hoed -> 1 px.
#  - onder de hoedband: rij 16 (x24-35) is de bandlijn; rij 17 x29-33 lag er als tweede zwarte rij onder, terwijl het model daar
#    rand-vlak is (ML 95-96 = rood donker, x33 ML 70) -> vlaktint volgens ML. Rij 17 x34-42 blijft zwart (enige lijn daar, ML <= 34).
for x in range(29,34): zet([(x,17)],vlak(x,17),'B3 onder de hoedband: tweede zwarte rij -> vlaktint (ML)')
#  - onderkant hoedrand rechts: rij 25 x40-51 is de buitenlijn (tegen de achtergrond / slagschaduw), rij 24 x40-51 lag er als
#    tweede zwarte rij boven (model: dikke zwarte onderrand). Gids: lijn 1 px -> rij 24 wordt de onderkant van de rand in de
#    donkerste vlaktint (rood diep 3), zodat de rand een donkere onderzijde krijgt i.p.v. een 2 px zwarte balk.
zet([(x,24) for x in range(40,52)],3,'B3 onderkant hoedrand rechts: tweede zwarte rij -> rood diep (3)')

if __name__=='__main__':
    from uit import opslaan, preview
    pal0=np.array(im.getpalette()[:48]).reshape(16,3)
    out=os.environ.get('OUT',os.path.join(H,'ludicolo_gaucho_e.png'))
    opslaan(s,pal,out)
    if os.environ.get('PREV'): preview(s,pal,s0,pal0,os.environ['PREV'],Z=10,box=(5,0,58,64))
    for k,v in tel.items(): print('%-66s %d'%(k,v))
    print('totaal gewijzigde pixels', int((s!=s0).sum()), '| alpha-diff', int(((s>0)!=(s0>0)).sum()),
          '| gezicht-diff', int((s[GEZ]!=s0[GEZ]).sum()), '| kleuren incl. transparant', len(np.unique(s)))
