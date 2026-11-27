import json,numpy as np
from soorten import BOUW
from hand import H
A=[r for r in json.load(open('auto.json')) if r['icon']=='gba']
def q(a):
    a=np.array([x for x in a if x is not None],float)
    if len(a)==0: return '-'
    return '%.2f (%.2f–%.2f) n%d'%(np.median(a),*np.percentile(a,[25,75]),len(a))
for b,L in BOUW.items():
    R=[r for r in A if r['bouw']==b]
    print('##',b)
    print(' S',q([r['S'] for r in R]),' Sw/S',q([r['Sw']/r['S'] for r in R]),' ih',q([r['ih'] for r in R]),' iw',q([r['iw'] for r in R]),' area',q([r['area_rel'] for r in R]), 'iou',q([r['iou'] for r in R]))
    hs=[H[s] for s in L]
    print(' pose',{p:sum(1 for h in hs if h['pose']==p) for p in ('zelfde','wissel','spiegel')})
    for k in ('kop','lijf','uitsteeksel','vleugel'):
        print(' ',k,'b',q([h[k][0] for h in hs if k in h]),'h',q([h[k][1] for h in hs if k in h]))
    print('  share f',q([h['share'][0] for h in hs if 'share' in h]),'i',q([h['share'][1] for h in hs if 'share' in h]),'ratio',q([h['share'][1]/h['share'][0] for h in hs if 'share' in h]))
    for k in ('dun','poot','oog'): print(' ',k,q([h[k] for h in hs if k in h]))
# alle
hs=list(H.values())
print('ALLE kop b',q([h['kop'][0] for h in hs if 'kop' in h]),'h',q([h['kop'][1] for h in hs if 'kop' in h]))
print('ALLE share ratio',q([h['share'][1]/h['share'][0] for h in hs if 'share' in h]),'i',q([h['share'][1] for h in hs if 'share' in h]))
print('ALLE dun',q([h['dun'] for h in hs if 'dun' in h]))
fh=np.array([r['fh'] for r in A]);ih=np.array([r['ih'] for r in A]);b,a=np.polyfit(fh,ih,1);print('ih = %.1f + %.3f*fh'%(a,b),'rest',np.std(ih-(a+b*fh)))
for lo,hi in((0,30),(30,40),(40,50),(50,58),(58,65)):
    m=(fh>=lo)&(fh<hi); print(lo,hi,m.sum(),np.median(ih[m]) if m.any() else '-')
print('iw max',max(r['iw'] for r in A),'ih max',max(r['ih'] for r in A))
print('ncol',q([r['ncol_i'] for r in A]),'front',q([r['ncol_f'] for r in A]))
print('edge top',q([r['edge_top'] for r in A]),'bot',q([r['edge_bot'] for r in A]))
w=[r for r in A if H[r['sp']]['pose']!='zelfde']; z=[r for r in A if H[r['sp']]['pose']=='zelfde']
print('wissel iou',q([r['iou'] for r in w]),'asp_f',q([r['asp_f'] for r in w]),'S',q([r['S'] for r in w]),'fh',q([r['fh'] for r in w]))
print('zelfde iou',q([r['iou'] for r in z]),'asp_f',q([r['asp_f'] for r in z]),'S',q([r['S'] for r in z]),'fh',q([r['fh'] for r in z]))
print('fill f',q([r['fill_f'] for r in w]),q([r['fill_f'] for r in z]))
