# Toont een klassenraster (npy) op 8x met modelkleuren naast elkaar voor meerdere fases
import sys; from PIL import Image; import numpy as np
COL={0:(255,255,255),1:(12,14,20),2:(127,140,200),3:(96,114,176),4:(78,91,162),5:(39,61,135),6:(59,102,173),7:(71,135,194),8:(93,176,225),9:(212,234,245),10:(239,150,169),11:(148,75,92),12:(225,67,65),13:(70,182,97),14:(240,219,70)}
def img(o,z=8):
    a=np.zeros(o.shape+(3,),'uint8')
    for k,c in COL.items(): a[o==k]=c
    return Image.fromarray(a).resize((o.shape[1]*z,o.shape[0]*z),Image.NEAREST)
if __name__=='__main__':
    ims=[img(np.load(f)) for f in sys.argv[2:]]
    W=Image.new('RGB',(sum(i.width+10 for i in ims),max(i.height for i in ims)),'grey'); x=0
    for i in ims: W.paste(i,(x,0)); x+=i.width+10
    W.save(sys.argv[1])
