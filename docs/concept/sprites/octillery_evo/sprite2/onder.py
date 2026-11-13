# onderlaag: model per spritecel geklasseerd -> onder.txt (kale onderlaag, daarna handwerk in bouw.py)
import cfg,numpy as np,sys
c=cfg.model(); L=c.mean(2); fg=cfg.fgmask(c)
yel=(c[...,0]>150)&(c[...,1]>120)&(c[...,2]<c[...,1]-25)&fg
dark=(L<45)&fg
red=fg&~yel&~dark
a=np.zeros((64,64),int); info={}
for y in range(64):
  for x in range(64):
    sl=cfg.cell(x,y)
    if sl[0].start<0 or sl[1].start<0 or sl[0].stop>1024 or sl[1].stop>1024: continue
    f=fg[sl].mean()
    if f<0.5: continue
    n=fg[sl].sum(); D=dark[sl].sum()/n; Y=yel[sl].sum()/n
    if D>=0.45: a[y,x]=1; continue
    if Y>=0.35:
        ly=L[sl][yel[sl]].mean(); a[y,x]=11 if ly>215 else 10 if ly>165 else 9; continue
    r=red[sl]
    if r.sum()==0: a[y,x]=1; continue
    l=np.median(L[sl][r])
    a[y,x]=3 if l<58 else 4 if l<82 else 5 if l<112 else 6
    if D>=0.28 and a[y,x]>3: a[y,x]-=1
cfg.write(a,'onder.txt')
