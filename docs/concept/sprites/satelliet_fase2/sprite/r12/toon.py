import sys, numpy as np
exec(open('bouw_r12.py').read().split('# ======== OPSLAAN')[0])
H='0123456789ABCDEF'
x0,x1,y0,y1=map(int,sys.argv[1:5])
print('    '+' '.join('%2d'%x for x in range(x0,x1)))
for y in range(y0,y1): print('%2d  '%y+' '.join(' '+('.' if v==0 else H[v]) for v in a[y,x0:x1]))
