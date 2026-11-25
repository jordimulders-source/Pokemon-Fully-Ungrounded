# r22: 6 micro-varianten van de r20-V (basis = sprite_r20/bokser.npy). Plek en punt van de V blijven; alleen de
# genoemde pixels wisselen tussen V-tint 3 en de romptint uit ruw.npy (r20, zonder V).
import numpy as np, sys
sys.path.insert(0,'../sprite_r7'); from build import save
B=np.load('r20_basis.npy'); R=np.load('ruw.npy')
WEG=lambda *p: [(x,y,int(R[y,x])) for x,y in p]     # V-pixel terug naar romptint (ruw)
BIJ=lambda *p: [(x,y,3) for x,y in p]               # romppixel wordt V-tint 3
VAR={
 'v1_flank_recht': WEG((27,28),(28,30),(28,31)),                 # linkerflank 28 (rij 25-29) -> 29 (30-32) -> 30 (33): knik weg
 'v2_punt_lager':  BIJ((30,34)),                                  # punt 1 rij dieper
 'v3_punt_hoger':  WEG((30,33),(29,32)),                          # punt 1 rij hoger: rij 32 alleen x30
 'v4_boven_links': BIJ((27,25)),                                  # bovenrand links weer op x27 zoals r18
 'v5_rechts_extra':BIJ((34,26)),                                  # rechterflank 35->34->33 (rij 25-27) i.p.v. 35->33
 'v6_1en5':        WEG((27,28),(28,30),(28,31))+BIJ((34,26)),
}
for n,ch in VAR.items():
    a=B.copy()
    for x,y,v in ch:
        assert R[y,x] in (7,8), (n,x,y)
        a[y,x]=v
    d=[(int(x),int(y)) for y,x in zip(*np.where(a!=B))]
    print(n,len(d),'px:',d); save(a,'var/'+n)
# ---- 7-9 (Jordi: "dus de v kan niet recht naar beneden zijn", "we kijken er vanuit een driekwart hoek op"):
# bovenrand van de r18-V blijft (rij 25, x27..34), punt op rij 33 maar 1/2/3 px links van x30 (loodrecht onder het
# midden 30,5 van de bovenrand); flanken = rechte lijnen van de bovenhoeken naar de punt, gevuld zoals r18 (tint 3).
# Eerst de r20-V weg (romptint uit ruw), dan de nieuwe V, alleen op romppixels.
TOPL,TOPR,TOP,PY=27,34,25,33
def schuin(px):
    s=set()
    for y in range(TOP,PY+1):
        t=(y-TOP)/(PY-TOP)
        for x in range(round(TOPL+(px-TOPL)*t),round(TOPR+(px-TOPR)*t)+1): s.add((x,y))
    return s
oud={(int(x),int(y)) for y,x in zip(*np.where((B==3)&np.isin(R,(7,8)))) if x>=26}
for n,px in [('v7_as1',29),('v8_as2',28),('v9_as3',27)]:
    a=B.copy()
    for x,y in oud: a[y,x]=R[y,x]
    for x,y in schuin(px):
        if R[y,x] in(7,8): a[y,x]=3
    d=[(int(x),int(y)) for y,x in zip(*np.where(a!=B))]
    print(n,'punt',(px,PY),len(d),'px anders dan r20'); save(a,'var/'+n)
    for j in range(24,35): print('  %2d '%j+''.join(str(v) if v else '.' for v in a[j,22:38]))
