# Kale reductie gekwantiseerd naar het modelpalet (per kleurgroep dichtstbijzijnde kleur) -> kaal.png / kaal.npy (64x64 indexen)
import json; import numpy as np; from PIL import Image
T=0.4; OX,OY=1,17
C=np.load('kaal_rgb.npy'); LM=np.load('lijncentra.npy'); LM2=np.load('lijncentra2.npy'); A=np.load('alpha.npy'); L=np.load('lijnfrac.npy'); LB=np.load('label.npy')
pal=json.load(open('palet.json')); cols=[[0,0,0]]+[[16,16,16]]; grp={}
for g in ('0','1','2'):
    grp[int(g)]=list(range(len(cols),len(cols)+len(pal[g]))); cols+=pal[g]
P=np.array(cols,float)
def feat(X): return np.c_[X@[.299,.587,.114], 2.0*(X[:,0]-X[:,1]), 2.0*(X[:,2]-X[:,1])]
H,W=A.shape; o=np.zeros((64,64),int)
for j in range(H):
    for i in range(W):
        if A[j,i]<0.45: continue
        if LM[j,i] or L[j,i]>=T: o[OY+j,OX+i]=1; continue
        if LM2[j,i] and LB[j,i]==0: o[OY+j,OX+i]=grp[0][-1]; continue
        ix=grp[LB[j,i]]; o[OY+j,OX+i]=ix[int(np.argmin(((feat(P[ix])-feat(C[j,i][None]))**2).sum(1)))]
np.save('kaal.npy',o); json.dump({'cols':cols,'grp':grp},open('kaal_palet.json','w'))
def opslaan(o,cols,naam):
    im=Image.fromarray(o.astype(np.uint8),'P'); pl=sum(cols,[]); im.putpalette(pl); im.save(naam,transparency=0)
    rgb=np.array(cols,'uint8')[o]; rgb[o==0]=255
    Image.fromarray(rgb).resize((512,512),Image.NEAREST).save(naam.replace('.png','_8x.png'))
opslaan(o,[list(map(int,c)) for c in cols],'kaal.png'); print(len(cols),'kleuren')
