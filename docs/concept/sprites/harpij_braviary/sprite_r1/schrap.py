# Alternatief (Gengas-methode): rijen/kolommen schrappen die het meest op hun buur lijken; nooit twee naast elkaar.
# Werkt op het gekwantiseerde model (model_idx). Uitvoer schrap_idx.npy
import numpy as np, sys; from PIL import Image
o=np.load('model_idx.npy')[3:95,24:82]; pal=np.load('model_pal.npy')
NR=int(sys.argv[1]); NC=int(sys.argv[2])
P=np.vstack([[255,255,255],pal])
rgb=P[o]
def kies(arr,N):
    n=arr.shape[0]; c=np.full(n,1e9)
    for k in range(1,n-1):
        c[k]=min(np.abs(arr[k]-arr[k-1]).sum(-1).clip(0,90).sum(),np.abs(arr[k]-arr[k+1]).sum(-1).clip(0,90).sum())
    # DP: kies N indices, niet aangrenzend, minimale som
    INF=1e18; dp=np.full((n+1,N+1),INF); dp[0,0]=0; ch=np.zeros((n+1,N+1),int)
    # dp[i][j] = min kost over eerste i lijnen, j gekozen, lijn i-1 vrij of gekozen
    best={}
    import functools
    sys.setrecursionlimit(10000)
    @functools.lru_cache(None)
    def f(i,j):
        if j==0: return 0.0
        if i>=n: return INF
        return min(f(i+1,j), c[i]+f(i+2,j-1))
    weg=[];i=0;j=N
    while j>0:
        if f(i+1,j)<=c[i]+f(i+2,j-1): i+=1
        else: weg.append(i); i+=2; j-=1
    return weg
wr=kies(rgb,NR); wc=kies(rgb.transpose(1,0,2),NC)
b=np.delete(np.delete(o,wr,0),wc,1)
np.save('schrap_idx.npy',b); print(b.shape,'rijen',wr,'kol',wc)
im=Image.fromarray(P[b].astype('uint8')); im.save('schrap.png'); im.resize((b.shape[1]*10,b.shape[0]*10),Image.NEAREST).save('schrap_10x.png')
