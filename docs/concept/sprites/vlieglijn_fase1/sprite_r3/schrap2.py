# Kale reductie v2: zoals schrap.py, maar het potengebied (model-y >= GRENS) krijgt een eigen kolomkeuze
# (zelfde vensters, dus elk kenmerk schuift hoogstens binnen zijn venster), gericht op het heel houden van
# kabelomlijning, glanslijn, ringen en koper. Alleen modelpixels, niets getekend.
import numpy as np, sys
cl=np.load('ncl.npy'); X0,Y0,X1,Y1=17,20,84,82; GRENS=int(sys.argv[1]) if len(sys.argv)>1 else 52
c=cl[Y0:Y1,X0:X1].copy()
def maakverlies(WT):
    def verlies(m,i):
        k=m[:,i]; L=m[:,i-1] if i>0 else np.full_like(k,-1); R=m[:,i+1] if i<m.shape[1]-1 else np.full_like(k,-1)
        lost=(k!=L)&(k!=R); return (WT[k]*lost).sum()+0.3*((k!=L)|(k!=R)).sum()
    return verlies
def kies(m,doel,verlies):
    n=m.shape[1]; weg=n-doel; grens=np.round(np.linspace(0,n,weg+1)).astype(int); out=[]
    for s in range(weg):
        lo,hi=grens[s],grens[s+1]
        cand=[i for i in range(lo,hi) if not out or i>out[-1]+1] or list(range(lo,hi))
        out.append(min(cand,key=lambda i:verlies(m,i)))
    return out
W1=np.ones(16); W1[[13,14,15]]=6; W1[1]=2; W1[10]=2
W2=np.ones(16); W2[[14,15]]=6; W2[1]=3; W2[9]=3; W2[[10,11]]=3
kc=kies(c,50,maakverlies(W1)); c2=np.delete(c,kc,axis=1)
kr=kies(c2.T,46,maakverlies(W1))
g=GRENS-Y0
kcl=kies(c[g:],50,maakverlies(W2)); c2l=np.delete(c,kcl,axis=1)
out=np.vstack([c2[:g],c2l[g:]]); out=np.delete(out,kr,axis=0)
print('kol boven',[i+X0 for i in kc]); print('kol poten',[i+X0 for i in kcl]); print('rijen',[i+Y0 for i in kr])
keepy=[j+Y0 for j in range(c.shape[0]) if j not in kr]; print('sprite-rij van grens:',keepy.index(GRENS) if GRENS in keepy else None)
import PIL.Image as I
a=np.asarray(I.open('natief.png').convert('RGB'))[Y0:Y1,X0:X1]
up=np.delete(a,kc,axis=1); lo=np.delete(a,kcl,axis=1); rgb=np.vstack([up[:g],lo[g:]]); rgb=np.delete(rgb,kr,axis=0)
I.fromarray(rgb).save('model_zelfde_schaal.png')   # het model zelf, met dezelfde geschrapte rijen/kolommen
np.savetxt('kaal_r3.txt',out,fmt='%2d'); print(out.shape,(out>0).sum())
