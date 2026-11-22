# r8 (herkeuring r7: FAIL op schaduw). Reeks r7 blijft; alleen herkleuren op het bevroren silhouet (alpha-diff 0, assert).
# Licht linksboven (Gen 3), mag van de modeltoon afwijken (Jordi: "het model is qua kleur niet leidend"). Coördinaten in de code (y,x).
import numpy as np, json
o=np.load('tango_r7.npy').copy(); r7=o.copy(); H,W=o.shape
_,O,D0,D1,D2,D3,D4,R1,R2,R3=range(10)
DONK=(D0,D1,D2,D3,D4)
log={}
def zet(y,x,v,k):
    if 0<=y<H and 0<=x<W and o[y,x]!=0 and o[y,x]!=v: o[y,x]=v; log[k]=log.get(k,0)+1
def tr(y,x): return not(0<=y<H and 0<=x<W) or o[y,x]==0
def licht_rand(y,x): return (tr(y-1,x) or tr(y,x-1)) and not (tr(y+1,x) or tr(y,x+1))
def boven(y,x):   # rij van de eerste dekkende pixel boven (y,x) in dezelfde kolom (bovenrand)
    t=y
    while t-1>=0 and o[t-1,x]!=0: t-=1
    return t
# ---- 1+2+8. linkervleugel (rij 25-38, kol 0-22) ----
LV=[(y,x) for y in range(25,39) for x in range(0,23) if o[y,x] in DONK]
for y,x in LV: zet(y,x,D3,'1_linkervleugel_hoofdtint_D3')
for y,x in LV:
    if licht_rand(y,x): zet(y,x,D4,'2_linkervleugel_bovenrand_D4')
    else:
        d=y-boven(y,x)
        if d==1 or (d==2 and 8<=x<=17): zet(y,x,D1,'1_linkervleugel_voorrand_D1')
for y,x in LV:     # onder-/achterrand: pixel direct boven of links van de zwarte onderlijn -> D4
    if o[y,x]==D3 and y>=34 and (o[y+1,x]==O or tr(y+1,x)): zet(y,x,D4,'1_linkervleugel_onderrand_D4')
for y in range(29,36):
    for x in range(18,23):
        if o[y,x] in (D3,D1) and not licht_rand(y,x) and y-boven(y,x)>=2: zet(y,x,D4,'1_linkervleugel_aanzet_D4')
# veerrijen: lijntje D4 met D1 erboven, >=3 px, langs de modelveerranden
for y,x in ((33,11),(33,12),(32,13),(32,14),(32,15)): zet(y,x,D4,'1_veerrij1_D4')
for y,x in ((32,11),(32,12),(31,13),(31,14),(31,15)): zet(y,x,D1,'1_veerrij1_D1')
for y,x in ((36,5),(36,6),(36,7),(36,8),(36,9),(36,10),(36,11)): zet(y,x,D4,'1_veerrij2_D4')
for y,x in ((35,4),(35,5),(35,6),(35,7),(35,8),(35,9),(35,10),(35,11)): zet(y,x,D1,'1_veerrij2_D1')
# ---- 1+2+5. rechtervleugel (rij 3-28, kol 43-63 en rij 19-28 kol 38-63) ----
def rv(y,x): return (y<=18 and x>=43 and not (y<=18 and x<=46 and y>=5 and x<=45)) or (19<=y<=28 and x>=41)
RV=[(y,x) for y in range(3,29) for x in range(36,64) if rv(y,x) and o[y,x] in DONK]
for y,x in RV: zet(y,x,D3,'1_rechtervleugel_hoofdtint_D3')
for y,x in RV:
    if licht_rand(y,x): zet(y,x,D4,'2_rechtervleugel_bovenrand_D4')
    elif y-boven(y,x)==1: zet(y,x,D1,'1_rechtervleugel_voorrand_D1')
for y,x in RV:   # sikkel langs onder- en achterrand (pixel boven/links van zwart of leeg aan de onder/rechterkant), 1 px; 2 px in het midden (rij 19-24)
    if o[y,x] in (D3,D1) and (o[y+1,x] in (O,0) or o[y,x+1] in (O,0)):
        zet(y,x,D4,'1_rechtervleugel_sikkel_D4')
        if 19<=y<=24 and o[y-1,x] in (D3,) : zet(y-1,x,D4,'1_rechtervleugel_sikkel_D4')
# veerrij bij de schouder (x44-52, y14-18): D1-rij op de curve van de bovenrand, 1 px D4 eronder; losse pixels -> vlaktint
for y,x in RV:
    if 44<=x<=52 and 14<=y<=19 and not licht_rand(y,x):
        d=y-boven(y,x)
        if d==1: zet(y,x,D1,'5_veerrij_schouder_D1')
        elif d==2: zet(y,x,D4,'5_veerrij_schouder_D4')
        elif o[y,x] in (D1,D4) and d>2: zet(y,x,D3,'5_losse_pixels_vlaktint')
# ---- 6. lichte vlek hals schaduwkant (x37-43, y20-22) -> D3
for y in range(20,23):
    for x in range(37,44):
        if o[y,x]==D1: zet(y,x,D3,'6_halsvlek_D3')
# ---- 3. jurk ----
for y in range(28,46):
    xs=[x for x in range(24,43) if o[y,x] in DONK]
    if not xs: continue
    for x in xs:
        if o[y,x] in (D1,D0) and not (y in (36,37) and x in (25,26)): zet(y,x,D3,'3_jurk_reset_D3')
    x0,x1=min(xs),max(xs)
    if y>=35:
        if licht_rand(y,x0) or tr(y,x0-1): zet(y,x0,D4,'2_jurk_linkerrand_D4'); s=x0+1
        else: s=x0
        bw={35:2,36:3,37:3,38:3,39:3,40:2,41:2,42:1,43:1,44:1,45:1}.get(y,0)
        for x in range(s,s+bw):
            if o[y,x]==D3: zet(y,x,D1,'3_jurk_lichtband_D1')
    sw={28:1,29:1,30:1,31:1,32:1,33:1,34:2,35:2,36:2,37:2,38:3,39:3,40:3,41:3,42:3,43:3,44:2,45:2}.get(y,0)
    for x in range(x1-sw+1,x1+1):
        if o[y,x] in (D3,D1): zet(y,x,D4,'3_jurk_sikkel_D4')
# middenplooi: D1 links, 1 px D4 rechts (kol 34), taps boven (rij 40), breder onder
PL={40:(33,33),41:(32,33),42:(32,33),43:(31,33),44:(31,33),45:(30,33)}
for y,(a,b) in PL.items():
    for x in range(a,b+1): zet(y,x,D1,'3_plooi_D1')
    zet(y,34,D4,'3_plooi_D4')
    if y>=43 and o[y,35] in DONK: zet(y,35,D4,'3_plooi_D4')
# ---- 4. torso (x24-37, y24-34) ----
for y in range(24,35):
    xs=[x for x in range(23,39) if o[y,x] in DONK]
    if not xs: continue
    x1=max(xs)
    if y<=27: zet(y,x1,D4,'4_torso_sikkel_tot_y24')
BOL={26:(23,25),27:(24,29),28:(24,28),29:(24,27),30:(24,26),31:(24,26),32:(24,26),33:(24,25),34:(24,25)}
for y,(a,b) in BOL.items():
    for x in range(a,b+1):
        if o[y,x]==D3: zet(y,x,D1,'4_bolling_D1')
for y,x in ((26,26),(26,27),(26,28),(26,29),(25,30),(25,31),(25,32),(25,33)): zet(y,x,D4,'4_schaduw_onder_V_D4')
# ---- 7. V-lijn taps ----
for y,x in ((22,23),(19,36),(19,37),(20,35)): zet(y,x,D3,'7_V_taps_D3')
zet(19,35,D4,'7_V_taps_D4')
assert ((o>0)==(r7>0)).all()
np.save('tango_r8.npy',o); log['px_veranderd_totaal']=int((o!=r7).sum()); json.dump(log,open('log_r8.json','w'),indent=0)
for k,v in sorted(log.items()): print(k,v)
