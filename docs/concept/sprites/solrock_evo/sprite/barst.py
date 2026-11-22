# Barstkaart: zwarte natieve modelpixels (lum<20) in de kern geprojecteerd op het spriteraster ("donkerste wint", >=N natieve px per spritepixel)
import numpy as np; from PIL import Image; import sys
N=int(sys.argv[1]) if len(sys.argv)>1 else 2
n=np.asarray(Image.open('natief512.png')).astype(int); l=n.mean(2)
S=11.87; X0=138-0.5*S; Y0=107-1.2*S; p=5.12; ph=4.25
cnt=np.zeros((64,64),int)
for j in range(n.shape[0]):
    for i in range(n.shape[1]):
        if l[j,i]<20:
            X=ph+p/2+i*p; Y=ph+p/2+j*p
            if np.hypot(X-501.5,Y-496)<188:
                sx=int((X-X0)//S); sy=int((Y-Y0)//S)
                if 0<=sx<64 and 0<=sy<64: cnt[sy,sx]+=1
np.save('barst.npy',cnt>=N)
