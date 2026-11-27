# Natief raster van het model terughalen: pitch 1408/240 = 5,867 (pitch.py: pieken bij 5,87 en 11,73 -> p=5,87),
# fase x 4,5 / y 5,0. Per cel de mediaan van het celbinnenste. Niets getekend.
import os, numpy as np; from PIL import Image
D=os.path.dirname(os.path.abspath(__file__)); MODEL=os.path.join(D,'..','model.png')
P=1408/240; PHX,PHY=4.5,5.0
def natief():
    a=np.asarray(Image.open(MODEL).convert('RGB')).astype(int)
    W=240; H=int(768/P); out=np.zeros((H,W,3),int)
    for j in range(H):
        for i in range(W):
            x0=int(round(i*P+PHX-P)); y0=int(round(j*P+PHY-P))
            blk=a[max(0,y0+1):y0+int(P)-1, max(0,x0+1):x0+int(P)-1]
            out[j,i]=np.median(blk.reshape(-1,3),0) if blk.size else 255
    return out
if __name__=='__main__':
    n=natief(); Image.fromarray(n.astype('uint8')).save(os.path.join(D,'..','natief.png')); print(n.shape)
