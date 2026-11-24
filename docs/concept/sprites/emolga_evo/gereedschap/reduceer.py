# Oppervlak-middeling (Hauntflare-methode, GEMINI.md: >13% verkleinen = niet schrappen): elke spritepixel krijgt
# de modelklasse met de grootste bedekking (meerderheidsband, Swablu-les: geen mengtinten); silhouet = bedekking >= DREMPEL.
import numpy as np
def gewichten(n_doel,n_bron,s,o):
    # doelpixel X bedekt bronbereik [(X-o)/s, (X+1-o)/s)
    W=np.zeros((n_doel,n_bron))
    for X in range(n_doel):
        a,b=(X-o)/s,(X+1-o)/s
        for u in range(max(0,int(np.floor(a))),min(n_bron,int(np.ceil(b)))):
            W[X,u]=max(0,min(b,u+1)-max(a,u))
    return W
def bedekking(c,s,ox,oy,nk,N=64):
    Wy=gewichten(N,c.shape[0],s,oy); Wx=gewichten(N,c.shape[1],s,ox)
    cov=np.stack([Wy@(c==k).astype(float)@Wx.T for k in range(nk)],-1)
    return cov/np.maximum(cov.sum(-1,keepdims=True),1e-9)
def reduceer(c,s,ox,oy,nk,drempel=0.45,kweeg=1.0,N=64):
    cov=bedekking(c,s,ox,oy,nk,N)
    fg=1-cov[...,0]
    w=cov.copy(); w[...,0]=0; w[...,1]*=kweeg
    o=w.argmax(-1); o[fg<drempel]=0
    return o,cov
