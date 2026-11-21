# Toont klassenrasters (npy) op 8x met modelkleuren naast elkaar. Ook model_L: modelhelderheid per spritepixel.
import sys; from PIL import Image; import numpy as np
COL={0:(255,255,255),1:(2,2,4),2:(89,92,99),3:(66,68,74),4:(56,57,62),5:(42,43,48),6:(31,32,36),7:(158,78,93),8:(149,41,60),9:(90,20,30),10:(240,160,172),11:(200,108,123),12:(130,60,75),13:(252,252,252),14:(110,112,122)}
def img(o,z=8):
    a=np.zeros(o.shape+(3,),'uint8')
    for k,c in COL.items(): a[o==k]=c
    return Image.fromarray(a).resize((o.shape[1]*z,o.shape[0]*z),Image.NEAREST)
if __name__=='__main__':
    ims=[img(np.load(f)) for f in sys.argv[2:]]
    W=Image.new('RGB',(sum(i.width+10 for i in ims),max(i.height for i in ims)),'grey'); x=0
    for i in ims: W.paste(i,(x,0)); x+=i.width+10
    W.save(sys.argv[1])
