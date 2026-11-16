# Onderlaag (ijskomeet-methode, factor 0,744): per spritepixel de oppervlakte-voetafdruk in natief.png.
# Genoeg donkere modelpixels (lijn) in de voetafdruk -> donkerste wint; anders oppervlaktegemiddelde. Kwantiseren naar het r13-ijzerpalet.
from PIL import Image; import numpy as np
D='/home/user/Pokemon-Fully-Ungrounded/docs/concept/sprites/spooktrein_fase3/'
N=np.array(Image.open(D+'model/natief.png').convert('RGB')).astype(float)
F=0.744
DY=0
def voet(x,y):
    x0=9+x/F; x1=9+(x+1)/F; y0=6+(y-2-DY)/F; y1=6+(y-1-DY)/F
    cells=[]
    for ny in range(int(np.floor(y0)),int(np.ceil(y1))):
        for nx in range(int(np.floor(x0)),int(np.ceil(x1))):
            w=(min(x1,nx+1)-max(x0,nx))*(min(y1,ny+1)-max(y0,ny))
            if w>0.02 and 0<=ny<99 and 0<=nx<99: cells.append((w,N[ny,nx]))
    return cells
lum=lambda c: 0.3*c[0]+0.59*c[1]+0.11*c[2]
def onderlaag(DREMPEL=80,AANDEEL=0.3):
    T=np.zeros((64,64,3)); lijn=np.zeros((64,64),bool); wit=np.zeros((64,64)); groen=np.zeros((64,64))
    for y in range(64):
        for x in range(64):
            c=voet(x,y)
            if not c: wit[y,x]=1; T[y,x]=255; continue
            W=sum(w for w,_ in c)
            wit[y,x]=sum(w for w,k in c if k.min()>215)/W
            groen[y,x]=sum(w for w,k in c if k[1]>k[0]+20 and k.min()<=215)/W
            d=sum(w for w,k in c if lum(k)<DREMPEL)/W
            ijz=[(w,k) for w,k in c if k.min()<=215 and not k[1]>k[0]+20]
            if d>=AANDEEL: T[y,x]=min((k for w,k in c),key=lum); lijn[y,x]=True
            elif ijz: Wi=sum(w for w,_ in ijz); T[y,x]=sum(w*k for w,k in ijz)/Wi
            else: T[y,x]=sum(w*k for w,k in c)/W
    return T,lijn,wit,groen
def kwant(c,P,idx):
    return idx[int(np.argmin([((c-P[i])**2).sum() for i in idx]))]
