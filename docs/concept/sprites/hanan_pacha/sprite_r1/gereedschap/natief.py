# Natief raster terughalen: r7 pitch 6,40 (1024/160), randfase 5,5 -> celgrenzen 6,5+6,4k. Mediaan van 3x3 in het celmidden.
import sys, numpy as np; from PIL import Image
IN,OUT,P,E=sys.argv[1],sys.argv[2],float(sys.argv[3]),float(sys.argv[4])
a=np.asarray(Image.open(IN).convert('RGB')).astype(int); H,W=a.shape[:2]
x0=E+1-P*np.ceil((E+1)/P)
xs=[x0+P/2+k*P for k in range(200) if x0+P/2+k*P<W]
ys=xs if H==W else [x0+P/2+k*P for k in range(200) if x0+P/2+k*P<H]
out=np.zeros((len(ys),len(xs),3),'uint8')
for j,y in enumerate(ys):
    for i,x in enumerate(xs):
        yi,xi=int(round(y-0.5)),int(round(x-0.5))
        b=a[max(0,yi-1):yi+2,max(0,xi-1):xi+2].reshape(-1,3)
        out[j,i]=np.median(b,axis=0)
Image.fromarray(out).save(OUT); print(len(xs),len(ys))
