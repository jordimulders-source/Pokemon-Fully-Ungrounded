from PIL import Image; import numpy as np
from collections import deque
def load(n): return np.asarray(Image.open(f'src{n}.png').convert('RGB')).astype(int)
def green(a): return (a[...,1]>a[...,0]+25)&(a[...,1]>a[...,2]+15)
def dil(m,r):
    o=m.copy()
    for dy in range(-r,r+1):
        for dx in range(-r,r+1):
            if dx*dx+dy*dy<=r*r: o|=np.roll(np.roll(m,dy,0),dx,1)
    return o
def ero(m,r): return ~dil(~m,r)
def comp(m,seeds):
    H,W=m.shape; out=np.zeros_like(m); q=deque()
    for y,x in seeds:
        if m[y,x]: out[y,x]=1; q.append((y,x))
    while q:
        y,x=q.popleft()
        for dy,dx in ((1,0),(-1,0),(0,1),(0,-1)):
            yy,xx=y+dy,x+dx
            if 0<=yy<H and 0<=xx<W and m[yy,xx] and not out[yy,xx]: out[yy,xx]=1; q.append((yy,xx))
    return out
def antmask(a,seeds,ymax):
    lum=a.mean(2)
    # antenna: not green, not cream (cream = bright and low chroma)
    chroma=a.max(2)-a.min(2)
    cream=(lum>185)&(chroma<90)
    m=(~green(a))&(~cream)
    m[ymax:]=False
    m=comp(m,seeds)
    m=ero(dil(m,4),4)  # close stripes
    return m.astype(bool)
