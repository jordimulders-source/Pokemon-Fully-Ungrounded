# basis.py: r7-basis = r6 + keuring_r6 MOET 1 (roze tong/hoornlicht) + MOET 2 (middentint alleen als doorlopende rand)
# Palet: index 14 (hoornmidden 190,45,46) samengevoegd met haarrood r (index 6); index 14 = roze (212,94,90).
import numpy as np; from PIL import Image
src=Image.open('../sprite_r6/vuurduivel_r6.png'); a=np.array(src); a0=a.copy()
pal=src.getpalette()[:48]; pal[14*3:14*3+3]=[212,94,90]
K,R,r,O,Y,X,P=1,5,6,7,8,12,14
log=[]
def zet(x,y,c,why):
    if a[y,x]!=c: log.append(f'({x},{y}) {a[y,x]}->{c}  {why}'); a[y,x]=c
for y,x in zip(*np.where(a0==14)): zet(x,y,r,'MOET1: hoornmidden -> haarrood')
for x,y in [(22,38),(23,38),(24,38),(25,38),(22,39),(23,39),(24,39)]: zet(x,y,P,'MOET1: tong roze')
for x,y in [(15,23),(15,24),(16,25),(25,23),(25,24),(26,22)]: zet(x,y,P,'MOET1: hoornlicht roze')
# MOET 2: haar (x10-41, y12-30). Eerst de middentint terug naar O (= r5-vlammen), dan de rand opnieuw en doorlopend leggen.
zone=[(x,y) for y in range(12,31) for x in range(10,42)]
def nb(x,y): return [a[y+dy,x+dx] for dx,dy in ((1,0),(-1,0),(0,1),(0,-1))]
for x,y in zone:
    if a[y,x]==X: a[y,x]=O
# rechts van de kop: één tong (35,24-27) met O-kern, geen om-en-om in kolom 35/36/37
for x,y in [(35,24),(35,25),(35,26),(36,24)]: a[y,x]=O
for x,y in [(36,25),(36,26),(35,27),(34,27),(37,26),(37,27),(36,27)]: a[y,x]=r
# losse r-stipjes in oranje (geen r/R/lijn als buur) -> O
for x,y in zone:
    if a[y,x]==r and sum(v in (r,R,K) for v in nb(x,y))==0: a[y,x]=O
# middentint: O-pixel met rood rechts of onder EN oranje links of boven (dus rand langs een tong, geen top-stipje)
rand=[]
for x,y in zone:
    if a[y,x]==O and (a[y,x+1] in (r,R) or a[y+1,x] in (r,R)) and (a[y,x-1] in (O,Y) or a[y-1,x] in (O,Y)): rand.append((x,y))
for x,y in rand: a[y,x]=X
def clusters(c):
    seen=set(); out=[]
    for x,y in zone:
        if a[y,x]==c and (x,y) not in seen:
            st=[(x,y)]; cl=[]; seen.add((x,y))
            while st:
                p=st.pop(); cl.append(p)
                for dx,dy in ((1,0),(-1,0),(0,1),(0,-1)):
                    q=(p[0]+dx,p[1]+dy)
                    if q not in seen and a[q[1],q[0]]==c: seen.add(q); st.append(q)
            out.append(cl)
    return out
# rand-clusters die ook diagonaal samenhangen tellen samen; echt losse (1 px, geen diagonale X-buur) -> O
for x,y in list(rand):
    if not any(a[y+dy,x+dx]==X for dx in (-1,0,1) for dy in (-1,0,1) if (dx,dy)!=(0,0)): a[y,x]=O
# rechts van de kop (x32-38, y23-28) als laatste vast: één tong met O-kern (35,24-25) en middentintrand rechts/onder
for x,y,c in [(33,23,O),(34,23,O),(35,23,O),(36,23,O),(33,24,r),(34,24,r),(35,24,O),(36,24,X),(32,25,r),(33,25,r),(34,25,r),
              (35,25,O),(36,25,X),(35,26,X),(36,26,r),(35,27,X),(34,27,r),(36,27,r),(37,26,r),(37,27,r)]: a[y,x]=c
for y,x in zip(*np.where(a!=a0)):
    if 12<=y<=30 and 10<=x<=41: log.append(f'({x},{y}) {a0[y,x]}->{a[y,x]}  MOET2: vlamrand opnieuw (middentint alleen doorlopend langs een oranje tong)')
im=Image.fromarray(a,'P'); im.putpalette(pal+[0]*(768-48)); im.save('vuurduivel_r7_basis.png',transparency=0,bits=4)
open('basis_wijzigingen.txt','w').write('\n'.join(log)+'\n')
print(len(log),'px; alpha-diff',int(((a>0)!=(a0>0)).sum()),'; ogen-diff',int((a[30:35,15:20]!=a0[30:35,15:20]).sum()+(a[28:35,23:29]!=a0[28:35,23:29]).sum()),
      '; lijn-diff',int(((a==K)!=(a0==K)).sum()),'; kleuren',len(set(a.flatten())))
print('X-clusters haar',sorted(len(c) for c in clusters(X)))
