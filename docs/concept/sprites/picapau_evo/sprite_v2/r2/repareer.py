# Reparaties op schoon.npy, elk benoemd en gemeten op het model -> r2.npy (ronde 2: reparaties van de coordinator op r1). Telt per zone de afwijking van de kale reductie.
# codes: 1 zwart, 2/3/4 bruin l/m/d, 5/6/7 creme l/m/d, 8 wang, 9/10/11 grijs l/m/d, 12/13 geel l/d, 14 wit, 15 selout bruin
import numpy as np
from celregel import cel
from kuif import U, L as KL, cells, pp
o=np.load('schoon.npy').copy(); kaal=np.load('kaal.npy'); H,W=o.shape
R={}
def zet(zone,lst):
    for x,y,v in lst:
        if o[y,x]!=v: R.setdefault(zone,[]).append((x,y,int(o[y,x]),v)); o[y,x]=v
def ring(zone,mask):
    # buitenlijn: gekleurde pixel in de zone die aan achtergrond grenst -> zwart (bruin aan de lichtkant -> selout)
    lst=[]
    for y,x in zip(*np.where(mask)):
        v=o[y,x]
        if v in (0,1,15): continue
        nb=[(y-1,x),(y+1,x),(y,x-1),(y,x+1)]
        bg=[0<=a<H and 0<=b<W and o[a,b]==0 for a,b in nb]
        if any(bg): lst.append((x,y,15 if v in (2,3,4) and (bg[0] or bg[2]) and not (bg[1] or bg[3]) else 1))
    zet(zone,lst)
# 1 kuif: middenlijn van beide slierten gemeten op het model (kuif.py), krul en haakje in de punten
z=np.load('lucht.npy'); kz=np.zeros_like(z); kz[0:11,12:49]=True; kz&=z
S=pp(cells(U)|cells(KL))
zet('kuif',[(x,y,1 if (y,x) in S else 0) for y,x in zip(*np.where(kz))]+[(x,y,1) for y,x in S])
# 1b krul als spiraaltje (model: U loopt over rij 6,8 naar x45, gaat rechts omhoog (46,5), over de top (45,3.9), links
#    omlaag (44.3,4.5) en eindigt binnenin (45,5)). Op 64 px te klein (2x2,6 px): vergroot tot 4x4 (x43-46, rij 3-6),
#    ring met het binnenste eind als 1 px vanaf linksboven naar binnen, gat L-vormig. Haakje: J met gat (8,41) zoals het model.
zet('krul',[(43,6,1),(44,6,1),(45,6,1),(46,5,1),(46,4,1),(45,3,1),(44,3,1),(43,4,1),(43,5,1),(44,4,1),(45,4,0),(44,5,0),(45,5,0),(46,6,0),(46,3,0),(43,3,0)])
zet('haakje',[(39,7,1),(40,8,1),(40,9,1),(41,9,1),(42,8,1),(41,8,0),(39,8,0),(42,9,0)])
# 1c koprand: de wis-zone van de kuif nam de modelkoprand mee; terug naar het model (rij 5 x20-22 omlijning, 30-52% zwart;
#    rij 6 x21-23 donkerbruine schaduw, lum 86-89; (16,6) zwart 47%)
zet('koprand',[(20,5,1),(21,5,1),(22,5,1),(21,6,4),(22,6,4),(23,6,4),(16,6,1)])
# 2 oog: modeloog x 18,9-22,2, y 10,1-13,9 (rond, donker, glans linksboven, iris onderin bruingrijs) -> rond 4x4 op x19-22,
#    hoeken weg; glans 1 px op (20,11), iris (h) op rij 12 midden. Geen gat meer, glans binnen het zwart.
zet('oog',[(19,10,3),(20,10,1),(21,10,1),(22,10,3),(19,11,1),(20,11,14),(21,11,1),(22,11,1),
           (19,12,1),(20,12,11),(21,12,11),(22,12,1),(19,13,5),(20,13,1),(21,13,1),(22,13,5)])
# 3 snavel: wig naar het model (lum per cel): bovensnavel licht (lum 164-178) rij 13-14, mondlijn rij 15 donkergrijs
#    (30-37% zwart, lum 109-144) i.p.v. zwart, ondersnavel G rij 15-16, punt licht met zwarte lijn eromheen,
#    bovenrand als donkergrijze lijn (h) tegen het bruine gezicht en zwart (32-46%) linksboven naar de punt.
zet('snavel',[(13,12,1),(14,12,11),(15,12,11),(16,12,3),
              (10,13,1),(11,13,4),(12,13,1),(13,13,9),(14,13,9),(15,13,9),(16,13,11),
              (10,14,1),(11,14,1),(12,14,9),(13,14,9),(14,14,9),(15,14,9),(16,14,9),
              (9,15,1),(10,15,9),(11,15,9),(12,15,10),(13,15,11),(14,15,11),(15,15,11),(16,15,10),(17,15,1),
              (9,16,0),(10,16,1),(11,16,1),(12,16,1),(13,16,1),(14,16,10),(15,16,10),(16,16,10)])
# 4 bliksem: celregel op het model (>=50% wit = leeg, >=30% zwart = lijn), daarna buitenlijn
bz=np.zeros((H,W),bool); bz[27:44,0:11]=True; bz[44:49,0:13]=True
zet('bliksem',[(x,y,cel(x,y,zw=0.30)) for y,x in zip(*np.where(bz))])
ring('bliksem',bz)
# 5 poten: per cel op het model (wit>=50% leeg, zwart>=45% lijn, anders toon op lum, poten.py) en daarna met de teenlijnen
#    van het model (zwarte kolom x21 rij 48-50 links; donkere kolom x28 rechts): drie tenen per poot met klauwtjes.
#    Verre poot (links, achter: zelfde kant als de verre vleugel) een tint donkerder (G/h), nabije poot g/G/h.
F={}
F.update({(20,45):1,(21,45):11,(22,45):1,
 (19,46):1,(20,46):10,(21,46):11,(22,46):1,
 (18,47):1,(19,47):11,(20,47):10,(21,47):10,(22,47):11,(23,47):1,
 (18,48):1,(19,48):11,(20,48):10,(21,48):1,(22,48):11,(23,48):1,
 (18,49):1,(19,49):11,(20,49):10,(21,49):1,(22,49):11,(23,49):1,
 (18,50):1,(19,50):1,(20,50):10,(21,50):1,(22,50):1,(23,50):0,
 (18,51):0,(19,51):0,(20,51):1,(21,51):0,(22,51):0, (19,52):0,(20,52):0,(21,52):0})
F.update({(26,47):1,(27,47):9,(28,47):10,(29,47):10,(30,47):1,
 (25,48):1,(26,48):9,(27,48):9,(28,48):10,(29,48):10,(30,48):1,
 (25,49):1,(26,49):10,(27,49):9,(28,49):11,(29,49):10,(30,49):1,
 (25,50):1,(26,50):1,(27,50):9,(28,50):1,(29,50):10,(30,50):1,
 (25,51):0,(26,51):0,(27,51):1,(28,51):0,(29,51):1,(30,51):0,
 (26,52):0,(27,52):0,(28,52):0,(29,52):0,(28,53):0})
zet('poten',[(x,y,v) for (x,y),v in F.items()])
# 6 ruis: donkere modellijnstipjes (h) los in bruin -> donkerbruin (binnenlijn in een donkere tint van het vlak)
zet('ruis',[(31,23,4),(46,27,4),(13,11,1)])
# losse tintpixels (<3 px-regel): eenzame tint binnen een kleurgroep -> meest voorkomende buurtint van dezelfde groep
G={2:'b',3:'b',4:'b',5:'c',6:'c',7:'c',12:'y',13:'y'}
lst=[]
for y in range(1,H-1):
    for x in range(1,W-1):
        v=o[y,x]
        if v not in G: continue
        nb=[o[a,b] for a in range(y-1,y+2) for b in range(x-1,x+2) if (a,b)!=(y,x)]
        if v in nb: continue
        same=[n for n in nb if G.get(n)==G[v]]
        if same: lst.append((x,y,max(set(same),key=same.count)))
zet('losse tint',lst)
# 7 selout: buitenlijn aan de lichtkant naast bruin of creme (buik) -> donkerbruine selout, schaduwkant zwart. Lichtkant gemeten met de
#   randnormaal over 5x5 (achtergrond boven+links > onder+rechts), zodat trappen niet om en om zwart/selout worden.
#   Niet op kuif/koord (lucht-zone). Daarna: losse selout/zwart in een randketen gelijk aan zijn twee randburen.
lst=[]; E={}
for y in range(H):
    for x in range(W):
        v=o[y,x]
        if v not in (1,15) or z[y,x] or bz[y,x]: continue
        if not any((0<=a<H and 0<=b<W and o[a,b]==0) for a,b in ((y-1,x),(y+1,x),(y,x-1),(y,x+1))): continue
        br=any(o[a,b] in (2,3,4,5,6,7) for a in range(max(0,y-1),min(H,y+2)) for b in range(max(0,x-1),min(W,x+2)))
        if not br: continue
        y0,y1,x0,x1=max(0,y-2),min(H,y+3),max(0,x-2),min(W,x+3)
        w=o[y0:y1,x0:x1]==0; yy,xx=np.mgrid[y0:y1,x0:x1]
        up=(w&(yy<y)).sum()+(w&(xx<x)).sum(); dn=(w&(yy>y)).sum()+(w&(xx>x)).sum()
        E[(y,x)]=15 if up>dn else 1
for _ in range(2):   # losse selout tussen zwart (of andersom) in de randketen gelijkmaken
    F=dict(E)
    for (y,x),v in E.items():
        nb=[E[(y+a,x+b)] for a in (-1,0,1) for b in (-1,0,1) if (a or b) and (y+a,x+b) in E]
        if len(nb)>=2 and all(n!=v for n in nb): F[(y,x)]=nb[0]
    E=F
for (y,x),want in E.items():
    if want!=o[y,x]: lst.append((x,y,want))
zet('selout',lst)
lst=[]
for y in range(H):
    for x in range(W):
        v=o[y,x]
        if v not in (1,15) or z[y,x] or bz[y,x]: continue
        nb=[o[a,b] for a in range(max(0,y-1),min(H,y+2)) for b in range(max(0,x-1),min(W,x+2)) if (a,b)!=(y,x)]
        if v==15 and 15 not in nb and 1 in nb: lst.append((x,y,1))
        if v==1 and 1 not in nb and 15 in nb and 0 in nb: lst.append((x,y,15))
zet('selout',lst)
np.save('r2.npy',o)
tot=0
for zn,l in R.items():
    print('%-10s %3d px'%(zn,len(l))); tot+=len(l)
d=(o!=kaal).sum(); print('totaal reparaties',tot,'| verschil met kale reductie (incl. schoon)',d)
