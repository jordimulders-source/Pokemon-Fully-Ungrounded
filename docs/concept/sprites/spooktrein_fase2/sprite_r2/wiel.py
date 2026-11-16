# Wielen opnieuw uit het model: per spritepixel het natieve blok; omlijning bij >=30% dekking, anders de grijstint
# (licht/midden/donker) die het model in dat blok het meest heeft. Print het resultaat; niets met de hand.
import numpy as np; from PIL import Image
a=np.asarray(Image.open('natief.png').convert('RGB')).astype(int); L=a@[0.3,0.59,0.11]
s,X0,Y0,oy,XC,k=[float(v) for v in open('r1.meta').read().split()]
def tone(px):
    l=px@[0.3,0.59,0.11]; r,g,b=px
    if l<45: return 1
    if abs(r-b)>25 and not (b>r): return 0          # hout: niet van het wiel
    if l>150: return 12
    if l>100: return 13
    return 14
def sample(nx0,nx1,ny0,ny1):
    res={}
    for j in range(int(np.floor((ny0-Y0)*s+oy)),int(np.ceil((ny1-Y0)*s+oy))):
        for i in range(int(np.floor((nx0-X0)*s)),int(np.ceil((nx1-X0)*s))):
            xs=X0+(i+(np.arange(6)+0.5)/6)/s; ys=Y0+(j-oy+(np.arange(6)+0.5)/6)/s
            t=[tone(a[int(y),int(x)]) for y in ys for x in xs if nx0<=x<nx1+1 and ny0<=y<ny1+1 and a[int(y),int(x)].min()<225]
            if len(t)<12: continue
            t=np.array(t)
            if (t==1).mean()>=0.3: res[(j,i)]=1; continue
            t=t[(t!=1)&(t!=0)]
            if len(t)==0: res[(j,i)]=1; continue
            u,c=np.unique(t,return_counts=True); res[(j,i)]=int(u[c.argmax()])
    return res
if __name__=='__main__':
    for box in ((38,51,109,122),(69,83,110,122)):
        r=sample(*box); ys=sorted({p[0] for p in r}); xs=sorted({p[1] for p in r})
        print(box,'sprite x',xs[0],'-',xs[-1])
        for y in ys: print(y,''.join({1:'O',12:'g',13:'G',14:'s'}.get(r.get((y,x),0),'.') for x in xs))
