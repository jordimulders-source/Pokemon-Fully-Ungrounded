from lagen import *
a,bg,lab=model(); H,W=lab.shape
nb=~bg
# rand: niet-achtergrond met achtergrondbuur
edge=nb&(np.roll(bg,1,0)|np.roll(bg,-1,0)|np.roll(bg,1,1)|np.roll(bg,-1,1))
ys,xs=np.where(edge); P=np.stack([xs+0.5,ys+0.5],1)
def fit(c0,r0,angs):
    d=P-c0; r=np.hypot(*d.T); ang=(np.degrees(np.arctan2(-d[:,1],d[:,0]))+360)%360  # 0=rechts, 90=boven
    m=(abs(r-r0)<5)&np.any([(ang>=lo)&(ang<=hi) for lo,hi in angs],0)
    p=P[m]; A=np.c_[2*p,np.ones(len(p))]; b=(p**2).sum(1); sol=np.linalg.lstsq(A,b,rcond=None)[0]
    c=sol[:2]; R=np.sqrt(sol[2]+(c**2).sum()); res=np.hypot(*(p-c).T)-R
    return c,R,len(p),abs(res).max()
if __name__=='__main__':
    print('voorbol',fit(np.array([57.5,121]),26.5,[(100,330)]))
    print('verbol',fit(np.array([190,45]),24,[(-10,150),(350,360)]))
    print('linksoogbol',fit(np.array([73,63]),10.5,[(90,270)]))
    print('rechtsoogbol',fit(np.array([189,91]),11,[(-90,100),(270,360)]))
