# Silhouetvergelijking: modeldekking per spritepixel (achtergrond via floodfill van de rand) tegen een sprite.
# Uitvoer: '#'=beide, '+'=alleen model (>=50%), '-'=alleen sprite, '.'=geen. Gebruik: python3 masker.py MODEL SPRITE X0 Y0 X1 Y1
import sys,numpy as np; from PIL import Image; from box import win
M=np.asarray(Image.open(sys.argv[1]).convert('RGB')).astype(float); S=np.asarray(Image.open(sys.argv[2])); x0,y0,x1,y1=map(int,sys.argv[3:7])
l=M@[.299,.587,.114]; s=M.max(2)-M.min(2); w=(l>225)&(s<30)
BG=np.zeros_like(w); BG[0]=w[0]; BG[-1]=w[-1]; BG[:,0]=w[:,0]; BG[:,-1]=w[:,-1]
while True:
    p=np.pad(BG,1); n=(p[:-2,1:-1]|p[2:,1:-1]|p[1:-1,:-2]|p[1:-1,2:]|BG)&w
    if (n==BG).all(): break
    BG=n
F=(~BG).astype(float)[...,None].repeat(3,2)
print('   '+''.join(str(x%10) for x in range(x0,x1)))
for Y in range(y0,y1):
    r=''
    for X in range(x0,x1):
        c=win(F,X,Y)[:,0].mean(); m=c>=.5; sp=S[Y,X]>0
        r+='#' if m and sp else '+' if m else '-' if sp else '.'
    print('%2d '%Y+r)
