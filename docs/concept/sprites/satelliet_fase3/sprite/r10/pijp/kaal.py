# Kale reductie van het bevroren model (r13b) naar 64 px breed.
# Oppervlakgewogen per paletklasse (klassegewicht voor dunne/donkere onderdelen), palet uit het model.
import sys
from common import *
PAL=[(0,0,0),
 (24,19,36),(41,38,69),(63,52,90),(84,74,112),(106,88,130),
 (120,78,143),(150,104,168),(182,132,196),
 (52,100,102),(80,160,158),
 (140,120,163),(186,175,205),(209,198,221),(231,220,238),(250,248,252)]
WGT={0:1.0,1:1.8,2:1.4,3:1.0,4:2.2,5:2.0,6:1.5,7:1.3,8:1.3,9:2.0,10:2.0,11:1.0,12:1.0,13:1.0,14:1.0,15:1.0}
def overlap(n_out,start,s,n_in):
    W=np.zeros((n_out,n_in))
    for i in range(n_out):
        a0=start+i*s; a1=a0+s
        for j in range(int(np.floor(a0)),int(np.ceil(a1))):
            if 0<=j<n_in:
                W[i,j]=max(0,min(a1,j+1)-max(a0,j))
    return W
def reduce(phx=0.0,phy=0.0,OUTW=64):
    a,bg=load(); H,Wd,_=a.shape
    ys,xs=np.where(~bg); x0,x1,y0,y1=xs.min(),xs.max()+1,ys.min(),ys.max()+1
    if VAR=='r10': x0,x1,y0,y1=3,228,3,156   # r10: zelfde kader als r8/r9 (schaal 3,515625), ook als een paneel binnen het kader krimpt
    s=(x1-x0)/OUTW
    oh=int(np.ceil((y1-y0)/s))
    pal=np.array(PAL[1:],float)
    d=((a[:,:,None,:]-pal[None,None])**2).sum(3); lab=d.argmin(2)+1; lab[bg]=0
    Wx=overlap(OUTW,x0+phx,s,Wd); Wy=overlap(oh,y0+phy,s,H)
    best=None
    sc=np.zeros((16,oh,OUTW))
    for c in range(16):
        sc[c]=Wy@(lab==c).astype(float)@Wx.T*WGT[c]
    out=sc.argmax(0)
    # transparant alleen als achtergrond > helft van het vak
    cov_bg=sc[0]/WGT[0]/(s*s)
    out[(cov_bg<0.5)&(out==0)]=sc[1:].argmax(0)[(cov_bg<0.5)&(out==0)]+1
    out[cov_bg>=0.6]=0
    return out,s
def save(idx,path,top=None):
    h=idx.shape[0]
    if top is None: top=(64-h)//2+3
    full=np.zeros((64,64),np.uint8); full[top:top+h,:idx.shape[1]]=idx
    im=Image.fromarray(full,'P'); flat=[v for c in PAL for v in c]; im.putpalette(flat+[0]*(768-len(flat)))
    im.save(path,transparency=0); return full
if __name__=='__main__':
    out,s=reduce()
    print('schaal',s,'maat',out.shape)
    save(out.astype(np.uint8),'kaal.png')
