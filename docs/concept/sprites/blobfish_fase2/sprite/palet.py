# Palet uit de modelkleuren: k-means per kleurgroep (lijf / rode laag / bordeaux laag) op de vulkleuren van de kale reductie.
import sys, json; import numpy as np
C=np.load('kaal_rgb.npy'); A=np.load('alpha.npy'); L=np.load('lijnfrac.npy'); LB=np.load('label.npy')
T=float(sys.argv[1]) if len(sys.argv)>1 else 0.4
K={0:int(sys.argv[2]) if len(sys.argv)>2 else 8,1:3,2:3}
def feat(X): return np.c_[X@[.299,.587,.114], 2.0*(X[:,0]-X[:,1]), 2.0*(X[:,2]-X[:,1])]
SEED={0:[(237,216,218),(228,191,195),(204,158,165),(181,155,157),(144,121,123),(223,144,164),(189,110,132),(120,75,88)]}
def km(X0,k,it=60,seed=None):
    X=feat(X0)
    c=feat(np.array(seed,float)) if seed else X[np.argsort(X[:,0])[np.linspace(0,len(X)-1,k).astype(int)]]
    for _ in range(it):
        d=((X[:,None]-c[None])**2).sum(2); a=d.argmin(1)
        c=np.array([X[a==q].mean(0) if (a==q).any() else c[q] for q in range(k)])
    if it==0: return np.array(seed,float)          # zaadkleuren = gemeten modelkleuren (lippen, glans, grijs)
    return np.array([X0[a==q].mean(0) for q in range(k) if (a==q).any()])
pal={}
for g,k in K.items():
    m=(A>=0.45)&(L<T)&(LB==g); c=km(C[m],k,it=(0 if g in SEED else 60),seed=SEED.get(g)); c=c[np.argsort(-(c@[.299,.587,.114]))]
    # elke paletkleur = de dichtstbijzijnde echte modelkleur (natief) uit dezelfde groep
    from PIL import Image
    mn=np.asarray(Image.open('model_natief.png').convert('RGBA')).astype(float); lb=np.load('label_natief.npy')
    MX=mn[(mn[...,3]>0)&(lb==g)&(mn[...,:3].max(2)>=70)][:,:3]
    c=np.array([MX[np.argmin(((feat(MX)-feat(q[None]))**2).sum(1))] for q in c])
    pal[g]=c.round().astype(int).tolist(); print(g,pal[g])
json.dump(pal,open('palet.json','w'))
