# Alternatieve kale reductie: vlakgemiddelde per doelpixel (oppervlakte-gewogen stemming over de natieve modelpixels die hij bedekt),
# met voorrang voor lijnen (zwart/rode lijn/olijflijn) zodra die >= DREMPEL van de cel bedekken, zodat 1-px-lijnen niet breken.
# Elke uitkomst is een modelkleur (geen middeling van RGB). Figuur 75x91 -> 51x62, zelfde plaatsing als kaal.py.
import numpy as np, sys
from gemeen import opslaan
q=np.load('kwant.npy'); ys,xs=np.where(q>0); f=q[ys.min():ys.max()+1,xs.min():xs.max()+1]
H,W=f.shape; TW,TH=51,62; DREMPEL=float(sys.argv[1]) if len(sys.argv)>1 else 0.30
LIJN=[1,2,8]
out=np.zeros((TH,TW),int)
for j in range(TH):
    y0,y1=j*H/TH,(j+1)*H/TH
    for i in range(TW):
        x0,x1=i*W/TW,(i+1)*W/TW
        w={}
        for yy in range(int(y0),int(np.ceil(y1))):
            hy=min(y1,yy+1)-max(y0,yy)
            for xx in range(int(x0),int(np.ceil(x1))):
                hx=min(x1,xx+1)-max(x0,xx); k=f[yy,xx]; w[k]=w.get(k,0)+hx*hy
        A=sum(w.values())
        if w.get(0,0)>=0.5*A: out[j,i]=0; continue
        lw={k:v for k,v in w.items() if k in LIJN}
        if lw and sum(lw.values())>=DREMPEL*A: out[j,i]=max(lw,key=lw.get); continue
        nw={k:v for k,v in w.items() if k!=0}
        out[j,i]=max(nw,key=nw.get)
o=np.zeros((64,64),int); X0=(64-TW)//2; Y0=63-TH; o[Y0:63,X0:X0+TW]=out
np.save('kaal_vlak.npy',o); opslaan(o,'kaal_vlak.png'); print('px',(o>0).sum())
