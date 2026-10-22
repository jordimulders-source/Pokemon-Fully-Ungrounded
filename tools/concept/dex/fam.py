import json,re
D=json.load(open('sp.json')); sp=D['sp']; order=D['order']
REG=('_ALOLA','_GALAR','_HISUI','_PALDEA','_HOENN')
def base_ok(k):
    v=sp[k]; nat=v.get('nat','')
    if not nat: return False
    return k=='SPECIES_'+nat[len('NATIONAL_DEX_'):]
def reg(k): return any(r in k for r in REG) and 'GMAX' not in k and 'MEGA' not in k
# nodes: base species + regional forms + some notable forms
nodes=[k for k in order if base_ok(k) or reg(k)]
pre={}
for k in nodes:
    for e in sp[k]['evos']:
        t=e[2]
        if t in sp: pre.setdefault(t,[]).append(k)
# family root
def root(k,seen=None):
    seen=seen or set()
    if k in seen: return k
    seen.add(k)
    ps=[p for p in pre.get(k,[]) if p in nodes]
    # prefer same region pre
    if not ps: return k
    return root(ps[0],seen)
fams={}
for k in nodes:
    r=root(k)
    fams.setdefault(r,[]).append(k)
out=[]
for r,mem in fams.items():
    leg=any(sp[m]['legend'] for m in mem)
    s=' | '.join(f"{sp[m].get('name',m)}{'('+m.split('_')[-1].title()+')' if reg(m) else ''}:{'/'.join(sp[m].get('types',['?']))}" for m in mem)
    out.append((r,sp[r]['gen'],leg,s))
json.dump({r:fams[r] for r in fams},open('fams.json','w'))
with open('fams.txt','w') as f:
    for r,g,l,s in out: f.write(f"{g}{'L' if l else ' '} {r[8:]}: {s}\n")
print(len(out), sum(len(v) for v in fams.values()))
