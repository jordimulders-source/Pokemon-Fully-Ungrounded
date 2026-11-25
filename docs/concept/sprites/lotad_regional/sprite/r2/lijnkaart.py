# Lijnkaart van de kraag in het model: natieve kraagpixel die duidelijk donkerder is dan zijn kraagomgeving
# (helderheid < mediaan van de kraagpixels in 5x5 - DREMPEL) en dun (<= 4 van zulke pixels in de 3x3) = scheidingslijn.
import numpy as np; from PIL import Image
from klassen import klassen_r8
DREMPEL=22
def lijnkaart():
    a,c,L=klassen_r8(); H,W=c.shape; lk=np.zeros((H,W),bool)
    for v in range(2,H-2):
        for u in range(2,W-2):
            if c[v,u]!=5: continue
            blok=L[v-2:v+3,u-2:u+3][c[v-2:v+3,u-2:u+3]==5]
            if L[v,u]<np.median(blok)-DREMPEL: lk[v,u]=True
    dun=lk.copy()
    for v in range(1,H-1):
        for u in range(1,W-1):
            if lk[v,u] and lk[v-1:v+2,u-1:u+2].sum()-1>4: dun[v,u]=False
    return c,dun
if __name__=='__main__':
    c,lk=lijnkaart()
    img=np.full(c.shape+(3,),255,'uint8'); img[c>0]=(200,200,200); img[c==5]=(170,200,150); img[c==1]=(0,0,0); img[lk]=(200,0,0)
    Image.fromarray(img).crop((80,65,165,105)).resize((680,320),Image.NEAREST).save('/tmp/claude-0/lk.png')
    print(lk.sum())
