# per spritepixel de natieve modelcellen (3x3) van het r17-pixelblad (fase y7/x32, figuur op x7/y3)
import numpy as np; from PIL import Image
a=np.asarray(Image.open('../r1/natief.png').convert('RGB')).astype(float); L=a@[.299,.587,.114]; bg=a.min(2)>225
R,G,B=a[...,0],a[...,1],a[...,2]; BR=(~bg)&(R>B+28)&(R>G+20)
OX,OY,PX,PY=7,3,32,7
SEPL=65
def cel(x,y):
    ny=PY+3*(y-OY); nx=PX+3*(x-OX)
    if ny<0 or nx<0 or ny+3>200 or nx+3>200: return None
    s=(slice(ny,ny+3),slice(nx,nx+3)); b=bg[s]; l=L[s]; br=BR[s]
    return dict(bg=int(b.sum()), donker=int(((~b)&(l<45)).sum()), bruin=int(br.sum()),
                Lbruin=float(l[br].mean()) if br.any() else 0., Lfig=float(l[~b].mean()) if (~b).any() else 0.,
                Lmauve=float(l[(~b)&~br&(l>=45)].mean()) if ((~b)&~br&(l>=45)).any() else 0., licht=int(((~b)&(l>=140)).sum()), sep=int(((~b)&(l<SEPL)).sum()))
