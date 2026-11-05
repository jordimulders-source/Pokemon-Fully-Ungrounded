"""Controle 3g t.o.v. 3f (2 px omlaag): gewijzigde pixels per zone (rechthoeken in 3g-coordinaten), 0 elders; runs in de ringen; techniek."""
from PIL import Image
D='/home/user/Pokemon-Fully-Ungrounded/docs/concept/sprites/salticonda/'
a=Image.open(D+'kleur3f/salticonda.png'); b=Image.open(D+'kleur3g/salticonda.png'); A=a.load(); B=b.load(); S=2
def f(x,y): return A[x,y-S] if y-S>=0 else 0
ZONES=[  # (naam, x0,x1,y0,y1) in 3g-coordinaten, eerste treffer telt
 ('5 Electric-glans halsband',18,21,24,24),('5 Electric-glans halsband rechts',32,32,23,23),
 ('3 staart + zoutkegel',55,63,43,57),
 ('1 halsband',12,44,22,28),('1 ring 2',10,50,32,38),('1 ring 3',4,52,45,52),
 ('2 onderrand/rechtsonder',0,63,57,62),('2 schaduwkant rechts (alleen K->O)',40,63,23,40)]
cnt={z[0]:0 for z in ZONES}; rest=[]
for y in range(64):
  for x in range(64):
    if f(x,y)!=B[x,y]:
      for n,x0,x1,y0,y1 in ZONES:
        if x0<=x<=x1 and y0<=y<=y1: cnt[n]+=1; break
      else: rest.append((x,y))
bad2=[(x,y) for y in range(23,41) for x in range(40,64) if f(x,y)!=B[x,y] and not (f(x,y)==2 and B[x,y]==1) and not (12<=x<=44 and 22<=y<=28) and not (10<=x<=50 and 32<=y<=38)]
print('zone 2 rechts: andere wijziging dan K->O:',bad2)
print('palet 0-14 gelijk:',a.getpalette()[:45]==b.getpalette()[:45],'| index 15 =',tuple(b.getpalette()[45:48]),'| modus',b.mode,'| transparency',b.info.get('transparency'),'| maat',b.size)
for n in cnt: print(f'  {n}: {cnt[n]} px')
print('  totaal gewijzigd:',sum(cnt.values()),'| BUITEN de zones:',len(rest),rest[:10])
print('rij 0 en 1 leeg:',all(B[x,0]==0 and B[x,1]==0 for x in range(64)),'| rij 63 leeg:',all(B[x,63]==0 for x in range(64)))
# runs van een zelfde turquoise-index (11-14) per rij in de ringzones
mx={}
for n,x0,x1,y0,y1 in ZONES[3:6]+[('staart',55,63,43,57)]:
  m=0
  for y in range(y0,y1+1):
    run=1
    for x in range(x0+1,x1+1):
      run = run+1 if B[x,y]==B[x-1,y] and B[x,y] in (11,12,13,14) else 1
      m=max(m,run)
  mx[n]=m
print('langste turquoise-run per ring:',mx)
# open randen, losse pixels, donker aandeel
N=lambda x,y:[(x+dx,y+dy) for dx,dy in ((1,0),(-1,0),(0,1),(0,-1)) if 0<=x+dx<64 and 0<=y+dy<64]
edge={};los=0;tot=0;dark={}
for im,P in (('3f',A),('3g',B)):
  t=sum(1 for x in range(64) for y in range(64) if P[x,y]); d=sum(1 for x in range(64) for y in range(64) if P[x,y]==1); dark[im]=(t,d,round(d/t,3))
for y in range(64):
  for x in range(64):
    if B[x,y]:
      nb=N(x,y)
      if any(B[p]==0 for p in nb) or x in(0,63) or y in(0,63): edge[B[x,y]]=edge.get(B[x,y],0)+1
      if all(B[p]!=B[x,y] for p in nb): los+=1
print('indexen aan de buitenrand:',dict(sorted(edge.items())),'| pixels zonder gelijke buur:',los)
print('pixels / donker (index 1) / aandeel:',dark)
