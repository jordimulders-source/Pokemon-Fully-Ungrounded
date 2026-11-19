# Metingen per spritepixel (64-coord): lijn (lum<75), beige (huls/kop), gem. lum van de huid. Gebruikt door stap1.py.
import numpy as np; from PIL import Image
n=np.asarray(Image.open('../r10/natief.png').convert('RGB')).astype(int)
lum=.3*n[...,0]+.59*n[...,1]+.11*n[...,2]; bg=n.min(2)>=236
R,G,B=n[...,0],n[...,1],n[...,2]; beige=(G>=0.68*R)&(B<=G+12)&(lum>=75)&~bg; line=(lum<75)&~bg
F,OX,OY=2.4,76.6,14.6
def meet(r,c):
    j,i=r-1,c-17; x0,x1=OX+i*F,OX+(i+1)*F; y0,y1=OY+j*F,OY+(j+1)*F; t=0;ln=0;be=0;e=0;L=0;Lw=0
    for yy in range(int(np.floor(y0)),int(np.ceil(y1))):
        wy=min(y1,yy+1)-max(y0,yy)
        for xx in range(int(np.floor(x0)),int(np.ceil(x1))):
            wx=min(x1,xx+1)-max(x0,xx); a=wx*wy
            if a<=0: continue
            t+=a; ln+=a*line[yy,xx]; be+=a*beige[yy,xx]; e+=a*bg[yy,xx]
            if not(line[yy,xx] or beige[yy,xx] or bg[yy,xx]): L+=lum[yy,xx]*a; Lw+=a
    return ln/t, be/t, e/t, (L/Lw if Lw else 0)
