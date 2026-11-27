# Pitch en fase van het natieve raster in het model meten (randsterkte per kolom/rij).
import numpy as np; from PIL import Image
a=np.asarray(Image.open('../gemini/model_kandidaat.png').convert('RGB')).astype(float)
L=a.mean(2)
fig=a.min(2)<225; yy,xx=np.where(fig); print('bbox',xx.min(),xx.max(),yy.min(),yy.max())
ex=np.abs(np.diff(L,axis=1)).sum(0); ey=np.abs(np.diff(L,axis=0)).sum(1)
def best(e):
    res=[]
    for p in np.arange(4.8,16,0.01):
        ph=np.arange(len(e))
        # som randsterkte op posities dicht bij k*p+f
        for f in np.arange(0,p,0.25):
            pass
    return res
def score(e,p):
    n=np.arange(len(e)); ang=2*np.pi*n/p
    z=(e*np.exp(1j*ang)).sum(); return abs(z)/e.sum(), (np.angle(z)%(2*np.pi))/(2*np.pi)*p
for nm,e in (('x',ex),('y',ey)):
    sc=[(score(e,p)[0],p) for p in np.arange(4.8,16,0.01)]
    sc.sort(reverse=True); print(nm,[(round(s,3),round(p,2)) for s,p in sc[:6]])
    for p in (sc[0][1],):
        print(' fase',score(e,p)[1])
