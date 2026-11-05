"""Controle kleurronde 2: PNG-modus/transparantie, kleuren, pixels, open randen, losse pixels, gaatjes."""
import sys
from PIL import Image
D='/home/user/Pokemon-Fully-Ungrounded/docs/concept/sprites/salticonda/kleur2/'
CH='.OKhedcbafgqrst'
for k in sys.argv[1:] or ['A','B']:
    b=Image.open(D+'salticonda_%s.png'%k); B=b.load()
    S={(x,y) for x in range(64) for y in range(64) if B[x,y]!=0}
    openr=[(x,y,CH[B[x,y]]) for (x,y) in S if any(q not in S for q in [(x+1,y),(x-1,y),(x,y+1),(x,y-1)]) and CH[B[x,y]] not in 'OKhst']
    lone=[]
    for (x,y) in S:
        c=B[x,y]; n=[B[q] for q in [(x+dx,y+dy) for dx in (-1,0,1) for dy in (-1,0,1) if dx or dy] if q in S]
        if n and all(v!=c for v in n): lone.append((x,y,CH[c]))
    holes=[(x,y) for x in range(1,63) for y in range(1,63) if (x,y) not in S and sum((x+dx,y+dy) in S for dx,dy in((1,0),(-1,0),(0,1),(0,-1)))>=3]
    xs=[p[0] for p in S]; ys=[p[1] for p in S]
    print(k,len(S),'px  box %dx%d'%(max(xs)-min(xs)+1,max(ys)-min(ys)+1),'| modus',b.mode,'transp',b.info.get('transparency'),
          '| kleuren',len({B[p] for p in S}),'| open randen',openr,'| gaatjes',holes,'\n  losse pixels',len(lone),sorted(lone,key=lambda t:(t[1],t[0])))
