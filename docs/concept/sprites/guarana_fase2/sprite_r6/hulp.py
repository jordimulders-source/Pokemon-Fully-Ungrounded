# r6 hulpjes: labelen zonder scipy, buren
import numpy as np
N4=((-1,0),(1,0),(0,-1),(0,1)); N8=[(dy,dx) for dy in (-1,0,1) for dx in (-1,0,1) if dy or dx]
def ok(y,x): return 0<=y<64 and 0<=x<64
def label(m,nb=N4):
    lab=np.zeros(m.shape,int); k=0
    for y,x in zip(*np.where(m)):
        if lab[y,x]: continue
        k+=1; st=[(y,x)]; lab[y,x]=k
        while st:
            cy,cx=st.pop()
            for dy,dx in nb:
                yy,xx=cy+dy,cx+dx
                if ok(yy,xx) and m[yy,xx] and not lab[yy,xx]: lab[yy,xx]=k; st.append((yy,xx))
    return lab,k
def gauss(m,s):
    r=int(np.ceil(3*s)); k=np.exp(-np.arange(-r,r+1)**2/(2*s*s)); k/=k.sum()
    p=np.pad(m.astype(float),r)
    p=np.apply_along_axis(lambda v:np.convolve(v,k,'same'),0,p)
    p=np.apply_along_axis(lambda v:np.convolve(v,k,'same'),1,p)
    return p[r:-r,r:-r]
