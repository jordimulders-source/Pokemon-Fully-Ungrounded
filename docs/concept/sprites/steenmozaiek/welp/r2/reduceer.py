# Stap 2: natief -> palet uit het model (<=15 kleuren, k-means, centra = echte natieve kleuren) -> verkleinen
# met vlakgemiddelde (alleen figuurpixels) + dichtstbijzijnde paletkleur; masker = bedekking >= 0,45.
import sys; from PIL import Image; import numpy as np
from collections import deque
n=np.asarray(Image.open('natief.png').convert('RGB')).astype(float); H,W,_=n.shape
# achtergrond = floodfill van de rand over bijna-wit (tanden en oogwit liggen binnen de omlijning)
bg=np.zeros((H,W),bool); light=n.min(axis=2)>205; q=deque()
for y in range(H):
    for x in (0,W-1): q.append((y,x))
for x in range(W):
    for y in (0,H-1): q.append((y,x))
while q:
    y,x=q.popleft()
    if 0<=y<H and 0<=x<W and not bg[y,x] and light[y,x]:
        bg[y,x]=True; q.extend([(y+1,x),(y-1,x),(y,x+1),(y,x-1)])
# ingesloten achtergrondgaten (wit vlak tussen kin en poot, 80 px) ook achtergrond; tanden/oogwit zijn <= 9 px
seen=bg.copy()
for y0 in range(H):
    for x0 in range(W):
        if light[y0,x0] and not seen[y0,x0]:
            st=[(y0,x0)]; seen[y0,x0]=True; cl=[]
            while st:
                y,x=st.pop(); cl.append((y,x))
                for yy,xx in ((y+1,x),(y-1,x),(y,x+1),(y,x-1)):
                    if 0<=yy<H and 0<=xx<W and light[yy,xx] and not seen[yy,xx]: seen[yy,xx]=True; st.append((yy,xx))
            if len(cl)>40:
                for y,x in cl: bg[y,x]=True
fig=~bg
np.save('masker_natief.npy',fig)
# palet: k-means op figuurpixels, 15 centra, elk centrum vervangen door de dichtstbijzijnde echte natieve kleur
px=n[fig]; rng=np.random.default_rng(1)
K=15
# init: farthest-point zodat kleine groepen (tong, tand, oog) een eigen centrum krijgen
C=[px[rng.integers(len(px))]]
for _ in range(K-1):
    d=np.min([((px-c)**2).sum(1) for c in C],axis=0); C.append(px[np.argmax(d)])
C=np.array(C)
for it in range(40):
    lab=np.argmin(((px[:,None]-C[None])**2).sum(2),1)
    C=np.array([px[lab==k].mean(0) if (lab==k).any() else C[k] for k in range(K)])
uniq=np.unique(px,axis=0)
PAL=np.array([uniq[np.argmin(((uniq-c)**2).sum(1))] for c in C]).astype(int)
cnt=[(lab==k).sum() for k in range(K)]
order=np.argsort(PAL.sum(1)); PAL=PAL[order]; cnt=np.array(cnt)[order]
if __name__=="__main__":
    for p,c in zip(PAL,cnt): print(tuple(p),c)
np.save('palet.npy',PAL)
q=np.argmin(((n[:,:,None]-PAL[None,None])**2).sum(3),2)
nq=PAL[q].astype('uint8'); nq[bg]=255
Image.fromarray(nq).save('natief_q.png')
# figuurbbox natief
yy,xx=np.where(fig); X0,X1,Y0,Y1=xx.min(),xx.max()+1,yy.min(),yy.max()+1
def wts(n0,n1,t):
    L=n1-n0; s=L/t; Wm=np.zeros((t,int(np.ceil(n1))+1))
    for i in range(t):
        a,b=n0+i*s,n0+(i+1)*s
        for k in range(int(np.floor(a)),int(np.ceil(b))):
            Wm[i,k]=max(0,min(b,k+1)-max(a,k))
    return Wm[:,:W if Wm.shape[1]>=W else Wm.shape[1]]
def reduce(tw):
    th=int(round(tw*(Y1-Y0)/(X1-X0)))
    Wx=wts(X0,X1,tw)[:, :W]; Wy=wts(Y0,Y1,th)[:, :H]
    if Wx.shape[1]<W: Wx=np.pad(Wx,((0,0),(0,W-Wx.shape[1])))
    if Wy.shape[1]<H: Wy=np.pad(Wy,((0,0),(0,H-Wy.shape[1])))
    f=fig.astype(float); area=np.outer(Wy.sum(1),Wx.sum(1))
    cov=Wy@f@Wx.T/area
    col=np.stack([Wy@(nq[:,:,c]*f)@Wx.T for c in range(3)],2)/np.maximum(Wy@f@Wx.T,1e-9)[:,:,None]
    idx=np.argmin(((col[:,:,None]-PAL[None,None])**2).sum(3),2)+1
    idx[cov<0.45]=0
    return idx
if __name__=='__main__':
    for tw in (46,50,54):
        idx=reduce(tw); np.save(f'red_{tw}.npy',idx)
        im=np.zeros(idx.shape+(4,),'uint8'); m=idx>0
        im[m,:3]=PAL[idx[m]-1]; im[m,3]=255
        Image.fromarray(im).save(f'red_{tw}.png'); print(tw,idx.shape)
