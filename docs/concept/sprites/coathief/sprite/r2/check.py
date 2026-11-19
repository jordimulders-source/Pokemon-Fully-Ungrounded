# Controle: tintvlakjes < 3 px (4-buren, zelfde index), losse omlijningspixels binnenin, kleurenaantal, helderheidsstappen.
import sys
R=[l.rstrip('\n') for l in open(sys.argv[1] if len(sys.argv)>1 else 'r1.txt')]
seen=set(); small=[]
for y in range(64):
  for x in range(64):
    c=R[y][x]
    if c in '01' or (x,y) in seen: continue
    st=[(x,y)]; comp=[]; seen.add((x,y))
    while st:
      p=st.pop(); comp.append(p)
      for dx,dy in [(1,0),(-1,0),(0,1),(0,-1)]:
        q=(p[0]+dx,p[1]+dy)
        if 0<=q[0]<64 and 0<=q[1]<64 and q not in seen and R[q[1]][q[0]]==c: seen.add(q); st.append(q)
    if len(comp)<3: small.append((c,comp))
print('vlakjes <3 px:',len(small))
for c,comp in small: print('  ',c,comp)
lone=[]
for y in range(1,63):
  for x in range(1,63):
    if R[y][x]!='1': continue
    n=[R[y+dy][x+dx] for dx,dy in [(1,0),(-1,0),(0,1),(0,-1),(1,1),(1,-1),(-1,1),(-1,-1)]]
    if '0' in n: continue
    if sum(v=='1' for v in n)==0: lone.append((x,y))
print('losse 1 binnenin:',lone)
print('indexen:',sorted(set(''.join(R))))
