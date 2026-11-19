# Gedeelde meting: per spritecel (png-coords) de natieve 3x3 modelklassen
import numpy as np
K=np.load('_tmp/klassen.npy')
GRP={0:'bg',1:'z',2:'b',3:'b',4:'b',5:'c',6:'c',7:'c',8:'r',9:'g',10:'g',11:'g',12:'y',13:'y',14:'w'}
def cel(x,y):
    r,c=3*y-2,4+3*x
    if r<0: return np.zeros(9,int)
    return K[max(r,0):r+3,c:c+3].ravel()
def nonbg(x,y): return int((cel(x,y)>0).sum())
def toon(x,y,grp):
    b=[v for v in cel(x,y) if GRP[v]==grp]
    return max(set(b),key=b.count) if b else None
