# hulp: idx+pal -> png (8x/10x) en geindexeerde png
from PIL import Image; import numpy as np
def save_idx(L,pal,path,scale=1,bg=(255,255,255)):
    H,W=L.shape
    rgb=np.zeros((H,W,3),np.uint8); rgb[:]=bg
    for k,c in enumerate(pal):
        if k==0: continue
        rgb[L==k]=np.array(c,np.uint8)
    im=Image.fromarray(rgb)
    if scale>1: im=im.resize((W*scale,H*scale),Image.NEAREST)
    im.save(path); return im
def save_p64(L,pal,path):
    H,W=L.shape
    C=np.zeros((64,64),np.uint8)
    ox=(64-W)//2; oy=64-H
    C[oy:oy+H,ox:ox+W]=L
    im=Image.fromarray(C,'P')
    flat=[]
    for c in pal: flat+=list(c)
    flat+= [0]*(768-len(flat))
    im.putpalette(flat); im.save(path,transparency=0); return im
def lab(rgb):
    c=np.asarray(rgb,float)/255
    c=np.where(c>0.04045,((c+0.055)/1.055)**2.4,c/12.92)
    M=np.array([[0.4124,0.3576,0.1805],[0.2126,0.7152,0.0722],[0.0193,0.1192,0.9505]])
    xyz=c@M.T/np.array([0.9505,1,1.089])
    f=np.where(xyz>0.008856,np.cbrt(xyz),7.787*xyz+16/116)
    return np.stack([116*f[...,1]-16,500*(f[...,0]-f[...,1]),200*(f[...,1]-f[...,2])],-1)
