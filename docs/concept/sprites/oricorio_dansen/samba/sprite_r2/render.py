# npy-klassen -> png (64x64 geplaatst of ruw), index 0 transparant
import sys, numpy as np; from PIL import Image; from palet import pal
def save(o,naam,p=None):
    im=Image.fromarray(o.astype('uint8'),'P'); fl=[c for t in (p or pal()) for c in t]; im.putpalette(fl+[0]*(768-len(fl))); im.save(naam,transparency=0)
def zoom(naam,z,bg=(255,255,255)):
    im=Image.open(naam).convert('RGBA'); b=Image.new('RGB',(im.width*z,im.height*z),bg); r=im.resize(b.size,Image.NEAREST); b.paste(r,(0,0),r); return b
if __name__=='__main__':
    for f in sys.argv[1:]:
        o=np.load(f); ys,xs=np.where(o>0); save(o[ys.min():ys.max()+1,xs.min():xs.max()+1],f[:-4]+'.png')
