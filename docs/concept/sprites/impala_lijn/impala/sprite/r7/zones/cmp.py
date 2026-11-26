# per pixel in een zone: modeldekking gemeten op de modelcontour (rijmidden en kolommidden, 1024 px, gemiddeld) vs huidig silhouet
import numpy as np, json, sys
RN=sys.argv[1]; X0,Y0,X1,Y1=map(int,sys.argv[2:6])
km=json.load(open('kaal_meta.json')); x0,y0,p=km['x0'],km['y0'],km['p']
wl=np.load('witlab.npz')['a']; fg=~((wl==-2)|(wl==1))
meta=json.load(open(f'{RN}/grid.json')); g=meta['grid']; OX,OY=meta['OX'],meta['OY']
def dek(x,y):
    xa,xb=int(round(x0+x*p)),int(round(x0+(x+1)*p)); ya,yb=int(round(y0+y*p)),int(round(y0+(y+1)*p))
    r=fg[int(y0+(y+.5)*p),xa:xb].mean(); k=fg[ya:yb,int(x0+(x+.5)*p)].mean(); return (r+k)/2
for Y in range(Y0,Y1+1):
    s=''
    for X in range(X0,X1+1):
        x,y=X-OX,Y-OY; o=g[y][x]!='.'; d=dek(x,y)
        s+= ('+' if d>=0.5 and not o else '-' if d<0.5 and o else g[y][x])
    print('%2d '%Y+s)
