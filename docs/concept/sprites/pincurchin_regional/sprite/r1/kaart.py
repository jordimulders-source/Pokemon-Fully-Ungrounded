# letterkaart van het natieve raster (dichtstbijzijnde modelkleur)
from PIL import Image;import numpy as np,sys
P={'K':(2,1,1),'D':(45,32,26),'s':(80,63,55),'m':(110,91,79),'l':(131,107,97),'r':(95,26,28),'R':(140,33,37),'L':(200,65,70),'y':(242,215,80),'w':(251,240,200),'o':(234,120,54),'O':(154,65,28)}
def lab(a):
    bg=a.min(axis=2)>=200
    keys=list(P); C=np.array([P[k] for k in keys],float)
    d=((a[...,None,:].astype(float)-C)**2).sum(-1); L=np.array(keys)[d.argmin(-1)]
    L[bg]='.'; return L
if __name__=='__main__':
    a=np.asarray(Image.open(sys.argv[1] if len(sys.argv)>1 else 'natief.png').convert('RGB'))
    L=lab(a)
    print('   '+''.join(str(i//10) for i in range(a.shape[1]))); print('   '+''.join(str(i%10) for i in range(a.shape[1])))
    for j,r in enumerate(L): print('%2d '%j+''.join(r))
