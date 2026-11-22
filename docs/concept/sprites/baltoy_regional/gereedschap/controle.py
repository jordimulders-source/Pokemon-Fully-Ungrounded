# Controle Gen 3-eisen op de sprite (tekst): kleuren, buitenlijn, losse vlakjes < 3 px per tint, losse zwarte pixels binnenin.
import sys
g=[r for r in open(sys.argv[1]).read().split()]; H,W=len(g),len(g[0])
at=lambda y,x: g[y][x] if 0<=y<H and 0<=x<W else '.'
print('kleuren (incl. transparant):',len(set(''.join(g))),sorted(set(''.join(g))))
rand=[(y,x,g[y][x]) for y in range(H) for x in range(W) if g[y][x]!='.' and any(at(y+a,x+b)=='.' for a,b in((1,0),(-1,0),(0,1),(0,-1)))]
fout=[(y,x,c) for y,x,c in rand if c not in 'KdDr']
print('buitenrand niet zwart/selout:',fout)
lichtzw=[(y,x) for y,x,c in rand if c in 'dr' and any(at(y+a,x+b)=='.' for a,b in((1,0),(0,1))) ]
print('selout aan de schaduwkant (rechts/onder transparant):',lichtzw)
seen=set(); klein=[]
for y in range(H):
    for x in range(W):
        c=g[y][x]
        if c in 'hlmRr' and (y,x) not in seen:
            st=[(y,x)]; seen.add((y,x)); cl=[]
            while st:
                p=st.pop(); cl.append(p)
                for a,b in((1,0),(-1,0),(0,1),(0,-1)):
                    q=(p[0]+a,p[1]+b)
                    if q not in seen and at(*q)==c: seen.add(q); st.append(q)
            if len(cl)<3: klein.append((c,cl))
print('tintvlakjes < 3 px:',len(klein)); [print('  ',c,cl) for c,cl in klein]
binnen=[(y,x) for y in range(H) for x in range(W) if g[y][x]=='K' and not any(at(y+a,x+b) in '.' for a in(-1,0,1) for b in(-1,0,1))]
print('zwart zonder contact met buiten (binnenlijn/losse):',binnen)
