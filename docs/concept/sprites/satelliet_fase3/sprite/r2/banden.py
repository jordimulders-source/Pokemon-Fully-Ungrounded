# Bandvormen uit het model fitten: per band t_c(w)=a+b*w+c*sqrt(1-(w/r)^2) en breedte, in buiscoordinaten.
from lagen import *
a_,bg,lab=model(); H,W=lab.shape
yy,xx=np.mgrid[0:H,0:W]; PX=xx+0.5; PY=yy+0.5
LANG=dict(o=np.array([62.1,128.0]),q=np.array([182.0,36.1]))
ZIJ=dict(o=np.array([74.9,64.7]),q=np.array([189.0,91.0]))
def asvec(A):
    d=A['q']-A['o']; L=np.hypot(*d); u=d/L; n=np.array([-u[1],u[0]]); n=n if n[1]>0 else -n; return u,n,L
KL={'P':[6,7,8],'N':[1,2,3,4,5]}
def fitband(A,t0,t1,soort,r):
    u,n,L=asvec(A); o=A['o']
    t=(PX-o[0])*u[0]+(PY-o[1])*u[1]; w=(PX-o[0])*n[0]+(PY-o[1])*n[1]
    m=np.isin(lab,KL[soort])&(t>=t0)&(t<=t1)&(np.abs(w)<=r)
    tw=t[m]; ww=w[m]
    bins=np.arange(-r,r+0.01,2.0); cs=[];wsx=[];br=[]
    for b0 in bins:
        k=(ww>=b0)&(ww<b0+2)
        if k.sum()>=3: cs.append(np.median(tw[k])); wsx.append(b0+1); br.append(np.percentile(tw[k],90)-np.percentile(tw[k],10)+1)
    cs=np.array(cs); wsx=np.array(wsx); q=np.clip(np.abs(wsx)/r,0,1)
    A_=np.c_[np.ones_like(wsx),wsx,np.sqrt(1-q*q)]; sol=np.linalg.lstsq(A_,cs,rcond=None)[0]
    res=cs-A_@sol
    return sol,float(np.median(br)),len(cs),float(np.abs(res).max())
BANDEN={
 'lang':[('voorkraag',10,30,'P',17),('voorband',40,58,'N',15),('hubkraag_voor',60,80,'P',17),('hubkraag_achter',88,112,'P',16),('achterband',118,134,'N',14),('verkraag',134,152,'P',16)],
 'zij':[('linkskraag',3,17,'P',10),('hubkraag_links',28,52,'P',11),('hubkraag_rechts',62,82,'P',11),('rechtskraag',96,112,'P',11)],
}
if __name__=='__main__':
    out={}
    for asn,lst in BANDEN.items():
        A=LANG if asn=='lang' else ZIJ
        for nm,t0,t1,so,r in lst:
            sol,b,n,mx=fitband(A,t0,t1,so,r); out[nm]=(asn,list(map(float,sol)),b,so,r)
            print(nm,np.round(sol,2),'breedte',round(b,1),'bins',n,'maxres',round(mx,2))
    import json; json.dump(out,open('banden.json','w'),indent=1)
