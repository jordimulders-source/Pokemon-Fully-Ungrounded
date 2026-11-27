import numpy as np; from PIL import Image
def rgb(lab,kl):
    H,W=lab.shape; out=np.zeros((H,W,4),'uint8')
    for j in range(H):
        for i in range(W):
            if lab[j,i]: out[j,i,:3]=kl[lab[j,i]]; out[j,i,3]=255
    return Image.fromarray(out)
def groot(im,s,bg=(255,255,255)):
    b=Image.new('RGBA',im.size,bg+(255,)); b.alpha_composite(im); return b.convert('RGB').resize((im.width*s,im.height*s),Image.NEAREST)
