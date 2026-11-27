# zone van de lichte voorkant in spritepixels: voetafdruk op het natieve model overwegend licht
import numpy as np; from PIL import Image
N=np.asarray(Image.open('../../model/r2_natief.png').convert('RGB')).astype(float); LUM=N.mean(2)
F=64/92; X0,Y0,OX,OY=5,7,0,2
def s2n(i,j): return X0+(i-OX)/F, X0+(i-OX+1)/F, Y0+(j-OY)/F, Y0+(j-OY+1)/F
def voet(i,j):
    x0,x1,y0,y1=s2n(i,j); out=[]
    for cy in range(int(y0),int(np.ceil(y1))):
      for cx in range(int(x0),int(np.ceil(x1))):
        a=(min(x1,cx+1)-max(x0,cx))*(min(y1,cy+1)-max(y0,cy))
        if a>0: out.append((cx,cy,a))
    return out
def lichtfrac(i,j,drempel=150):
    v=voet(i,j); t=sum(a for _,_,a in v)
    return sum(a for x,y,a in v if drempel<=LUM[y,x]<240)/t
def toon(i,j):
    "oppervlak-gewogen mediaan van de lichte cellen (lijnen en donker tellen niet)"
    v=[(LUM[y,x],a) for x,y,a in voet(i,j) if 140<=LUM[y,x]<240]
    if not v: return None
    v.sort(); t=sum(a for _,a in v); s=0
    for l,a in v:
        s+=a
        if s>=t/2: return l
