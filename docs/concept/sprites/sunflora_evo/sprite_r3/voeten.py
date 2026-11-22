# Mechanische voetbewerking op r12 (vóór de verkleining): voeten = r12-pixels onder y=792, links x<560, rechts x>=560.
# Elk blok draait om zijn bovenmidden (aanhechting) met NEAREST; origineel weg, gedraaid blok terug. Niets getekend.
# Gebruik: voeten.py hoekL hoekR uit.png   (graden, PIL-richting: + = tegen de klok in)
import sys, numpy as np; from PIL import Image
aL,aR,OUT=float(sys.argv[1]),float(sys.argv[2]),sys.argv[3]
im=Image.open('../gemini/r12.png').convert('RGB'); a=np.array(im)
nw=a.astype(int).sum(2)<720; Y0=792
base=a.copy(); feet=np.zeros_like(nw); feet[Y0:]=nw[Y0:]
base[feet]=255
res=Image.fromarray(base)
for side,ang in (('L',aL),('R',aR)):
    m=feet.copy()
    if side=='L': m[:,560:]=False
    else: m[:,:560]=False
    ys,xs=np.where(m[Y0:Y0+4]); px,py=xs.mean(),Y0
    rgba=np.zeros((1024,1024,4),'uint8'); rgba[...,:3]=a; rgba[...,3]=m*255
    r=Image.fromarray(rgba).rotate(ang,resample=Image.NEAREST,center=(px,py))
    res.paste(r,(0,0),r)
res.save(OUT)
