# Stap 2: kale reductie van het werkmodel (99x99 natief, figuur 86x81) naar 64x60, onderkant op de bodem.
# A = oppervlak-middeling + dichtstbijzijnde modelkleur (k-means-centra van het model, Hauntflare-recept)
# B = gewogen meerderheid per modelkleur binnen de voetafdruk (zwart weegt 1,6x zodat 1-px-lijnen blijven)
import numpy as np; from PIL import Image
a=np.asarray(Image.open('model/r10_k8.png').convert('RGB')).astype(float)
fig=np.load('sprite_r1/masker.npy'); c=np.load('sprite_r1/km.npy')
yy,xx=np.where(fig); x0,y0=xx.min(),yy.min(); x1,y1=xx.max()+1,yy.max()+1
crop=a[y0:y1,x0:x1]; m=fig[y0:y1,x0:x1].astype(float)
H0,W0=m.shape; s=64/W0; W,H=64,round(H0*s)
lab=np.argmin(((crop[...,None,:]-c[None,None])**2).sum(-1),-1)
# voetafdruk-gewichten (exacte oppervlakteoverlap)
def wmat(N0,N):
    M=np.zeros((N,N0)); e=N0/N
    for i in range(N):
        lo,hi=i*e,(i+1)*e
        for j in range(int(lo),min(N0,int(np.ceil(hi)))):
            M[i,j]=max(0,min(hi,j+1)-max(lo,j))
    return M
Wy,Wx=wmat(H0,H),wmat(W0,W)
A=Wy@m@Wx.T/(Wy.sum(1)[:,None]*Wx.sum(1)[None])
C=np.stack([Wy@(crop[...,k]*m)@Wx.T for k in range(3)],2)/np.maximum(Wy@m@Wx.T,1e-9)[...,None]
outA=np.argmin(((C[...,None,:]-c[None,None])**2).sum(-1),-1)
K=len(c); dark=np.argmin(c.sum(1))
votes=np.stack([Wy@((lab==k)*m)@Wx.T for k in range(K)],-1)
votes[...,dark]*=1.6
outB=votes.argmax(-1)
# C = gewogen meerderheid per SPRITEPALETINDEX (clusters met dezelfde paletkleur tellen samen); lijntinten wegen zwaarder
import sys; sys.path.insert(0,'sprite_r1'); from gemeen import KM2P
pv=np.zeros(votes.shape[:2]+(16,))
for k in range(K): pv[...,KM2P[k]]+=np.stack([Wy@((lab==k)*m)@Wx.T],-1)[...,0]
BOOST={1:1.6,2:1.5,8:1.3}
for p,b in BOOST.items(): pv[...,p]*=b
outC_p=pv.argmax(-1)
P2K={}
for k,p in KM2P.items(): P2K.setdefault(p,k)
outC=np.vectorize(lambda p:P2K.get(p,8))(outC_p)
oy=64-H
def save(lbl,naam):
    rgb=np.full((64,64,3),255,'uint8'); al=np.zeros((64,64),bool)
    al[oy:,:]=A>=0.5
    rgb[oy:,:][A>=0.5]=c[lbl][A>=0.5].astype('uint8')
    np.save(f'sprite_r1/{naam}_lbl.npy',np.where(al,np.pad(lbl,((oy,0),(0,0)),constant_values=-1),-1))
    Image.fromarray(rgb).save(f'sprite_r1/{naam}.png')
    Image.fromarray(rgb).resize((512,512),Image.NEAREST).save(f'sprite_r1/{naam}_8x.png')
save(outA,'kaal_A'); save(outB,'kaal_B'); save(outC,'kaal_C')
print('factor',round(s,3),'maat',W,H)
