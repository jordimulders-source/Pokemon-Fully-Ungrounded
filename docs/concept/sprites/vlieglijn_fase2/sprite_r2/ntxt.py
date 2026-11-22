# Natief model als tekst in een spritevenster: ntxt.py x0 y0 x1 y1 (spritecoordinaten). Spritecelgrenzen als | en -.
import sys,numpy as np; from PIL import Image
x0,y0,x1,y1=map(int,sys.argv[1:5])
nat=np.asarray(Image.open('natief.png').convert('RGB')).astype(int); grp=np.load('ngrp.npy')
X0,Y0,fx,fy,OX,OY=21,12,109/56,123/63,4,1
L=nat.mean(-1)
def ch(y,x):
    g=grp[y,x]; l=L[y,x]
    if g=='.': return ' '
    if g=='#': return '#'
    if g=='k': return 'k' if l<75 else 'd' if l<140 else 'g' if l<190 else 'w'
    if g=='p': return 'P' if l<85 else 'p' if l<120 else 'q'
    if g=='l': return 'L' if l<60 else 'l' if l<95 else 'i'
    if g=='y': return 'Y' if l<150 else 'y'
    if g=='e': return 'E' if l<170 else 'e'
nx0,nx1=int(X0+(x0-OX)*fx),int(np.ceil(X0+(x1-OX)*fx)); ny0,ny1=int(Y0+(y0-OY)*fy),int(np.ceil(Y0+(y1-OY)*fy))
cb=lambda n:(n-X0)/fx+OX; rb=lambda n:(n-Y0)/fy+OY
for y in range(ny0,ny1):
    s=''
    for x in range(nx0,nx1):
        if int(cb(x))!=int(cb(x-1)): s+='|'
        s+=ch(y,x)
    if int(rb(y))!=int(rb(y-1)): print(f'--- sprite rij {int(rb(y))}')
    print(f'{y:3d} {s}')
print('sprite kolommen vanaf',int(cb(nx0)))
