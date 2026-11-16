# zones (wiel, schoorsteen, rail, midden) door dezelfde schrap + 2x-reductie -> 64x64 (zelfde plaatsing als plaats.py)
import numpy as np, ast; from PIL import Image
a=np.asarray(Image.open('natief_samen.png').convert('RGB')).astype(int); fg=a.min(2)<225; ys,xs=np.where(fg)
Z=np.load('zones.npy')[:, ys.min()-1:ys.max()+2, xs.min()-1:xs.max()+2]
r=open('schrap.txt').read().split('\n'); rows=ast.literal_eval(r[0]); cols=ast.literal_eval(r[1])
Z=np.delete(np.delete(Z,rows,1),cols,2)
F=np.delete(np.delete(fg[ys.min()-1:ys.max()+2, xs.min()-1:xs.max()+2],rows,0),cols,1)
OY,OX=1,0; h=(Z.shape[1]-OY)//2; w=(Z.shape[2]-OX)//2
Zh=np.zeros((4,h,w),bool); Fh=np.zeros((h,w),bool)
for j in range(h):
    for i in range(w):
        sl=(slice(OY+2*j,OY+2*j+2),slice(OX+2*i,OX+2*i+2))
        for k in range(4): Zh[k,j,i]=Z[k][sl].sum()>=2
        Fh[j,i]=F[sl].sum()>=2
o=np.load('half.npy'); 
yy,xx=np.where(Fh)  # half.npy is bijgesneden op o>0; zelfde bijsnijding via o
np.save('zones_half.npy',Zh)
