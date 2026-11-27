# Gemini-plaatje (1024) -> natief raster 100x100: per cel lijn (zwart) als >=30% zwart, anders mediaan van de rest
import sys
from PIL import Image
import numpy as np
def natief(f,n=100,frac=0.3):
    a=np.array(Image.open(f).convert('RGB')).astype(int)
    g=1024/n; out=np.zeros((n,n,3),int)
    for r in range(n):
        for c in range(n):
            blk=a[int(r*g):int((r+1)*g),int(c*g):int((c+1)*g)].reshape(-1,3)
            k=blk.sum(1)<150
            if k.mean()>=frac: out[r,c]=np.median(blk[k],0)
            else:
                rest=blk[~k]; wit=rest.sum(1)>720
                out[r,c]=np.median(rest[wit],0) if wit.mean()>0.5 else np.median(rest[~wit],0)
    return out.astype('uint8')
if __name__=='__main__':
    for f in sys.argv[1:-1]:
        Image.fromarray(natief(f)).resize((800,800),Image.NEAREST).save(sys.argv[-1]+'/'+f.split('/')[-1].replace('.png','_nat8.png'))
