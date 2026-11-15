# Stap 2b: zelfde vlakgewichten als reduceer.py, maar met kenmerkregel zodat dunne modellijnen en kleine
# kenmerkkleuren (lijn, lila, creme, tongroze, tandwit) niet wegvallen in het gemiddelde:
# per doelpixel de bedekking per kleurgroep; haalt een kenmerkgroep >= T, dan wint de grootste kenmerkgroep
# (kleur = dichtstbijzijnde paletkleur van die groep bij het gemiddelde van die pixels), anders gemiddelde van het bruin.
# Niets getekend: elke pixel komt uit zijn eigen vlak modelpixels.
import sys; from PIL import Image; import numpy as np
from reduceer import nq, fig, PAL, X0,X1,Y0,Y1, wts, W, H
P=PAL.astype(float); lum=P@[0.299,0.587,0.114]
def grp(c):
    r,g,b=c; l=0.299*r+0.587*g+0.114*b
    if min(c)>240: return 'wit'
    if max(c)-min(c)<15 and l>150: return 'grijs'
    if l<45: return 'lijn'
    if r>215 and g<160: return 'roze'
    if r>205 and g>195: return 'creme'
    if b>r-30 and b>g: return 'lila'
    return 'bruin'
G=[grp(tuple(p)) for p in PAL]
if __name__=='__main__':
    for p,g in zip(PAL,G): print(tuple(p),g)
qi=np.argmin(((nq[:,:,None].astype(float)-P[None,None])**2).sum(3),2)
T={'grijs':0.3,'wit':0.2,'roze':0.25,'lijn':0.30,'creme':0.30,'lila':0.30}
PRI=['wit','roze','grijs','lijn','creme','lila']
def reduce(tw,T=T):
    th=int(round(tw*(Y1-Y0)/(X1-X0)))
    Wx=wts(X0,X1,tw)[:, :W]; Wy=wts(Y0,Y1,th)[:, :H]
    Wx=np.pad(Wx,((0,0),(0,W-Wx.shape[1]))); Wy=np.pad(Wy,((0,0),(0,H-Wy.shape[1])))
    f=fig.astype(float); area=np.outer(Wy.sum(1),Wx.sum(1)); cov=Wy@f@Wx.T/area
    fg={}; colg={}
    for g in set(G):
        m=np.isin(qi,[k for k in range(len(G)) if G[k]==g]).astype(float)*f
        s=Wy@m@Wx.T; fg[g]=s/np.maximum(Wy@f@Wx.T,1e-9)
        colg[g]=np.stack([Wy@(nq[:,:,c]*m)@Wx.T for c in range(3)],2)/np.maximum(s,1e-9)[:,:,None]
    idx=np.zeros((th,tw),int)
    for j in range(th):
        for i in range(tw):
            if cov[j,i]<0.45: continue
            cand=[g for g in PRI if fg[g][j,i]>=T[g]]
            if cand:
                g=max(cand,key=lambda g:(fg[g][j,i],-PRI.index(g)))
            else:
                g='bruin' if fg['bruin'][j,i]>0 else max(PRI,key=lambda g:fg[g][j,i])
            ks=[k for k in range(len(G)) if G[k]==g]
            c=colg[g][j,i]; idx[j,i]=ks[int(np.argmin(((P[ks]-c)**2).sum(1)))]+1
    return idx
if __name__=='__main__':
    for tw in (46,50,54):
        idx=reduce(tw); np.save(f'red2_{tw}.npy',idx)
        im=np.zeros(idx.shape+(4,),'uint8'); m=idx>0; im[m,:3]=PAL[idx[m]-1]; im[m,3]=255
        Image.fromarray(im).save(f'red2_{tw}.png'); print(tw,idx.shape)
