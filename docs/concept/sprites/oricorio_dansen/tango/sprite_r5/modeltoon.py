# model_L(y,x): modelhelderheid (gemiddelde van het 2x2-natieve blok) voor spritepixel (y,x) in 64x64-coördinaten.
import numpy as np; from PIL import Image; from schrap import kies
nat=np.asarray(Image.open('natief.png')).astype(float)@[.299,.587,.114]
cl=np.load('klassen_natief.npy'); r=kies(cl,0,1); c=kies(cl[r],1,0)
o=cl[r][:,c]; ys,xs=np.where(o>0); Y0,X0=ys.min(),xs.min(); h,w=ys.max()-Y0+1,xs.max()-X0+1
DY=(61-h+1)-Y0; DX=(64-w)//2-X0
def model_L(y,x):
    j,i=y-DY,x-DX
    if not(0<=j<len(r) and 0<=i<len(c)): return 255
    a,b=r[j],c[i]
    return nat[a:a+2,b:b+2].mean()
L=np.array([[model_L(y,x) for x in range(64)] for y in range(64)])
if __name__=='__main__':
    np.save('model_L.npy',L)
    o=np.load('basis.npy'); assert ((L<215)==(o>0)).mean()>0.95, ((L<215)==(o>0)).mean()
    print('ok', ((L<215)==(o>0)).mean())
