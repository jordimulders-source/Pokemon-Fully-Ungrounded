# Eindkeuring (DC) gaucho-Lotad: basis sprite/r3/lotad_gaucho_oogG.png -> lotad_gaucho_e.png
# Alleen uitvoering: palet (hue shift), schaduw uit de modelhelderheid, omlijning volgens de DC-gids.
# Silhouet (alpha), ogen (x18-33,y39-41), kraagpuntvorm en poten (alpha) blijven gelijk; controle in controle.py.
import sys, os, numpy as np; from PIL import Image
H=os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0,H)
from meet import ML, fm, randkaart
BRON=os.path.join(H,'..','sprite','r3','lotad_gaucho_oogG.png')
im=Image.open(BRON); s0=np.array(im); s=s0.copy()
pal=np.array(im.getpalette()[:48]).reshape(16,3)
tel={}; log=[]
OOG=np.zeros((64,64),bool); OOG[39:42,18:34]=True
rand=randkaart(s0)
def zet(lijst,v,naam):
    n=0
    for x,y in lijst:
        assert not OOG[y,x], (x,y)
        if s[y,x]!=v: s[y,x]=v; n+=1; log.append((naam,x,y))
    tel[naam]=tel.get(naam,0)+n

# ---------- 3. Kleurtinten: r1-families, hue shift (schaduw roder/verzadigder, licht lichter en geler) ----------
NIEUW={2:(108,52,34),3:(156,86,58),4:(192,118,80),5:(222,152,106),
       6:(86,62,44),7:(124,104,74),8:(164,137,92),
       10:(180,150,86),11:(232,204,124)}
for k,v in NIEUW.items(): pal[k]=v

# ---------- 1. Schaduw ----------
# Kraag: donkerbruin (6) alleen waar het model donker is of een lijn heeft; elders de middentint (7).
TK=int(os.environ.get('TK',135))
kraag=(fm==5)&(s0>=6)&(s0<=9)
c=[]
for y,x in zip(*np.where(kraag&(s0==6)&~rand)):
    nb=[ML[yy,xx] for yy in range(y-2,y+3) for xx in range(x-2,x+3) if kraag[yy,xx]]
    if ML[y,x]>=TK and ML[y,x]>=np.median(nb)-12: c.append((x,y))
zet(c,7,'S1 kraag 6->7 (model midden)')

# ---------- 2. Belijning ----------
# 2a. Zwarte klonters: binnenpixel zwart in de binnenhoek van een getrapte buitenlijn (zwarte randburen boven/onder EN
#     links/rechts) -> de donkerste eigen tint van dat onderdeel (gids: "remove the clusters so that the outline is always
#     one pixel wide"). Lijn blijft 8-verbonden.
DONKER={2:2,3:2,4:6,5:6,6:6}
c={}
for y,x in zip(*np.where((s0==1)&~rand&~OOG)):
    v=any(s0[y+d,x]==1 and rand[y+d,x] for d in (-1,1)); h=any(s0[y,x+d]==1 and rand[y,x+d] for d in (-1,1))
    if v and h:
        ms=[fm[y+dy,x+dx] for dy in (-1,0,1) for dx in (-1,0,1) if s0[y+dy,x+dx]>1]
        if ms:
            m=max(set(ms),key=ms.count); c.setdefault(DONKER[m],[]).append((x,y))
for v,l in c.items(): zet(l,v,'B1 klonter in binnenhoek -> eigen donker')

# 1b. Losse middentint-pixels die S1 midden in donkerbruin zette (eilandje van 1 px) terug naar 6: geen ruis toevoegen.
from clusters import kleine
terug=[(x,y) for v,comp in kleine(s,2) if v==7 for (x,y) in comp if s0[y,x]==6]
zet(terug,6,'S1b los 7-eilandje terug naar 6')

# 2b. Afwisseling zwart/gekleurd op een buitenrand (SPRITE_KERN: nooit om en om op een rand; zwart als boog van
#     linksmidden via linksonder): hoedrand links y33-35, kop links y39-42, kraag links y51-55.
zet([(11,34)],1,'B2 buitenrand: om-en-om opgeheven')          # hoedrand links: 1,2,1 -> zwart (onderkant links)
zet([(17,41)],2,'B2 buitenrand: om-en-om opgeheven')          # kop links boven de snavel: 2,2,1,2 -> gekleurd (lichtkant)
zet([(18,53),(18,54)],1,'B2 buitenrand: om-en-om opgeheven')  # kraag links onder: 1,1,6,6,1 -> zwart (linksonder)

# 2c. Binnenlijn binnen een onderdeel niet zwart: een losse zwarte pixel in de lijn kroon/rand rechts (overige lijn = 2).
zet([(41,27)],2,'B3 binnenlijn hoed zwart -> eigen donker')

# 2d. Snavel-bovenlijn doorlopend in de snavellijn (6) i.p.v. om en om 6/2; de hoekpixel krijgt de kopkleur volgens het model.
zet([(24,42),(25,42)],6,'B4 snavellijn doorlopend')
zet([(26,42)],5,'B4 snavellijn doorlopend')                   # ML 131, buren kop licht (5)

# 2e. Outline highlights (gids: "shadow/outline highlight color on the outlines in the very most highlighted parts ...
#     on the inside of the outline"): alleen waar het model aan de rand het lichtst is (ML >= 160) en het vlak binnen licht is.
zet([(27,23),(26,24),(30,22)],3,'B5 outline highlight hoed (2->3)')
zet([(18,49),(17,50)],7,'B5 outline highlight kraagpunt (6->7)')

if __name__=='__main__':
    from uit import opslaan, preview
    pal0=np.array(im.getpalette()[:48]).reshape(16,3)
    out=os.environ.get('OUT',os.path.join(H,'lotad_gaucho_e.png'))
    opslaan(s,pal,out)
    if os.environ.get('PREV'): preview(s,pal,s0,pal0,os.environ['PREV'])
    for k,v in tel.items(): print('%-45s %d'%(k,v))
    print('totaal gewijzigde pixels', int((s!=s0).sum()), '| alpha-diff', int(((s>0)!=(s0>0)).sum()),
          '| oog-diff', int((s[OOG]!=s0[OOG]).sum()), '| kleuren incl. transparant', len(np.unique(s)))
