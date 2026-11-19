from PIL import Image
import numpy as np, sys
a=np.array(Image.open('../../r17/picapau.png'))
L=np.array([-0.55,-0.7,0.5]); L/=np.linalg.norm(L)
def I(x,y,c,r):
    u=(x-c[0])/r[0]; v=(y-c[1])/r[1]; nz=np.sqrt(max(0.0,1-u*u-v*v))
    n=np.array([u,v,nz]); n/=np.linalg.norm(n); return n@L
b=a.copy()
def zone(x,y):
    if y<=21 and 24<=x<=34: return 'E'
    if y<=28 and x>=32: return 'K'
    if y<=37: return 'H'
    if y==38: return 'N'
    return 'L'
th={'H':(0.42,0.05),'L':(0.62,0.12)}
cs={'H':((24.5,29),(10,8.5)),'L':((25.5,45.5),(10.5,9.5))}
for y in range(64):
  for x in range(64):
    if a[y,x] not in (2,3,4): continue
    z=zone(x,y)
    if z not in th: continue
    i=I(x,y,*cs[z]); hi,lo=th[z]
    b[y,x]=2 if i>hi else (3 if i>lo else 4)
np.save('_tmp/auto.npy',b)
for y in range(12,63): print('%2d '%y+''.join('.' if v==0 else '%X'%v for v in b[y,14:49]))
from collections import Counter
for z in 'HL':
  c=Counter(int(b[y,x]) for y in range(64) for x in range(64) if b[y,x] in (2,3,4) and zone(x,y)==z); print(z,c)
