# nat.py sx0 sx1 sy0 sy1: natieve klassenkaart in spritecoordinaten (2x2 natieve px per spritepixel, | = spritegrens)
import sys, numpy as np
K=np.load('natief_klas.npy'); CH='.#dmlRrOYbBkpWMa'
X0,Y0,NX,NY=[int(v) for v in open('info.txt').read().split()]
sx0,sx1,sy0,sy1=map(int,sys.argv[1:5])
print('    '+''.join('%-3d'%x for x in range(sx0,sx1)))
for sy in range(sy0,sy1):
    for r in range(2):
        ny=NY+(sy-Y0)*2+r
        print(('%2d  ' % sy if r==0 else '    ')+''.join(CH[K[ny,NX+(sx-X0)*2]]+CH[K[ny,NX+(sx-X0)*2+1]]+'|' for sx in range(sx0,sx1)))
