# Controle: kleurentelling, losse tintclusters (<3 px) per materiaalgroep, lichte pixels op de buitenrand, losse zwarte pixels
import sys, numpy as np
o=np.load(sys.argv[1] if len(sys.argv)>1 else 'r1.npy'); H,W=o.shape
print('kleuren (incl. transparant):',len(np.unique(o)), 'gebruikt:',sorted(set(o.ravel())))
grp={2:'lijf',3:'lijf',4:'lijf',5:'geel',6:'geel',7:'geel',8:'ijs',9:'ijs',10:'ijs',11:'ijs',12:'rood',13:'rood',14:'rood'}
seen=np.zeros_like(o,bool); klein=[]
for y in range(H):
    for x in range(W):
        v=o[y,x]
        if v not in grp or seen[y,x]: continue
        st=[(y,x)]; comp=[]
        while st:
            j,i=st.pop()
            if j<0 or i<0 or j>=H or i>=W or seen[j,i] or o[j,i]!=v: continue
            seen[j,i]=True; comp.append((i,j)); st+=[(j+1,i),(j-1,i),(j,i+1),(j,i-1)]
        if len(comp)<3: klein.append((v,comp))
print('clusters < 3 px:',len(klein))
for v,c in klein: print('  %x'%v,c)
rand=[(x,y,'%x'%o[y,x]) for y in range(H) for x in range(W) if o[y,x] in (5,8,9) and any((0<=y+dy<H and 0<=x+dx<W and o[y+dy,x+dx]==0) or not(0<=y+dy<H and 0<=x+dx<W) for dy,dx in((1,0),(-1,0),(0,1),(0,-1)))]
print('lichte pixels aan de buitenrand:',rand)
