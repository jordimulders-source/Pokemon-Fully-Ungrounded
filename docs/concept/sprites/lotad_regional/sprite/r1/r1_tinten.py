# Meet de kleuren per onderdeel in r1/gemini_r1.png (maskers uit r8/kleur_r1.py, natief raster) -> clusters per onderdeel.
import numpy as np; from PIL import Image
a=np.asarray(Image.open('natief_r1.png').convert('RGB')).astype(float)
R,G,B=a[...,0],a[...,1],a[...,2]; L=0.3*R+0.59*G+0.11*B; sat=a.max(2)-a.min(2)
H,W=L.shape; y,x=np.mgrid[0:H,0:W]; X=5.83+x*4.266; Y=5.83+y*4.27
w=(L>222)&(sat<40); ln=L<62; body=~w&~ln
b={}
b['hoed']=body&(Y<232)&(R>G+45)            # alleen terracotta, niet het lichte vlechtwerk
b['snavel']=body&(X>=385)&(X<=480)&(Y>=262)&(Y<=320)&(G>R-40)&(B<130)&(R>150)
b['poten']=body&(Y>385)&(R>G+35)&~b['snavel']
b['kraag']=body&(Y>=300)&(Y<=440)&(R-G<35)&~b['snavel']&~b['poten']&(Y>=232)
b['kop']=body&(Y>=236)&(Y<=330)&(R>G+35)&~b['snavel']
def km(P,k,it=30):
    P=P[np.argsort(P@[0.3,0.59,0.11])]; C=P[np.linspace(0,len(P)-1,k).astype(int)].copy()
    for _ in range(it):
        d=((P[:,None]-C[None])**2).sum(2); l=d.argmin(1)
        for j in range(k):
            if (l==j).any(): C[j]=P[l==j].mean(0)
    l=((P[:,None]-C[None])**2).sum(2).argmin(1); n=np.bincount(l,minlength=k)
    o=np.argsort(C@[0.3,0.59,0.11]); return C[o].round().astype(int),n[o]
if __name__=='__main__':
    for k_ in b:
        C,n=km(a[b[k_]],4); print(k_,b[k_].sum(),[ (tuple(c),int(m)) for c,m in zip(C,n)])
