# codes -> 8x png (voor bekijken)
import sys; import numpy as np; from PIL import Image
COL={0:(255,255,255),1:(24,20,16),2:(250,236,150),3:(238,206,86),4:(210,164,52),5:(232,82,58),6:(178,42,34),
7:(200,130,72),8:(186,96,44),9:(123,41,8),10:(180,180,172),11:(64,64,72),12:(156,82,0),13:(98,49,8),14:(240,232,184),16:(255,255,255),17:(98,49,8),18:(124,124,128)}
def img(o,s=8):
    h,w=o.shape; a=np.zeros((h,w,3),'uint8')
    for k,c in COL.items(): a[o==k]=c
    return Image.fromarray(a).resize((w*s,h*s),0)
if __name__=='__main__':
    ims=[img(np.load(f)) for f in sys.argv[2:]]
    W=sum(i.width+8 for i in ims); H=max(i.height for i in ims); out=Image.new('RGB',(W,H),(128,128,128)); x=0
    for i in ims: out.paste(i,(x,0)); x+=i.width+8
    out.save(sys.argv[1])
