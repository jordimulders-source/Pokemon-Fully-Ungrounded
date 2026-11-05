"""Controle kleurronde 1: alpha-diff met de silhouetten, open randen, losse pixels, kleurtelling."""
from PIL import Image
D='/home/user/Pokemon-Fully-Ungrounded/docs/concept/sprites/salticonda/'
CH='.OKhedcbafgqrst'
for k,src in [('A','silhouet1/variant_A.png'),('E','silhouet2/variant_E.png')]:
    a=Image.open(D+src); b=Image.open(D+'kleur1/salticonda_%s.png'%k)
    A=a.load(); B=b.load()
    diff=sum(1 for x in range(64) for y in range(64) if (A[x,y]!=0)!=(B[x,y]!=0))
    S={(x,y) for x in range(64) for y in range(64) if B[x,y]!=0}
    openr=[(x,y,CH[B[x,y]]) for (x,y) in S if any(q not in S for q in [(x+1,y),(x-1,y),(x,y+1),(x,y-1)]) and CH[B[x,y]] not in 'OKhst']
    lone=[]
    for (x,y) in S:
        c=B[x,y]; n=[B[q] for q in [(x+1,y),(x-1,y),(x,y+1),(x,y-1)] if q in S]
        if n and all(v!=c for v in n) and CH[c] not in 'OKhqrst': lone.append((x,y,CH[c]))
    print(k,'alpha-diff',diff,'| modus',b.mode,'transparantie',b.info.get('transparency'),'| kleuren',len(set(B[p] for p in S)),
          '| open randen',openr,'| losse pixels',len(lone),lone[:12])
