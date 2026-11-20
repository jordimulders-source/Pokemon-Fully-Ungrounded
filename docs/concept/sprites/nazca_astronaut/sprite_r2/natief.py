# Natief raster (pitch 10.24, fase 9.25) van een Gemini-plaatje -> 100x100 (mediaan 5x5 per cel)
import sys; from PIL import Image; import numpy as np
def natief(path, p=10.24, ph=9.25):
    a=np.asarray(Image.open(path).convert('RGB')).astype(int)
    cs=np.arange(ph+p/2,1024,p); n=len(cs); out=np.zeros((n,n,3),'uint8')
    for j,y in enumerate(cs):
        for i,x in enumerate(cs):
            y0,x0=int(y)-2,int(x)-2
            out[j,i]=np.median(a[y0:y0+5,x0:x0+5].reshape(-1,3),axis=0)
    return out
if __name__=='__main__':
    Image.fromarray(natief(sys.argv[1])).save(sys.argv[2])
