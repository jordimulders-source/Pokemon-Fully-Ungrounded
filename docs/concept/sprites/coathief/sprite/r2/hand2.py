# Ronde 2 bovenop r1.txt -> r2.txt. Alleen de benoemde reparaties; alpha gelijk aan r1.
import os
D=os.path.dirname(os.path.abspath(__file__))
R=[list(l.rstrip('\n')) for l in open(os.path.join(D,'r1.txt'))]
G=[l.rstrip('\n') for l in open(os.path.join(D,'groep.txt'))]
R1=[r[:] for r in R]

# 2. CREME ROND HET OOG: (21,42) en (24,40) zijn in het model randmenging (113/109), geen creme -> kopgrijs.
#    Wenkbrauwboog = model: (18..21,38) + (17,39),(17,40); rechts uiteinde in schaduwtint (model 181, smaller).
for (x,y),c in {(21,42):'3',(24,40):'3',(18,38):'9',(19,38):'9',(20,38):'9',(21,38):'9',(17,39):'9',(17,40):'9'}.items(): R[y][x]=c

# 4. OORVOET RECHTS naar het model: rand (U) licht, binnenkant donker, een enkele lijn eromheen.
for (x,y),c in {(24,30):'1',(25,30):'4',(26,30):'4',(27,30):'1',
                (23,31):'1',(24,31):'4',(25,31):'2',(26,31):'2',(27,31):'3',(28,31):'1',
                (22,32):'1',(23,32):'4',(24,32):'2',(25,32):'2',(26,32):'2',(27,32):'3',(28,32):'1',
                (23,33):'1',(24,33):'1',(25,33):'1',(26,33):'2',(27,33):'3',(28,33):'1'}.items(): R[y][x]=c

# 3. LIJF rij 31..47: grote vlakken. Licht linksboven (rug/schouder), midden, sikkel langs buik en achterkant.
B=[(x,y) for y in range(31,48) for x in range(64) if G[y][x]=='B']
def edge(x,y): return any(not(0<=x+dx<64 and 0<=y+dy<64) or R1[y+dy][x+dx]=='0' for dx,dy in [(0,-1),(-1,0),(1,0),(0,1)])
right={y:max(x for x,yy in B if yy==y) for y in range(31,48)}
left={y:min(x for x,yy in B if yy==y) for y in range(31,48)}
bottom={}
for y in range(64):
  for x in range(64):
    if G[y][x]=='B': bottom[x]=max(bottom.get(x,0),y)
# lichtgrens (handgekozen kromme): onder deze rij is het geen licht meer
licht={x:(40 if x<=30 else 38 if x<=33 else 36 if x<=36 else 35 if x<=40 else 34 if x<=44 else 33) for x in range(20,50)}
for x,y in B:
  if edge(x,y) or R1[y][x]=='1': continue
  t='6'
  if y<=licht[x]: t='7'
  # nek: smalle schaduw tegen de kop (kop valt over het lijf), breder onder de kaak
  if x<=left[y]+(0 if y<38 else 1 if y<42 else 2): t='5' if y>=41 else '6'
  # achterkant: sikkel langs de rechterrand, breder naar onder
  w=1 if y<35 else 2 if y<39 else 3
  if x>=right[y]-w: t='5'
  # buik: sikkel langs de onderrand (2 diep in het midden, smaller bij de poten)
  d=2 if 33<=x<=40 else 1
  if y>bottom.get(x,99)-d-(1 if 35<=x<=38 else 0): t='5'
  R[y][x]=t
open(os.path.join(D,'r2.txt'),'w').write('\n'.join(''.join(r) for r in R)+'\n')
bad=[(x,y) for y in range(64) for x in range(64) if (R[y][x]=='0')!=(R1[y][x]=='0')]
print('alpha-diff met r1:',bad)
# opruimen: losse middentint naast de kooplijn
R[33][29]='7'
open(os.path.join(D,'r2.txt'),'w').write('\n'.join(''.join(r) for r in R)+'\n')
