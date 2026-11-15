# lijnkaart: modelpixels met p10 < 55 als lijn ('#'), rest = glad.txt. Uitvoer sprite/maker/lijnen.txt
import numpy as np
exec(open('sprite/meet/px.py').read().split('if __name__')[0])
SIL=np.load('sprite/sil56_rond.npy')
R=[list(l.rstrip('\n')) for l in open('sprite/maker/glad.txt')]
for y in range(64):
  for x in range(64):
    if SIL[y,x] and R[y][x] not in 'rstuv':
      b,l=blok(x,y)
      if l.size and np.percentile(l,10)<55: R[y][x]='#'
open('sprite/maker/lijnen.txt','w').write('\n'.join(''.join(r) for r in R)+'\n')
print('   '+''.join(str(x//10) for x in range(64)));print('   '+''.join(str(x%10) for x in range(64)))
for y in range(18,60): print('%2d %s'%(y,''.join(R[y])))
