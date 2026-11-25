# Controle: kleuren, buitenlijn (zwart vs selout), losse tintvlakjes <3 px, losse lijnpixels midden in een vlak
import sys, json
from collections import Counter
RN=sys.argv[1]; m=json.load(open(f'{RN}/grid.json')); g=m['grid']; H=len(g); W=len(g[0])
op=lambda x,y: 0<=x<W and 0<=y<H and g[y][x]!='.'
rand=[(x,y) for y in range(H) for x in range(W) if g[y][x]!='.' and any(not op(x+dx,y+dy) for dx,dy in((1,0),(-1,0),(0,1),(0,-1)))]
c=Counter(g[y][x] for x,y in rand); print('buitenrand:',dict(c),'zwart %.0f%%'%(100*c['0']/len(rand)))
print('licht op buitenrand:',[(x,y,g[y][x]) for x,y in rand if g[y][x] in 'LMCnhKJ'])
seen=set(); small=[]
for y in range(H):
    for x in range(W):
        if (x,y) in seen or g[y][x] in '.0': continue
        v=g[y][x]; st=[(x,y)]; seen.add((x,y)); cc=[]
        while st:
            a,b=st.pop(); cc.append((a,b))
            for dx,dy in((1,0),(-1,0),(0,1),(0,-1)):
                if op(a+dx,b+dy) and (a+dx,b+dy) not in seen and g[b+dy][a+dx]==v: seen.add((a+dx,b+dy)); st.append((a+dx,b+dy))
        if len(cc)<3: small.append((v,cc))
print('tintvlakjes <3 px:',len(small),[ (v,cc) for v,cc in small])
los=[(x,y) for y in range(H) for x in range(W) if g[y][x]=='0' and (x,y) not in rand and sum(g[y+dy][x+dx]=='0' for dx,dy in((1,0),(-1,0),(0,1),(0,-1),(1,1),(1,-1),(-1,1),(-1,-1)) if op(x+dx,y+dy))==0]
print('losse zwarte pixels binnenin:',los)
print('kleuren:',sorted(set(''.join(g))-{'.'}),len(set(''.join(g))))
