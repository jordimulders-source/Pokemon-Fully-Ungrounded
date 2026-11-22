"""Rekent uit punten.py de verhoudingen front -> icoon uit en schrijft data/metingen.csv, data/punten.json en data/samenvatting.json.
python3 analyse.py"""
import json,os,csv,numpy as np
from punten import P
from laad import front,icoon
os.makedirs('data',exist_ok=True)
def hoogte(a):
    ys,xs=np.nonzero(a[...,3]); return ys.max()-ys.min()+1, xs.max()-xs.min()+1
def maten(d):
    k=d['kop']; m={}
    m['kop_b']=k[2]-k[0]+1; m['kop_h']=k[3]-k[1]+1
    m['oor']=k[1]-d['oor'] if d['oor'] is not None and k[1]-d['oor']>0 else None
    o=d['oog']; m['oog']=(o[2]*o[3])**.5
    m['snuit']=o[0]-k[0]+.5
    m['lijf']=d['romp'][1]-d['romp'][0]+1 if d['romp'] else None
    m['vp']=d['vp']-d['buik'] if d['vp'] is not None and d['buik'] is not None else None
    m['ap']=d['ap']-d['buik'] if d['ap'] is not None and d['buik'] is not None else None
    s=d['staart']; m['staart']=max(s[2]-s[0]+1,s[3]-s[1]+1) if s else None
    m['oog_h']=(o[0]-k[0])/(k[2]-k[0]); m['oog_v']=(o[1]-k[1])/(k[3]-k[1])
    return m
rows=[]
for sp,d in P.items():
    Hf,Wf=hoogte(front(sp)); Hi,Wi=hoogte(icoon(sp)); S=Hi/Hf
    mf,mi=maten(d['f']),maten(d['i'])
    r=dict(soort=sp,groep=('vogel' if d.get('vogel') else 'tweevoeter' if d.get('tweevoeter') else 'viervoeter'),
           frontaal=int(bool(d.get('frontaal'))),posewissel=int(bool(d.get('posewissel'))),
           front_h=Hf,front_b=Wf,icoon_h=Hi,icoon_b=Wi,schaal=round(S,3),schaal_b=round(Wi/Wf,3))
    for k in ['kop_b','kop_h','oor','oog','snuit','lijf','vp','ap','staart']:
        r[k+'_f']=mf[k]; r[k+'_i']=mi[k]
        ok=mf[k] and mi[k] and not (k=='snuit' and d.get('frontaal'))
        r['rel_'+k]=round(mi[k]/mf[k]/S,3) if ok else None
    # kop t.o.v. lijf (icoon tegen front), kop als deel van de figuurhoogte
    r['kop_aandeel_f']=round(mf['kop_h']/Hf,3); r['kop_aandeel_i']=round(mi['kop_h']/Hi,3)
    r['kop_lijf_f']=round(mf['kop_b']/mf['lijf'],3) if mf['lijf'] else None; r['kop_lijf_i']=round(mi['kop_b']/mi['lijf'],3) if mi['lijf'] else None
    r['rel_kop_lijf']=round(r['kop_lijf_i']/r['kop_lijf_f'],3) if mf['lijf'] and mi['lijf'] else None
    for k in ['oog_h','oog_v']:
        r[k+'_f']=round(mf[k],3); r[k+'_i']=round(mi[k],3); r['d_'+k]=round(mi[k]-mf[k],3)
    if d.get('frontaal'): r['d_oog_h']=None
    r['pose']=d['pose']; rows.append(r)
with open('data/metingen.csv','w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
json.dump(P,open('data/punten.json','w'),indent=1)
def stat(vals):
    v=np.array([x for x in vals if x is not None],float)
    if len(v)==0: return None
    return dict(n=len(v),gem=round(v.mean(),3),med=round(float(np.median(v)),3),p25=round(float(np.percentile(v,25)),3),p75=round(float(np.percentile(v,75)),3),min=round(v.min(),3),max=round(v.max(),3))
keys=['schaal','schaal_b']+['rel_'+k for k in ['kop_b','kop_h','oor','oog','snuit','lijf','vp','ap','staart','kop_lijf']]+['kop_aandeel_f','kop_aandeel_i','oog_h_f','oog_h_i','d_oog_h','oog_v_f','oog_v_i','d_oog_v']
groepen={'alle':rows,'viervoeters':[r for r in rows if r['groep']=='viervoeter'],
         'zijaanzicht (3/4 of profiel, geen posewissel)':[r for r in rows if not r['frontaal'] and not r['posewissel'] and r['groep']=='viervoeter'],
         'frontaal':[r for r in rows if r['frontaal']]}
S={g:{k:stat([r[k] for r in R]) for k in keys} for g,R in groepen.items()}
json.dump(S,open('data/samenvatting.json','w'),indent=1)
for g in S:
    print('==',g,len(groepen[g]))
    for k in keys:
        s=S[g][k]
        if s: print(f"{k:16s} n={s['n']:2d} gem {s['gem']:.2f} med {s['med']:.2f}  p25-p75 {s['p25']:.2f}-{s['p75']:.2f}  min-max {s['min']:.2f}-{s['max']:.2f}")
