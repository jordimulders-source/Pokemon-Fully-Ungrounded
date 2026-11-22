# Gem. helderheid van de roze modelpixels per spritepixel (zonder zwart), en zwartfractie. Gebruik: python3 lumroze.py MODEL X0 Y0 X1 Y1
import sys,numpy as np; from PIL import Image; from box import win
M=np.asarray(Image.open(sys.argv[1]).convert('RGB')).astype(float); x0,y0,x1,y1=map(int,sys.argv[2:6])
print('    '+''.join('%-7d'%x for x in range(x0,x1)))
for Y in range(y0,y1):
    s='%2d  '%Y
    for X in range(x0,x1):
        w=win(M,X,Y); l=w@[.299,.587,.114]; roze=(w[:,0]>w[:,1]+40)&(l>=55); z=(l<55).mean()
        s+=('%3d/%d  '%(l[roze].mean(),min(9,int(10*z)))) if roze.sum()>len(w)*.25 else ('  -/%d  '%min(9,int(10*z)))
    print(s)
