from lagen import *
a,bg,lab=model(); H,W=lab.shape
C0=np.array([62.1,128.0]); C1=np.array([182.0,36.1]); S0=np.array([74.9,64.7]); S1=np.array([189.0,91.0])
def axis(p,q):
    d=q-p; L=np.hypot(*d); u=d/L; n=np.array([-u[1],u[0]]); n= n if n[1]>0 else -n; return u,n,L
def profiel(o,u,n,t):
    res=[]
    for w in np.arange(-25,25,0.5):
        p=o+u*t+n*w; x,y=int(p[0]),int(p[1])
        res.append(lab[y,x] if 0<=x<W and 0<=y<H else 0)
    res=np.array(res); ws=np.arange(-25,25,0.5)
    i0=np.where(ws==0)[0][0]
    lo=i0
    while lo>0 and res[lo-1]!=0: lo-=1
    hi=i0
    while hi<len(res)-1 and res[hi+1]!=0: hi+=1
    return ws[lo],ws[hi],''.join('.' if c==0 else '0123456789abcdef'[c] for c in res)
if __name__=='__main__':
    u,n,L=axis(C0,C1); print('lang L',L)
    for t in range(20,150,6): print('t',t,profiel(C0,u,n,t))
    u,n,L=axis(S0,S1); print('zij L',L)
    for t in range(6,120,6): print('s',t,profiel(S0,u,n,t))
