# diff r7 -> r8: per pixel, bevroren veer + oog/masker, silhouet
import numpy as np; from PIL import Image
CH='.KWwvucbanyedrs'
a=np.array(Image.open('../sprite_r7/rufflet_r7.png')); b=np.array(Image.open('rufflet_r8.png'))
assert Image.open('rufflet_r8.png').getpalette()[:45]==Image.open('../sprite_r7/rufflet_r7.png').getpalette()[:45]
d=a!=b; print('gewijzigd:',int(d.sum()))
for y,x in zip(*np.where(d)): print(f'  ({x},{y}) {CH[a[y,x]]}->{CH[b[y,x]]}')
veer=list(zip(*np.where((a==13)|(a==14))))+[(22,26),(23,28),(23,25)]
print('veer (alle r/s + W (26,22),(28,23),(25,23)) diff:',sum(int(d[p]) for p in veer))
toe={(22,27),(22,28),(24,30),(31,18),(32,18),(32,19)}
print('oog/masker-vak x22-32 y18-34 diff buiten toegestane px:',sum(int(d[y,x]) for y in range(18,35) for x in range(22,33) if (x,y) not in toe))
s=(a>0)!=(b>0); print('silhouet:',[(int(x),int(y),'+' if b[y,x] else '-') for y,x in zip(*np.where(s))])
