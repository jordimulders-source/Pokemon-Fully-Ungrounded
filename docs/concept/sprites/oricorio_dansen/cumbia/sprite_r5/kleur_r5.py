# r5 (eindkeuring r4: kleur/lijn, vorm bevroren). Werkt op r4 (cumbia_kls.npy uit build2.py) -> cumbia_r5.npy.
# Elke nieuwe tint staat op een plek waar de toonkaart van het model (toon.py) dezelfde richting geeft. Oog, snavel, poten, bloem onaangeroerd.
import numpy as np, json
from toon import model_L
o=np.load('cumbia_kls.npy').copy(); r4=o.copy(); H,W=o.shape
O,B1,B2,B3,N,M,L1,L2,P,K1,K2,R,G,Y,HL=range(1,16)
log={}
def nb(y,x):
    return [(y+dy,x+dx) for dy,dx in((-1,0),(1,0),(0,-1),(0,1)) if 0<=y+dy<H and 0<=x+dx<W]
def tr(y,x): return not(0<=y<H and 0<=x<W) or o[y,x]==0
BEVROREN=set()
for y in range(13,23):            # oog + snavel
    for x in range(16,34):
        if r4[y,x] in (O,K1,K2,15) or (y>=14 and y<=18 and 25<=x<=31): BEVROREN.add((y,x))
for y in range(52,64):
    for x in range(64):
        if r4[y,x] in (K1,K2) or y>=55: BEVROREN.add((y,x))
def zet(y,x,v,k):
    if (y,x) in BEVROREN or o[y,x]==v: return
    o[y,x]=v; log[k]=log.get(k,0)+1
# 0. glimpje: W (15) -> P (9); P wordt puur wit in het palet (punt 5: 9/15 samen). Plek 15 wordt het hooglicht van het lijf.
for y,x in zip(*np.where(r4==15)): o[y,x]=P; log['5_W_naar_P']=log.get('5_W_naar_P',0)+1
# 1a. sikkel B2 rechts aan de kop (x29-33, y10-22): B1-pixel met binnen 2 px rechts B3/omlijning en modeltoon onder de mediaan
for y in range(10,23):
    for x in range(29,34):
        if o[y,x]==B1 and any(o[y,x+d] in (B3,O) for d in (1,2) if x+d<W) and model_L(y,x)<130: zet(y,x,B2,'1a_sikkel_kop_rechts')
# 1b. onder kaak/snavel (y19-22, x19-27): B1 met modeltoon < 130 die aan B3 grenst
for y in range(19,23):
    for x in range(19,28):
        if o[y,x]==B1 and any(o[a,b]==B3 for a,b in nb(y,x)) and model_L(y,x)<135: zet(y,x,B2,'1b_onder_kaak')
# 1c. overgang hals/lijf (y24-28): B1 boven of links van B3 -> B2 (1 px)
for y in range(24,29):
    for x in range(14,46):
        if o[y,x]==B1 and (o[y+1,x]==B3 or o[y,x+1]==B3) and model_L(y,x)<138: zet(y,x,B2,'1c_hals_lijf')
# 1d. hooglicht: kruin en borstbolling als één klein vlekje (3 px): start op de lichtste modelpixel, groei naar de lichtste buren
for (y0,y1,x0,x1,k) in ((10,14,20,26,'1d_hooglicht_kruin'),(22,25,21,28,'1d_hooglicht_borst')):
    cand={(y,x):model_L(y,x) for y in range(y0,y1) for x in range(x0,x1) if o[y,x]==B1 and all(o[a,b] in (B1,15) for a,b in nb(y,x))}
    if not cand: continue
    sel=[max(cand,key=cand.get)]
    while len(sel)<3:
        rand=[p for q in sel for p in nb(*q) if p in cand and p not in sel]
        if not rand: break
        sel.append(max(rand,key=cand.get))
    for y,x in sel: zet(y,x,15,k)
# 2a. lijf/vleugels: bovenrand van het B3-vlak aan de lichtkant (y26-30) -> B2 waar erboven B1 staat
for y in range(26,31):
    for x in range(8,46):
        if o[y,x]==B3 and o[y-1,x] in (B1,15) : zet(y,x,B2,'2a_bovenrand_B2')
# 2b. sikkel N langs onder- en rechterkant van het lijfvlak (y29-35): B3 met omlijning/naad eronder of rechts
for y in range(29,36):
    for x in range(14,45):
        if o[y,x]==B3 and (o[y+1,x]==O or o[y,x+1]==O) and not tr(y+1,x): zet(y,x,N,'2b_sikkel_N')
# 3. linkerrand rok: y30-45 buitenrand (transparant links of boven) -> N; y46-48 -> zwart
for y in range(30,49):
    for x in range(0,10):
        if o[y,x] in (O,N) and (tr(y,x-1) or tr(y-1,x)) and not tr(y,x):
            zet(y,x,N if y<=45 else O,'3_linkerrand')
# 4. binnenlijnen aan de licht-/bovenkant -> N (zwart blijft waar de lijn in de schaduw valt)
ZONES=[(31,31,35,41),(34,35,16,28),(28,31,7,14),(41,41,22,23),(46,48,15,17),(46,48,34,41)]
for (y0,y1,x0,x1) in ZONES:
    for y in range(y0,y1+1):
        for x in range(x0,x1+1):
            if o[y,x]==O and not any(tr(a,b) for a,b in nb(y,x)): zet(y,x,N,'4_binnenlijn_N')
# 5. rok iets cyaner (palet) + L2 laten vervallen waar hij banden vormt: L2 -> L1 (3 blauw + wit)
# (L2 -> L1 geprobeerd: rok werd vlak en donkerder; L2 blijft, rok wordt alleen cyaner via het palet)
# 6. onderste ruche (x12-40, y48-53): per kolomstuk bovenste 1 px M, rest N (onderrand donker)
for x in range(12,41):
    y=48
    while y<=53:
        if o[y,x] in (N,M):
            y0=y
            while y<=53 and o[y,x] in (N,M): y+=1
            for yy in range(y0,y):
                zet(yy,x,M if yy==y0 else N,'6_onderste_ruche')
        else: y+=1
np.save('cumbia_r5.npy',o); json.dump(log,open('log_r5.json','w'),indent=0); print(log)
print('zwart binnen de vorm: %.0f%% -> %.0f%%'%tuple(100*sum(1 for y in range(H) for x in range(W) if a[y,x]==O and not any(not(0<=yy<H and 0<=xx<W) or a[yy,xx]==0 for yy,xx in [(y-1,x),(y+1,x),(y,x-1),(y,x+1)]))/max(1,(a==O).sum()) for a in (r4,o)))
