# hulpje: klassekaart (64x64) -> png op schaal, met modelpalet
import numpy as np, sys
from PIL import Image
P=list(np.load('nat_pal.npy').round().astype(int))+[[220,190,80],[120,90,140],[250,252,252]]
def render(M,schaal=12,pal=None):
    pal=pal if pal is not None else P
    im=Image.new('RGB',(64,64),(255,255,255)); px=im.load()
    for j in range(64):
      for i in range(64):
        if M[j,i]>=0: px[i,j]=tuple(int(v) for v in pal[M[j,i]])
    return im.resize((64*schaal,64*schaal),Image.NEAREST)
if __name__=='__main__':
    L=np.load('L.npy'); V=np.load('V.npy'); M=np.where(L>=0,L,V)
    render(M).save(sys.argv[1])
