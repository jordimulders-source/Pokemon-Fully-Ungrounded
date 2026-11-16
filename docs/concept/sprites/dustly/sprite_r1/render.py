import sys; sys.path.insert(0,'sprite_r1'); from PIL import Image; import numpy as np; import pal
def img(idx,P,scale=1,bgc=None):
    rgb=np.array(P+[(0,0,0)]*(16-len(P)),'uint8')[idx]; al=(idx>0)
    out=np.zeros(idx.shape+(4,),'uint8'); out[...,:3]=rgb; out[...,3]=al*255
    im=Image.fromarray(out)
    if bgc is not None:
        b=Image.new('RGBA',im.size,bgc+(255,)); b.alpha_composite(im); im=b
    return im.resize((im.width*scale,im.height*scale),Image.NEAREST)
if __name__=='__main__':
    idx=np.load(sys.argv[1]); img(idx,pal.TROUW,int(sys.argv[3]),(255,255,255)).convert('RGB').save(sys.argv[2])
