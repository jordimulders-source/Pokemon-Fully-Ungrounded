# Opslaan/tonen (geen neveneffecten).
import numpy as np; from PIL import Image; import gemeen as g
def opslaan(idx,pad,pal=g.PAL):
    im=Image.fromarray(idx.astype('uint8'),'P'); p=[c for rgb in pal for c in rgb]; im.putpalette(p+[0]*(768-len(p)))
    im.save(pad,transparency=0); return im
def rgb(idx,pal=g.PAL,bg=(255,255,255)):
    P=np.array(pal,'uint8'); o=P[idx].copy(); o[idx==0]=bg; return Image.fromarray(o,'RGB')
