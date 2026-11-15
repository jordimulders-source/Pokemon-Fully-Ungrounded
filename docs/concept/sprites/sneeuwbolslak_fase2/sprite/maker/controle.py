# python3 maker/controle.py raster.txt : silhouet, kleuren, tintvlakjes <3 px, losse donkere pixels, open buitenrand
import sys,numpy as np
R=[l.rstrip('\n') for l in open(sys.argv[1])]; SIL=np.load('sil56_rond.npy')
A=np.array([[c!='.' for c in r] for r in R]); print('silhouetdiff',int((A!=SIL).sum()))
print('letters',sorted(set(''.join(R))-{'.'}),'=',len(set(''.join(R))),'kleuren incl. transparant')
def comp(x,y,pred):
  st=[(x,y)]; s={(x,y)}
  while st:
    a,b=st.pop()
    for da,db in ((1,0),(-1,0),(0,1),(0,-1)):
      p=(a+da,b+db)
      if 0<=p[0]<64 and 0<=p[1]<64 and p not in s and pred(R[p[1]][p[0]]): s.add(p); st.append(p)
  return s
klein=[];seen=set()
for y in range(64):
  for x in range(64):
    c=R[y][x]
    if c in 'abceuvrst' and (x,y) not in seen:
      s=comp(x,y,lambda k:k==c); seen|=s
      if len(s)<3: klein.append((c,sorted(s)))
print('tintvlakjes <3 px:',len(klein)); [print(' ',k) for k in klein]
los=[(x,y) for y in range(1,63) for x in range(1,63) if R[y][x] in 'd#' and all(SIL[y+dy,x+dx] for dy,dx in ((1,0),(-1,0),(0,1),(0,-1))) and not any(R[y+dy][x+dx] in 'd#' for dy,dx in ((1,0),(-1,0),(0,1),(0,-1),(1,1),(1,-1),(-1,1),(-1,-1)))]
print('losse donkere pixels:',los)
rand=[(x,y) for y in range(64) for x in range(64) if SIL[y,x] and R[y][x] not in 'd#' and any(not(0<=y+dy<64 and 0<=x+dx<64) or not SIL[y+dy,x+dx] for dy,dx in ((1,0),(-1,0),(0,1),(0,-1)))]
print('lichte pixels op buitenrand (open omlijning):',rand)
