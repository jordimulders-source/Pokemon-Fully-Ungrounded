# tab.py X0 Y0 X1 Y1 : per pixel onderlaagteken + donkerfractie (0-9) + dekking (0-9)
import sys,numpy as np
D='/home/user/Pokemon-Fully-Ungrounded/docs/concept/sprites/viscacha/kleur_r7/'
m=np.load(D+'stappen/meting.npz'); U=[l.rstrip() for l in open(D+'onderlaag.txt')]
x0,y0,x1,y1=map(int,sys.argv[1:5])
print('    '+''.join('%-4d'%x if x%2==0 else '    ' for x in range(x0,x1)))
for y in range(y0,y1):
  print('%2d  '%y+''.join(U[y][x]+str(min(9,int(m['dkf'][y,x]*10)))+str(min(9,int(m['cov'][y,x]*10)))+' ' for x in range(x0,x1)))
