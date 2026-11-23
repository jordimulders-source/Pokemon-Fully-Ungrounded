# kaart.py out.png a.png b.png ... : zwarte pixels rood (rand) / magenta (binnen), rest vervaagd, 8x
import sys,numpy as np; from PIL import Image
from meet import zwart_idx
def kaart(f,k=8):
    im=Image.open(f); a=np.array(im).astype(int); rgb=np.array(im.convert('RGB')).astype(float)
    Z=zwart_idx(im); fig=a>0; H,W=a.shape
    out=np.full((H,W,3),255.0); out[fig]=rgb[fig]*0.35+255*0.65
    for y,x in np.argwhere(np.isin(a,Z)&fig):
        r=any(not(0<=x+dx<W and 0<=y+dy<H) or a[y+dy,x+dx]==0 for dx,dy in((1,0),(-1,0),(0,1),(0,-1)))
        out[y,x]=(220,0,0) if r else (40,40,40)
    return Image.fromarray(out.astype('uint8')).resize((W*k,H*k),Image.NEAREST)
if __name__=='__main__':
    ims=[kaart(f) for f in sys.argv[2:]]
    O=Image.new('RGB',(sum(i.width+16 for i in ims),max(i.height for i in ims)),'white'); x=0
    for i in ims: O.paste(i,(x,0)); x+=i.width+16
    O.save(sys.argv[1])
