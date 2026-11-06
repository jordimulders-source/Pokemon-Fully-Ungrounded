"""Controle potoo-sprite: open randen, losse pixels, tintclusters < 3 px (4-samenhangend), kleuren, maat.
Gebruik: python3 controle.py <raster.txt> [<vorig raster.txt>]"""
import sys
r=[l.rstrip('\n') for l in open(sys.argv[1])][:64]
P=[(x,y) for y in range(64) for x in range(64)]
LIJN=set('12E8')          # mogen op de buitenrand liggen (buitenlijn, selout, hoornhaak, oog)
VLAK=set('34567ABCD9F')   # vlaktinten voor de clustertoets (9 als holte/V-spleet ook)
def at(x,y): return r[y][x] if 0<=x<64 and 0<=y<64 else '.'
nb4=lambda x,y:[at(x+dx,y+dy) for dx,dy in ((1,0),(-1,0),(0,1),(0,-1))]
openr=[(x,y,r[y][x]) for x,y in P if r[y][x]!='.' and '.' in nb4(x,y) and r[y][x] not in LIJN]
los=[(x,y,r[y][x]) for x,y in P if r[y][x]!='.' and r[y][x] not in nb4(x,y) and r[y][x] in VLAK]
seen=set(); cl=[]
for x,y in P:
    c=r[y][x]
    if c not in VLAK or (x,y) in seen: continue
    st=[(x,y)]; comp=[]; seen.add((x,y))
    while st:
        a,b=st.pop(); comp.append((a,b))
        for dx,dy in ((1,0),(-1,0),(0,1),(0,-1)):
            p=(a+dx,b+dy)
            if p not in seen and at(*p)==c: seen.add(p); st.append(p)
    if len(comp)<3: cl.append((c,sorted(comp)))
gat=[(x,y) for x,y in P if r[y][x]=='.' and all(n!='.' for n in nb4(x,y))]
ys=[y for x,y in P if r[y][x]!='.']; xs=[x for x,y in P if r[y][x]!='.']
print('figuur: x %d-%d, y %d-%d (%d x %d px), pixels: %d'%(min(xs),max(xs),min(ys),max(ys),max(xs)-min(xs)+1,max(ys)-min(ys)+1,len(xs)))
print('kleuren gebruikt:',''.join(sorted(set(''.join(r))-{'.'})))
print('open randen (lichte kleur op de buitenrand):',openr)
print('losse pixels:',los)
print('gaatjes (transparant omsloten):',gat)
print('tintclusters < 3 px:',len(cl))
for c,comp in cl: print('  ',c,comp)
if len(sys.argv)>2:
    o=[l.rstrip('\n') for l in open(sys.argv[2])][:64]
    d=[(x,y,o[y][x],r[y][x]) for x,y in P if o[y][x]!=r[y][x]]
    print('gewijzigd t.o.v. vorig:',len(d),'px; alpha-diff:',sum((o[y][x]=='.')!=(r[y][x]=='.') for x,y in P))
