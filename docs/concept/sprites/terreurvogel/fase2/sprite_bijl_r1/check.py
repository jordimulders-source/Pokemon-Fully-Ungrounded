# controle: kleine tintvlakjes, losse zwarte pixels binnenin, open randen, alpha-diff t.o.v. kale reductie
import sys, numpy as np; from PIL import Image
import r1
S=np.array(Image.open(sys.argv[1])); K=np.load('kaal.npy')
print('alpha-diff t.o.v. silhouet kale reductie:',int(((S>0)!=(K>0)).sum()))
lab,n=None,None
def leeg(y,x): return not(0<=y<64 and 0<=x<64) or S[y,x]==0
rand=[(y,x) for y in range(64) for x in range(64) if S[y,x] and any(leeg(y+a,x+b) for a,b in((-1,0),(1,0),(0,-1),(0,1)))]
licht=[(y,x,S[y,x]) for y,x in rand if S[y,x] not in(1,3,6,9,13)]
print('randpixels niet-lijntint:',licht)
kl=[]
for idx in range(2,16):
    L,n=r1.ndimage.label(S==idx)
    for k in range(1,n+1):
        ys,xs=np.where(L==k)
        if len(ys)<3: kl.append((idx,len(ys),list(zip(xs.tolist(),ys.tolist()))))
print('vlakjes <3 px (idx,n,[(x,y)]):'); [print(' ',v) for v in kl]
los=[(x,y) for y in range(64) for x in range(64) if S[y,x]==1 and (y,x) not in rand and sum(S[y+a,x+b]==1 for a,b in((-1,0),(1,0),(0,-1),(0,1)))==0]
print('losse zwarte binnenpixels (x,y):',los)
print('kleuren gebruikt:',sorted(set(S.ravel().tolist())))
