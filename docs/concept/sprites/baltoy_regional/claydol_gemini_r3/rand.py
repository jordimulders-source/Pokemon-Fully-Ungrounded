import numpy as np
def randlicht(S,maxlicht=6):
    T=np.pad(S==0,1,constant_values=True); out=[]
    for y,x in zip(*np.where(S>0)):
        if (T[y,x+1] or T[y+2,x+1] or T[y+1,x] or T[y+1,x+2]) and S[y,x]<=maxlicht and S[y,x]>0: out.append((y,x,S[y,x]))
    return out
