# Toonkaart: per spritepixel de modelhelderheid (natief, 3x3 gemiddeld over pixels van dezelfde kleurgroep), via de schrap-afbeelding.
import numpy as np; from PIL import Image
lab=np.load('km_lab.npy'); na=np.asarray(Image.open('natief.png').convert('RGB')).astype(float)
L=na@[.299,.587,.114]
KL={0:'O',1:'O',2:'O',3:'N',4:'N',5:'N',6:'B3',7:'M',8:'B3',9:'M',10:'K2',11:'M',12:'R',13:'B2',14:'L1',15:'G',16:'B1',17:'L2',18:'L2',19:'K1',20:'Y',21:'P'}
grp=np.full(lab.shape,'',dtype=object)
for k,v in KL.items(): grp[lab==k]={'B1':'b','B2':'b','B3':'b','N':'s','M':'s','L1':'s','L2':'s','P':'s'}.get(v,'x' if v!='O' else 'o')
# schrap-indexen opnieuw (zelfde als schrap.py)
NAMEN=['_','O','B1','B2','B3','N','M','L1','L2','P','K1','K2','R','G','Y']; I={n:i for i,n in enumerate(NAMEN)}
cl=np.zeros(lab.shape,int)
for k,v in KL.items(): cl[lab==k]=I[v]
def kies(a,axis,start=0):
    n=a.shape[axis]; keep=[]
    for b in range(start,n,4):
        grp_=list(range(b,min(b+4,n)))
        if len(grp_)<4: keep+=grp_; continue
        def diff(i,j): return (np.take(a,i,axis)!=np.take(a,j,axis)).sum()
        cost=[min(diff(g,g-1) if g>0 else 99,diff(g,g+1) if g+1<n else 99) for g in grp_]
        drop=grp_[int(np.argmin(cost))]; keep+=[g for g in grp_ if g!=drop]
    return keep
r=kies(cl,0); c=kies(cl[r],1)
assert (cl[r][:,c]==np.load('schrap.npy')).all()
def model_L(y,x,g='b'):
    R,C=r[y+5],c[x+5]; v=[L[i,j] for i in range(R-1,R+2) for j in range(C-1,C+2) if 0<=i<100 and 0<=j<100 and grp[i,j]==g]
    return np.mean(v) if v else np.nan
if __name__=='__main__':
    import sys
    o=np.load('cumbia_kls.npy'); g=sys.argv[1] if len(sys.argv)>1 else 'b'
    ids=[2,3,4] if g=='b' else [5,6,7,8,9]
    vals=[model_L(y,x,g) for y in range(64) for x in range(64) if o[y,x] in ids]
    q=np.nanpercentile(vals,[10,25,50,75,90]); print('kwantielen',q.round())
    print('   '+''.join(str(x%10) for x in range(64)))
    for y in range(64):
        s=''
        for x in range(64):
            if o[y,x] in ids:
                v=model_L(y,x,g); s+='?' if np.isnan(v) else str(int(np.clip((v-q[0])/(q[4]-q[0])*9,0,9)))
            else: s+= '.' if o[y,x]==0 else ('#' if o[y,x]==1 else '-')
        if s.strip('.'): print('%2d '%y+s)
