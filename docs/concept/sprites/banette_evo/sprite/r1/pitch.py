import sys; from PIL import Image; import numpy as np
a=np.asarray(Image.open(sys.argv[1]).convert('RGB')).astype(int)
x0,x1,y0,y1=[int(v) for v in sys.argv[2:6]] if len(sys.argv)>5 else (0,1024,0,1024)
a=a[y0:y1,x0:x1]
gx=np.abs(np.diff(a,axis=1)).sum(axis=2).sum(axis=0).astype(float)
gy=np.abs(np.diff(a,axis=0)).sum(axis=2).sum(axis=1).astype(float)
def fit(g):
    res=[]
    for p in np.arange(4,20,0.01):
        best=0;bph=0
        for ph in np.arange(0,p,0.25):
            idx=np.round(np.arange(ph,len(g)-1,p)).astype(int); s=g[idx].mean()
            if s>best: best,bph=s,ph
        res.append((best/g.mean(),p,bph))
    res.sort(reverse=True); return res[:6]
print('x',[(round(a,2),round(b,2),c) for a,b,c in fit(gx)])
print('y',[(round(a,2),round(b,2),c) for a,b,c in fit(gy)])
