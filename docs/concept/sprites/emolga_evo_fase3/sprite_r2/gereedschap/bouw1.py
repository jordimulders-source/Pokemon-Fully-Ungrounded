# bouw1.py: A0 = kale reductie (bouw0) + technische opschoning + per-pixelreparaties naar het model. Elke wijziging wordt gelogd
# met zone en reden; aan het eind telling per zone t.o.v. kaal.png. Uitvoer: ../tussen/a0_pre.png (voor de automatische rand/korrel)
# en ../A0.png.
import sys; sys.path.insert(0,'/home/user/Pokemon-Fully-Ungrounded/docs/concept/sprites/emolga_evo_fase3/sprite_r1/gereedschap')
from fv import *; import palet
K,Dk,E,Gl,y,Y,L,B,W,w,M,N,O=range(1,14)
kaal=np.asarray(Image.open(D+'sprite_r1/tussen/kaal.png')).astype(int)
o=kaal.copy(); LOG=[]; BESCHERMD=np.zeros((64,64),bool)
def zet(x,yy,v,zone,reden,bescherm=False):
    if o[yy,x]!=v: LOG.append((zone,x,yy,palet.CH[o[yy,x]],palet.CH[v],reden))
    o[yy,x]=v
    if bescherm: BESCHERMD[yy,x]=True
blok=modelblokken()                    # (64,64,256,3) modelpixels per spritepixel
LUM=np.median(blok.mean(-1),-1)        # mediane helderheid van het model per spritepixel
GEEL=(o>=y)&(o<=L)
def lijn(pts):
    # 1-px lijn door gemeten modelpunten (x,y in spritecoordinaten): dicht bemonsteren, afronden, L-hoekjes weg.
    s=[]
    for (x0,y0),(x1,y1) in zip(pts[:-1],pts[1:]):
        for t in np.linspace(0,1,40):
            p=(int(round(x0+(x1-x0)*t)),int(round(y0+(y1-y0)*t)))
            if not s or s[-1]!=p: s.append(p)
    i=1
    while i<len(s)-1:
        a,b,c=s[i-1],s[i],s[i+1]
        if abs(a[0]-c[0])==1 and abs(a[1]-c[1])==1: s.pop(i)
        else: i+=1
    return s
def beste_niet_geel(x,yy):
    # vervanging voor een gele pixel die niet op de modellijn ligt: de meest voorkomende niet-gele buurkleur
    nb=[o[yy+dy,x+dx] for dy in (-1,0,1) for dx in (-1,0,1) if (dy or dx) and 0<=yy+dy<64 and 0<=x+dx<64]
    nb=[v for v in nb if v>0 and not (y<=v<=L)]
    return max(set(nb),key=nb.count) if nb else Dk

# ---- zone poten (rij 0-9) ----
zet(32,6,0,'poten','kier tussen de poten (model achtergrond x31,6-32,3 y3,6-7,3; mediaan 225)')
zet(32,7,Dk,'poten','onder de kier is het model donker (mediaan 26)')
# voeten en poten: tint op de modelmediaan (grijze tenen/linkerrand 45-60 -> E, zwart 20-45 -> D, < 20 -> K)
for yy in range(0,9):
    for x in range(27,36):
        if o[yy,x]==0 or (y<=o[yy,x]<=L) or (x,yy)==(32,7): continue
        l=LUM[yy,x]; v=E if l>=45 else (Dk if l>=20 else K)
        zet(x,yy,v,'poten','tint op modelmediaan %d'%l)
zet(35,7,y,'poten','begin gele rand rechts (model mediaan 129, geel) op de rand: donkergeel',True)
zet(35,8,y,'poten','gele rand (model mediaan 91) op de rand: donkergeel',True)
# tenen en lichte linkerrand van de poten (model grijs 46-57) beschermd, anders vallen ze als vlakje < 3 px weg
for p in [(28,1),(29,1),(33,1),(32,2),(30,6),(30,7),(33,6),(33,7),(33,8)]:
    zet(p[0],p[1],E,'poten','grijze teen/poot-rand (model mediaan %d)'%LUM[p[1],p[0]],True)
zet(31,9,B,'poten','bovenkant witte ovaal (model mediaan 173)')

# ---- zone rechter gele rand (rij 9-36): 1 px geel op de gemeten modellijn, rand erbuiten zwart ----
RECHTS={9:35.2,10:35.7,11:36.2,12:36.8,13:37.5,14:38.1,15:38.7,16:39.2,17:39.7,18:40.4,19:40.8,20:41.3,21:41.6,22:41.9,23:42.3,
        24:42.5,25:42.7,26:42.9,27:43.2,28:43.2,29:43.4,30:43.5,31:43.3,32:43.2,33:43.0,34:42.8,35:42.5}
for yy,c in RECHTS.items():
    e=max(np.where(o[yy]>0)[0])
    s=min(int(round(c)),e-1)
    for x in range(30,e+1):
        if x==e: zet(x,yy,K,'rechterrand','omlijning buiten de gele rand (model: zwart buiten geel)')
        elif x>=s: zet(x,yy,L if yy<=20 else (Y if yy<=30 else y),'rechterrand','gele rand op modellijn %.1f'%c,True)
        elif y<=o[yy,x]<=L: zet(x,yy,beste_niet_geel(x,yy),'rechterrand','geel naast de modellijn')
# ---- zone linker gele lijnen: A (vleugelpunt -> splitsing), A' (splitsing -> hals), B (splitsing -> links omlaag) ----
A=[(21.0,18),(21.0,19),(21.5,20),(21.6,21),(22.1,22),(22.6,23),(23.1,24),(23.7,25),(24.3,26),(25.6,27),(26.7,28),(27.9,29),(28.6,30)]
A2=[(28.6,30),(29.1,30.4),(30.3,31),(31.4,32),(32.2,33),(33.4,34),(34.2,35),(34.8,36),(35.2,37),(35.6,38),(36.0,39),(36.0,40)]
Bl=[(28.6,30),(26.8,30.4),(25.8,31),(25.2,32),(24.3,33),(23.8,34),(23.2,35),(23.1,36)]
op=set(lijn(A))|set(lijn(A2))|set(lijn(Bl))|{(36,41),(37,41),(38,41)}   # hals: kaal (model 36,0-38,4)
op={p for p in op if o[p[1],p[0]]>0}
for yy in range(17,42):
    for x in range(18,40):
        if (x,yy) in op:
            v=L if yy<=24 else Y
            if (x,yy) in set(lijn(Bl)) and yy>30: v=Y
            if yy>=37: v=Y
            zet(x,yy,v,'linkerlijnen','gele lijn op modellijn',True)
        elif y<=o[yy,x]<=L: zet(x,yy,beste_niet_geel(x,yy),'linkerlijnen','geel naast de modellijn')
np.save(D+'sprite_r1/tussen/op.npy',np.array(sorted(op)))

# ---- zone vouwlijn: zwarte binnenlijn van de ovaal schuin naar rechtsonder (model: zwart < 16 per blok, middens) ----
VOUW=[(29,17),(30.5,18),(32,19),(33,20),(34,21),(35,22),(35.4,23),(36,24),(36.5,25),(37,26),(38,27),(38.2,28),(38.6,29),(39,30),
      (39,31),(39,32),(39,33),(39,34),(39,35),(39.2,36)]
vouw=set(lijn(VOUW))
for (x,yy) in vouw:
    if o[yy,x] in (Dk,E,Gl,K): zet(x,yy,K,'vouwlijn','vouwlijn op modellijn',True)
for yy in range(28,37):
    for x in range(38,42):
        if o[yy,x]==K and (x,yy) not in vouw and not BESCHERMD[yy,x] and x<max(np.where(o[yy]>0)[0])-1:
            zet(x,yy,Dk,'vouwlijn','zwart naast de vouwlijn (model: lijn op x39)')
# ---- zone gezicht (rij 38-49) ----
# ogen: modelzwart per spritepixel gemeten (mediaan < 60), glans = lichtste modelpixel in de pupil (onderhoek, model)
OOG_NABIJ=[(28,44),(29,44),(27,45),(28,45),(29,45),(30,45),(27,46),(29,46),(30,46),(29,47)]
OOG_VER=[(22,44),(21,45),(22,45),(21,46),(22,47)]
for p in OOG_NABIJ+OOG_VER: zet(p[0],p[1],K,'gezicht','oog (model zwart)',True)
zet(28,46,W,'gezicht','glans nabije oog (model x28,5-29,0 y46,3-46,8)',True)
zet(22,46,W,'gezicht','glans verre oog (model x22,5 y46,3)',True)
# mond: dunne zwarte modellijn x23,5-28,9 op rij 39 met haakje op 28,40
for x in (24,25,26,27): zet(x,39,M,'gezicht','mondlijn (model p10 < 10)',True)
zet(28,40,M,'gezicht','mondhaakje (model p10 18)',True)
zet(23,39,B,'gezicht','mondlijn begint pas bij x23,5 (model mediaan 115)')
# neus (gele vlek x22,6-25,2 y41,25-42,5)
zet(24,41,L,'gezicht','gele snuitvlek (model 0,51)',True); zet(23,42,Y,'gezicht','gele snuitvlek (model 0,38)',True); zet(24,42,Y,'gezicht','gele snuitvlek (model 0,41)',True)
OOGSET=set(OOG_NABIJ+OOG_VER)|{(28,46),(22,46)}
# masker: cellen met modelmediaan 85-170 binnen het masker; toon naar modelhelderheid
MASKER={42:[20,21,28,29,30,31],43:[20,21,22,26,27,28,29,30,31,32],44:[20,21,23,24,25,26,27,30,31,32],45:[20,23,24,25,26,31,32,33],
        46:[23,24,25,26,31,32,33],47:[21,22,23,24,25,26,27,28,30,31,32,33],48:[21,22,23,27,28,29,30,31,32,33],49:[29,30,31]}
MSET={(x,yy) for yy,xs in MASKER.items() for x in xs}-OOGSET
for (x,yy) in MSET:
    # model: egale staalblauwe vlek met een donkere omlijning rondom. Omlijning M = maskerpixel met een 4-buur buiten masker/oog;
    # opvulling N; lichte bovenrand O waar de pixel direct onder de omlijning ligt en het model daar licht is (>= 148).
    def binnen(p): return p in MSET or p in OOGSET
    rand_=any(not binnen((x+dx,yy+dy)) for dx,dy in ((1,0),(-1,0),(0,1),(0,-1)))
    l=LUM[yy,x]; v=M if rand_ else N
    if not rand_ and l>=148 and (x,yy-1) in MSET and not binnen((x,yy-2)): v=O
    zet(x,yy,v,'gezicht','masker (omlijning rondom zoals het model), modelmediaan %d'%l,True)
# rest van de kop (wit/wangplukken/linkerplukken): dichtstbijzijnde tint op de modelmediaan
OOG=set(OOG_NABIJ+OOG_VER)|{(28,46),(22,46)}
for yy in range(38,49):
    for x in range(19,39):
        if o[yy,x]==0 or BESCHERMD[yy,x] or (x,yy) in OOG: continue
        if not (o[yy,x] in (B,W,w,M,N,O)): continue
        if yy<=41 and x>=34: continue          # vleugel/hals rechtsboven
        l=LUM[yy,x]; v=W if l>=225 else (B if l>=185 else (O if l>=148 else (N if l>=115 else M)))
        zet(x,yy,v,'gezicht','wit/plukken, modelmediaan %d'%l)
# ---- zone kruin/voorhoofd (rij 48-52) ----
zet(21,18,K,'linkerlijnen','punt van de vleugel: zwarte omlijning om het begin van de lijn (model)')
zet(25,49,L,'kruin','gele voorhoofdstreep (model 0,88)',True); zet(25,50,Y,'kruin','gele voorhoofdstreep (model 0,79)',True)
zet(26,50,Y,'kruin','gele voorhoofdstreep (model 0,87)',True); zet(26,51,y,'kruin','gele voorhoofdstreep (model 0,50)',True)
zet(27,51,K,'kruin','eind streep op de rand -> omlijning (model: zwarte rand rond de streep)')
for x in (24,25,26): zet(x,48,W,'kruin','wit voorhoofd (model mediaan 236-242)')
# ---- zone oren (rij 49-63): lichte rand aan de linkerkant van beide oren (model 60-140 grijs) ----
for p in [(19,57),(19,58),(19,59),(19,60)]: zet(p[0],p[1],E,'oren','grijze rand verre oor (model mediaan 100-106)',True)
for p in [(31,52),(31,53),(31,54),(32,55),(32,56),(33,57)]: zet(p[0],p[1],E,'oren','grijze rand nabije oor (model mediaan 54-137)',True)
# ---- gezicht: linkerlob van het masker (x20-22) en wangplukken ----
zet(36,42,M,'gezicht','lijntje tussen de wangplukken (model mediaan 93)',True)
zet(26,44,N,'gezicht','losse lichte maskerpixel onder de omlijning -> opvulling',True)
zet(21,43,N,'gezicht','losse lichte maskerpixel in de linkerlob -> opvulling',True)
np.save(D+'sprite_r1/tussen/beschermd.npy',BESCHERMD)
palet.opslaan(o,D+'sprite_r1/tussen/a0_pre.png')
import pickle; pickle.dump(LOG,open(D+'sprite_r1/tussen/log1.pkl','wb'))
from collections import Counter
print(Counter(z for z,*_ in LOG)); print('totaal',len(LOG))
