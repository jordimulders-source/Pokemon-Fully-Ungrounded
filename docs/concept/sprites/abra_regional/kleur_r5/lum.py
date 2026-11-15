# lum.py x0 x1 y0 y1 : native luma per spritecel (2x2), kolommen = spritex
import sys; from PIL import Image; import numpy as np
n=np.asarray(Image.open('../kleur_r1/natief.png').convert('RGB')).astype(float)@[.299,.587,.114]
x0,x1,y0,y1=map(int,sys.argv[1:5])
def g(ny,nx):
    if 0<=ny<n.shape[0] and 0<=nx<n.shape[1]: v=int(n[ny,nx]); return '  .' if v>=240 else '%3d'%v
    return '  .'
print('     '+''.join('%8d'%x for x in range(x0,x1)))
for y in range(y0,y1):
    for r in range(2):
        print(('%3d%s '%(y,'a') if r==0 else '    b ')+''.join(' '+g(2*y-14+r,2*x-1)+g(2*y-14+r,2*x)+' ' for x in range(x0,x1)))
