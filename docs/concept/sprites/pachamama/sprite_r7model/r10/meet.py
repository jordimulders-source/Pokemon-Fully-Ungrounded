# r10: r10-gezicht (natieve klassen uit r9/natief_klasse.npy) meten in een willekeurig gezichtsmasker.
# Gelijke schaal T natieve px per spritepx; natief (i,j) = (CI + (x-29)*T, CJ + (y-30)*T) voor spritecoordinaat (x,y).
# Elke spritecel: alle natieve pixels waarvan het middelpunt in de cel valt; regels zoals r9 (lijnen/oogwit winnen bij >=1/3).
# Gebruik: python3 r10/meet.py MASKER.npy BASIS.npy T CI CJ UIT.npy
import sys, numpy as np
R='docs/concept/sprites/pachamama/sprite_r7model/'
m=np.load(sys.argv[1]); o=np.load(sys.argv[2]).copy(); T,CI,CJ=map(float,sys.argv[3:6])
K=np.load(R+'r9/natief_klasse.npy'); NJ,NI=K.shape
jj,ii=np.mgrid[0:NJ,0:NI]; X=29+(ii+0.5-CI)/T; Y=30+(jj+0.5-CJ)/T
leeg=[]
for y,x in zip(*np.where(m)):
  sel=(X>=x)&(X<x+1)&(Y>=y)&(Y<y+1); c=K[sel]; f=c[c>=0]; n=len(c)
  if len(f)<0.4*n: o[y,x]=0; leeg.append((int(y),int(x))); continue
  cnt={k:(f==k).sum() for k in (1,2,3,4,13,10,5)}; t=len(f)
  if cnt[1]>=t/3: v=1
  elif cnt[10]>=t/3: v=10
  elif cnt[2]>=t/3 or cnt[1]+cnt[2]>=0.45*t: v=2
  else: v=max((3,4,13,5),key=lambda k:cnt[k])
  o[y,x]=v
for _ in range(6):
  for (y,x) in leeg:
    if o[y,x]: continue
    nb=[o[y+dy,x+dx] for dy in (-1,0,1) for dx in (-1,0,1) if m[y+dy,x+dx] and o[y+dy,x+dx] in (3,4,13)]
    if nb: o[y,x]=max(set(nb),key=nb.count)
np.save(sys.argv[6],o)
print('leeg (buiten modelgezicht, buurtint):',len(leeg),leeg)
ys,xs=np.where(m)
for r in range(ys.min()-1,ys.max()+2): print('%2d '%r+''.join((('%x'%o[r,c]) if m[r,c] else ('·' if o[r,c] else ' ')) for c in range(xs.min()-2,xs.max()+3)), ' (kol %d..)'%(xs.min()-2) if r==ys.min()-1 else '')
