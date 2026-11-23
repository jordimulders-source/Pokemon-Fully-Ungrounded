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
