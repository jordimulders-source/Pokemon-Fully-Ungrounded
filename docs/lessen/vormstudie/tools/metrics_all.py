import sys,re,glob,json
sys.path.insert(0,'.')
from lib import *
d=dex(); name2n={v:k for k,v in d.items()}
parent={}
for f in glob.glob(R+'src/data/pokemon/species_info/gen_*_families.h'):
    cur=None; inevo=False
    for l in open(f):
        m=re.match(r'\s*\[SPECIES_(\w+)\]\s*=',l)
        if m: cur=m.group(1).lower(); inevo=False
        if '.evolutions' in l: inevo=True
        if inevo:
            for t in re.findall(r'SPECIES_(\w+)\}',l):
                t=t.lower()
                if t in name2n and cur in name2n and t not in parent: parent[t]=cur
            if ')' in l and l.strip().endswith('),'): inevo=False
def stage(n):
    s=1
    while n in parent and s<4: n=parent[n]; s+=1
    return s
def final(n):
    return not any(p==n for p in parent.values())
rows=[]
for i,n in sorted(d.items()):
    for gba in ([True,False] if i<=386 else [False]):
        im=load(n,gba)
        if not im: continue
        m=metrics(im)
        if not m: continue
        m.update(n=n,dex=i,gba=gba,stage=stage(n),final=final(n),gen=1 if i<=151 else 2 if i<=251 else 3 if i<=386 else 4 if i<=493 else 5 if i<=649 else 6 if i<=721 else 7 if i<=809 else 8 if i<=905 else 9)
        rows.append(m)
json.dump(rows,open('metrics.json','w'))
print(len(rows))
import statistics as st
def summ(sel,lab):
    if not sel: return
    print(f"{lab:28s} n={len(sel):4d} A={st.median(r['A'] for r in sel):5.0f} h={st.median(r['h'] for r in sel):4.0f} w={st.median(r['w'] for r in sel):4.0f} fill={st.median(r['fill'] for r in sel):.2f} cx={st.median(r['cx'] for r in sel):+.3f} head={st.median(r['head'] for r in sel):+.3f} gl={st.median(r['y1'] for r in sel):.0f}")
g3=[r for r in rows if r['gba']]
new=[r for r in rows if not r['gba']]
for lab,sel in [('gen1-3 gba',g3),('gen4+ ',[r for r in new if r['dex']>386]),('gen1-3 newstyle',[r for r in new if r['dex']<=386])]:
    summ(sel,lab)
    for s in (1,2,3):
        summ([r for r in sel if r['stage']==s and not (s==1 and r['final'])],f'  stage{s} (in lijn)')
    summ([r for r in sel if r['stage']==1 and r['final']],'  losse soort')
