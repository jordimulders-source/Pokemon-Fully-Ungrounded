# Ronde 11: B6b (r10) opschonen. Vorm en manier blijven; alleen:
# 1 nekbovenlijn als vloeiende boog (K = donkerste eigen lijftint, zoals de kinlijn van de kop), halsstrook 1 px meegebogen
#   (2 px breed), randen van franje/nekmanen langs de halsstrook mee; 2 nekvolume: L-band onder de bovenlijn zoals de flank
#   van r6 (L onder de ruglijn), geen losse L-vlek; 3 netheid. Buiten manen+nek+halsstrook: diff 0.
import json, sys, r8lib as L, r10, vel8
from scipy import ndimage as nd
import numpy as np
v,B=r10.bouw(6,'b'); B=vel8.met_oog(B); B6B=[list(r) for r in B]; g=[r[:] for r in B6B]
H,W=len(g),len(g[0]); LOG={}
def put(x,y,c,why):
    if g[y][x]!=c: g[y][x]=c
    LOG[(x,y)]=why
# ---- vormen
FR={29:(9,11),30:(9,12),31:(9,13),32:(9,13),33:(8,13),34:(8,14),35:(8,14),36:(9,14),37:(10,13),38:(11,12)}   # keelfranje
HA={28:(13,14),29:(12,14),30:(13,14),31:(14,15),32:(14,15),33:(14,15),34:(15,16),35:(15,16),36:(15,16),37:(16,17),38:(16,17),39:(17,18),40:(17,18)}
MANE=v.mask   # nekmanen + franje van B6b
REDGE={y:max(x for x,yy in MANE if yy==y and x>=15) for y in range(23,42) if any(yy==y and x>=15 for x,yy in MANE)}   # rechterrand nekmanen (B6b)
NM=set()
for y in range(23,42):
    if y not in REDGE: continue
    x0=HA[y][1]+1 if y in HA else min(x for x,yy in MANE if yy==y and x>=15)
    for x in range(x0,REDGE[y]+1):
        if (x,y) in MANE or y in HA: NM.add((x,y))
NM={p for p in NM if p in MANE or (p[0]>=HA.get(p[1],(0,0))[1]+1)}
FRS={(x,y) for y,(a,b) in FR.items() for x in range(a,b+1)}
HAS={(x,y) for y,(a,b) in HA.items() for x in range(a,b+1)}
# nek: bovenlijn als boog van achter de oren (21,26) naar de schoft (33,31): stappen 1,2,3,3,3 (steil bij de kop, vlak naar de rug)
TOP={21:26,22:27,23:27,24:28,25:28,26:28,27:29,28:29,29:29,30:30,31:30,32:30,33:31}
ZONE=L.ZONE|{(x,TOP[x]) for x in TOP}|HAS|FRS
oud=lambda x,y: B6B[y][x]
manenkleur=lambda x,y: oud(x,y) if oud(x,y) in 'lm' else None
def dichtste(x,y,S,pred):
    best=None
    for a,b in S:
        c=pred(a,b)
        if c and (best is None or (a-x)**2+(b-y)**2<best[0]): best=((a-x)**2+(b-y)**2,c)
    return best[1] if best else 'l'
# ---- 1 nek (rechts van de nekmanen, boven rij 42)
for x,t in TOP.items():
    for y in range(22,t):
        if (x,y) in ZONE and (x,y) not in NM: put(x,y,'.','lucht boven de nekboog')
    put(x,t,'K','nekboog: K (donkerste eigen lijftint, sterker dan D; zoals de kinlijn)')
for y in range(26,42):
    if y not in REDGE: continue
    for x in range(REDGE[y]+1,34):
        if x in TOP and y<=TOP[x]: continue
        if (x,y) not in ZONE or (x,y) in NM: continue
        if not (x in TOP or y>=31): continue
        if B6B[y][x] in 'W': continue
        if x==REDGE[y]+1: put(x,y,'D','slagschaduw naast de manen (Arcanine: lijf naast de kraag donker)'); continue
        d=y-TOP.get(x,31)
        if (d==1 and 23<=x<=33) or (d==2 and 25<=x<=31): put(x,y,'L','nek: L-band onder de bovenlijn, zoals de flank van r6 onder de ruglijn')
        elif B6B[y][x] in 'LMD' or B6B[y][x] in '0.': put(x,y,'M','nek: M (lijftint)')
# ---- 2 halsstrook (2 px M, 1 px meegebogen)
oudhals=set(L.HALS)
for x,y in HAS: put(x,y,'M','halsstrook (gebogen)')
# ---- 3 franje: vulling uit B6b-franje, omtrek per regel
FROLD={p for p in MANE if p[0]<=13 and 29<=p[1]<=38}
for x,y in FRS:
    put(x,y,dichtste(x,y,FROLD,manenkleur),'franje: vultint van de dichtstbijzijnde B6b-franjepixel')
# ---- nekmanen: vulling uit B6b, linkerrand d langs de halsstrook
for x,y in {p for p in NM if p[1]>=27}:
    if oud(x,y) not in 'lm': put(x,y,dichtste(x,y,MANE,manenkleur),'nekmanen: vultint dichtstbijzijnde B6b-manenpixel')
# oude manen/halsstrook-pixels die nu niets meer zijn: borst (lijf)
for x,y in (FROLD|oudhals|{p for p in MANE if p[0]<=18 and p[1]>=28})-FRS-HAS-NM:
    put(x,y,'M','borst/hals: lijftint M (manen/halsstrook schoof op)')
NM={p for p in NM if p[1]>=27}          # boven rij 27 (achter de kaak) blijft B6b
MN=FRS|NM
# omtrek manen: buur buiten de manen links/boven -> d, rechts/onder -> 0
ch=[]
MNX=MN|{p for p in MANE if p[1]<27}
for x,y in MN:
    bu=[(a,b) for a,b in((-1,0),(0,-1),(1,0),(0,1)) if (x+a,y+b) not in MNX and not (g[y+b][x+a] in '0K' and (x+a,y+b) not in LOG) and not (y+b<=28 and x+a<=14)]   # kop: manen lopen erachter door
    if not bu:
        if g[y][x] in 'd0': put(x,y,dichtste(x,y,MANE,manenkleur),'binnen: vultint')
        continue
    if (x,y) in NM and ((x-1,y) in HAS or (x,y-1) in HAS): c='d'            # nekmanen tegen de halsstrook: lichtkant
    elif any(a>0 or b>0 for a,b in bu): c='0'           # schaduwkant (rechts/onder): zwart
    else: c='d'
    ch.append((x,y,c))
for x,y,c in ch: put(x,y,c,'manenomtrek: lichtkant d, schaduwkant 0')
# borst: buitenrand 0, slagschaduw D direct onder franje/manen
for y in range(36,46):
    for x in range(6,24):
        if (x,y) in MN or (x,y) in HAS or (x,y) not in ZONE: continue
        if g[y][x] in 'LMD':
            if any(g[y+b][x+a]=='.' for a,b in((1,0),(-1,0),(0,1),(0,-1))): put(x,y,'0','borst: buitenlijn')
            elif any((x+a,y-1) in MN for a in(-1,0,1)): put(x,y,'D','borst: slagschaduw onder de manen')
# netheid: tintvlakjes < 3 px (L/M/D/l/m) in de zone -> meerderheid van de buren
for _ in range(2):
    for c in 'LMDlm':
        A=np.zeros((H,W),bool)
        for x,y in set(LOG)|MN:
            if g[y][x]==c: A[y,x]=True
        lab,n=nd.label(A,structure=np.ones((3,3)))
        for k in range(1,n+1):
            pts=np.argwhere(lab==k)
            if len(pts)<3:
                for y,x in pts:
                    nb=[g[y+b][x+a] for a,b in((1,0),(-1,0),(0,1),(0,-1)) if g[y+b][x+a] in ('LMD' if c in 'LMD' else 'lm') and g[y+b][x+a]!=c]
                    if nb: put(x,y,max(set(nb),key=nb.count),'netheid: tintvlakje < 3 px')
G=[''.join(r) for r in g]
if __name__=='__main__':
    L.toon(G,22,47,36)
