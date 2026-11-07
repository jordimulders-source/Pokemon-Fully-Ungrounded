# klas.py X0 Y0 X1 Y1 : meetkaart per spritepixel: '#'=zwart (gem<60), 'o'=donker (60-95), '-'=mix (p15<60), anders tint-cijfer van modus palet; '.' buiten silhouet
import sys
from tl import *
p=np.array(pal(P+'kleur_r3/normal.pal'),float)
X0,Y0,X1,Y1=map(int,sys.argv[1:5])
print('    '+''.join(str(x%10) for x in range(X0,X1)))
for y in range(Y0,Y1):
  r=''
  for x in range(X0,X1):
    if not SIL[y,x]: r+='.'; continue
    sl=box(x,y); v=LUM[sl]; m=v.mean(); q=np.percentile(v,15)
    c=C[sl].reshape(-1,3); d=((c[:,None,:]-p[None,1:])**2).sum(2).argmin(1)+1
    r+= '#' if m<60 else 'o' if m<95 else '-' if q<60 else '%X'%np.bincount(d,minlength=16).argmax()
  print('%2d  '%y+r)
