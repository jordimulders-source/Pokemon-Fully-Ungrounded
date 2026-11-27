# controle: alpha-diff met r1, aantal kleuren, losse 1-px tintvlekjes, losse lijnpunten, 2x2 lijnklonten
import numpy as np, raster2png, sys
from PIL import Image
R=raster2png.lees(sys.argv[1] if len(sys.argv)>1 else 'raster_af.txt')
r1=np.asarray(Image.open('../r1/uku_pacha_r1.png').convert('RGB')); a1=~(r1==255).all(2)
a2=np.array([[c!='.' for c in r] for r in R])
print('alpha-diff met r1:',int((a1!=a2).sum()), list(zip(*np.where(a1!=a2)))[:10])
print('kleuren (incl. transparant):',len(set(''.join(R))))
def at(x,y): return R[y][x] if 0<=x<64 and 0<=y<64 else '.'
los=[];punt=[];klont=[]
for y in range(64):
  for x in range(64):
    c=R[y][x]
    if c=='.': continue
    n4=[at(x+a,y+b) for a,b in ((1,0),(-1,0),(0,1),(0,-1))]
    n8=[at(x+a,y+b) for a in (-1,0,1) for b in (-1,0,1) if a or b]
    if c in 'Kn':
      if not any(v in 'KnD' for v in n8): punt.append((x,y))
      if all(at(x+a,y+b) in 'Kn' for a,b in ((1,0),(0,1),(1,1))): klont.append((x,y))
    elif c not in 'YPWh' and c not in n4: los.append((x,y,c))
print('losse 1-px tintvlekjes:',len(los),los[:40])
print('losse lijnpunten:',punt)
print('2x2 lijnklonten:',klont)
