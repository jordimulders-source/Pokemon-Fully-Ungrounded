# Kleurronde k5 tempel: vanaf k4. Rechts drie toonzones zoals het model: lichte bovenranden,
# middengrijze zijvlakken (grote stenen, voegen in 7), donkere gladde bergwand (f + e-facet). Gevelplaten: nok 1 px.
import sys, os, numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','k1'))
from gereedschap import *
H=os.path.dirname(os.path.abspath(__file__))
a,pal=laad(os.path.join(H,'..','k4','tempel.png'))
E,F,V=14,15,7
MOS=(8,9,13)
def vrij(x,y): return a[y,x] not in MOS and a[y,x] not in (0,1)
def zet(pts,c):
    for (x,y) in pts:
        if vrij(x,y): a[y,x]=c
def R(d):  # {y:(x0,x1)}
    return [(x,y) for y,(x0,x1) in d.items() for x in range(x0,x1+1)]
def stenen(masker, voegen, toon):
    """masker min voegen -> stenen (4-samenhang); toon(cx,cy) -> één tint per steen; voegen in 7"""
    m={p for p in masker if vrij(*p)}; vs=set(voegen)
    zet([p for p in vs if p in m],V)
    rest=m-vs; gezien=set(); n=0
    for p in sorted(rest):
        if p in gezien: continue
        st=[]; stack=[p]; gezien.add(p)
        while stack:
            q=stack.pop(); st.append(q)
            for d in ((1,0),(-1,0),(0,1),(0,-1)):
                r=(q[0]+d[0],q[1]+d[1])
                if r in rest and r not in gezien: gezien.add(r); stack.append(r)
        cx=sum(q[0] for q in st)/len(st); cy=sum(q[1] for q in st)/len(st)
        zet(st,toon(cx,cy)); n+=1
    return n

# ---------- 1. Bergwand: glad f-vlak met één diagonale e-facet (schaduwbaan van het model), geen voegen/6 ----------
BW=R({15:(55,55),16:(55,55),17:(55,55),18:(55,55),19:(55,55),20:(55,56),21:(55,56),22:(55,56),23:(55,56),24:(55,56),25:(55,57),26:(55,57),
      29:(56,57),30:(56,58),31:(56,58),32:(56,58),33:(56,58),34:(56,58),35:(56,59),36:(56,59),37:(56,59),38:(56,59),
      39:(59,59),40:(59,60),41:(59,60),42:(59,60),43:(59,60),44:(59,60),45:(60,61),46:(60,61),47:(60,61),48:(60,61)})
for (x,y) in BW:
    if vrij(x,y): a[y,x]= E if y>=20+(x-55)*10/3 else F

# ---------- 4. Bovenranden ----------
zet(R({11:(48,52)}),5)                       # bovenkant bovenste terras, door tot de bergwand
zet(R({27:(53,57),28:(52,57)}),4)            # bovenrand middelste terras, door tot de bergwand
RAND=R({40:(49,55),41:(49,55),42:(50,55)})+R({39:(56,58),40:(56,58),41:(56,58)})
for (x,y) in RAND:
    if vrij(x,y): a[y,x]= 4 if x<=53 else 5   # bovenvlak blok rechtsonder, 3 px dik, naar achteren een tint donkerder

# ---------- 2. Zijvlakken: basis 6, naar rechts/onder f; grote stenen, voegen in 7 ----------
# boven (rechts van de vouwlijn)
TS=R({12:(48,53),13:(48,54),14:(48,54),15:(49,54),16:(49,54),17:(50,54),18:(50,54),19:(50,54),20:(51,54),21:(51,54),
      22:(51,54),23:(51,54),24:(51,54),25:(51,54),26:(53,54)})
Vts=[(48,15),(49,15),(50,15),(51,15),(51,14),(52,14),(53,14),(54,14),(54,13), (51,12),(51,13),
     (51,21),(52,21),(52,20),(53,20),(54,20), (52,16),(52,17),(52,18),(52,19)]
Vts=[p for p in Vts if p!=(48,15)]           # (48,15) is de vouwlijn (e), laten staan
n1=stenen(TS,Vts,lambda cx,cy: 6 if cy<20.5 else F)
# boven, links van de vouwlijn
US=R({18:(45,48),19:(45,48),20:(45,49),21:(45,49),22:(45,49),23:(45,49),24:(45,49),25:(45,49)})
Vus=[(45,22),(46,22),(47,22),(47,21),(48,21),(49,21),(47,23),(47,24),(47,25)]
n2=stenen(US,Vus,lambda cx,cy: 6 if cy<21.5 or cx<47 else F)
# midden
MS=R({29:(45,55),30:(41,55),31:(41,55),32:(41,55),33:(41,55),34:(41,55),35:(41,55),36:(41,55),37:(41,55),38:(41,55),39:(41,55),40:(41,44),41:(41,42)})
MS=[p for p in MS if p not in RAND]
Vms=[(41,35),(42,35),(43,35),(44,34),(45,34),(46,34),(47,33),(48,33),(49,33),(50,32),(51,32),(52,32),(53,31),(54,31),(55,31),
     (46,29),(46,30),(46,31),(46,32),(46,33),(51,29),(51,30),(51,31),
     (48,34),(48,35),(48,36),(48,37),(48,38),(48,39),(53,32),(53,33),(53,34),(53,35),(53,36),(53,37),(53,38),(53,39)]
n3=stenen(MS,Vms,lambda cx,cy: 6 if cx<50.5 and not (cy>33 and cx>48) else F)
# blok rechtsonder
top={44:45,45:47,46:48,47:45,48:44,49:44,50:43,51:43,52:43,53:43,54:43,55:43,56:42,57:42,58:42,59:45,60:49}
LS=[]
for x,y0 in top.items():
    for y in range(y0,62):
        if a[y,x] in (0,1): break
        LS.append((x,y))
LS=[p for p in LS if p not in RAND]
J1=[(44,53),(45,53),(45,52),(46,52),(47,52),(47,51),(48,51),(49,51),(49,50),(50,50),(51,50),(51,49),(52,49),(53,49),(53,48),(54,48),(55,48),(55,47),(56,47),(57,47),(57,46),(58,46),(59,46),(59,45)]
Vls=J1+[(50,43),(50,44),(50,45),(50,46),(50,47),(50,48),(50,49),(55,43),(55,44),(55,45),(55,46),
        (48,52),(48,53),(48,54),(48,55),(48,56),(48,57),(48,58),(53,49),(53,50),(53,51),(53,52),(53,53),(53,54),(53,55)]
n4=stenen(LS,Vls,lambda cx,cy: 6 if cx<54.5 and not (cy>49 and cx>48) else F)

# ---------- 5. Gevelplaten: nok 1 px (6) langs de schuine bovenrand, rest f, voet e ----------
def plaat(rijen, nok, voet):
    for y,(x0,x1) in rijen.items():
        for x in range(x0,x1+1): a[y,x]=F
    for p in nok: a[p[1],p[0]]=6
    for p in voet: a[p[1],p[0]]=E
plaat({19:(22,26),20:(22,26),21:(23,27),22:(23,27),23:(24,28),24:(24,28),25:(25,29),26:(26,29)},
      [(22,19),(23,19),(22,20),(23,20),(23,21),(23,22),(24,22),(24,23),(24,24),(25,24),(25,25),(26,25),(26,26)],[(28,26),(29,26)])
plaat({20:(35,38),21:(35,38),22:(36,39),23:(36,39),24:(37,40),25:(37,40),26:(38,41)},
      [(35,20),(36,20),(35,21),(36,21),(36,22),(36,23),(37,23),(37,24),(37,25),(38,25),(38,26)],[(40,26),(41,26)])
plaat({9:(33,34),10:(32,34),11:(33,35),12:(33,35),13:(34,36),14:(34,36)},
      [(33,9),(32,10),(33,10),(33,11),(33,12),(34,12),(34,13)],[(36,14)])
# losse pixels opruimen (clusters < 3 px)
a[16,49]=E; a[20,49]=E                     # vouwlijn bovenste blok aaneengesloten
for (x,y) in [(57,25),(57,26)]: a[y,x]=E   # bergwand: facet
a[41,40]=6                                 # hoekpixel bij de steen van het middelste zijvlak
a[15,45]=4                                 # bovenrand bovenste terras aaneen
a[18,44]=6; a[19,44]=6                     # bij de steen van het zijvlak
a[26,39]=E                                 # voet gevelplaat G2: 3 px
print('stenen boven/US/midden/onder:',n1,n2,n3,n4)
bewaar(a,pal,os.path.join(H,'tempel.png'))
