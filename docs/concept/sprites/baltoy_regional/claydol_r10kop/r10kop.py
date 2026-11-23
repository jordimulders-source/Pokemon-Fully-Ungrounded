# r10-kop (natief raster) zonder krans-rondjes en punt: alles boven cut(x) binnen de kopellips wordt
# kopsteen uit de directe omgeving eronder (per kolom: meest voorkomende steentoon van de eerste 3 schone pixels).
import os, numpy as np; from PIL import Image
from klas import klas, M
H=os.path.dirname(os.path.abspath(__file__))
E=(49.5,41.0,31.0,25.6)          # kopellips r10 (cx,cy,rx,ry), gemeten op de zichtbare omtrek
# eerste schone kopregel onder de rondjes/punt, per kolombereik (natieve x)
CUT=[(19,25,31),(26,33,26),(34,41,24),(42,47,25),(48,57,30),(58,63,30),(64,80,33)]
def cut(x):
    for a,b,c in CUT:
        if a<=x<=b: return c
    return 0
def bouw():
    T,_=klas(); T=T.copy()
    yy,xx=np.mgrid[0:99,0:99]
    ell=((xx-E[0])/E[2])**2+((yy-E[1])/E[3])**2<=1
    gevuld=np.zeros((99,99),bool)
    for x in range(19,81):
        c=cut(x)
        sch=[T[y,x] for y in range(c,c+14) if T[y,x] in 'hlmd'][:3] or ['h']
        t=max(set(sch),key=sch.count)
        for y in range(0,c):
            if ell[y,x]: T[y,x]=t; gevuld[y,x]=True
    kop=ell.copy()
    return T,kop,gevuld
if __name__=='__main__':
    T,kop,gev=bouw()
    C={k:v for k,v in M.items()}
    a=np.array([[C[t] for t in r] for r in T],np.uint8)
    a[~kop]=(a[~kop]*0.35+np.array([255,255,255])*0.65).astype(np.uint8)
    import sys; sys.path.insert(0,H); from rooster import rooster
    rooster(Image.fromarray(a),10,os.path.join(H,'r10kop_check.png'),12,8,88,70)
