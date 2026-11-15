# Snelle vergelijking: kop 12x van varianten + model, en 1x/3x van de hele sprite. python3 snel.py out a.npy b.npy ...
import sys,numpy as np
from PIL import Image, ImageDraw
from toon6 import big
from zie import mod, F
fs=sys.argv[2:]; b=(0,0,26,24); z=12
ims=[big(np.load(f)[b[1]:b[3],b[0]:b[2]],z,F,(255,255,255,255)) for f in fs]+[mod(b,z)]
W=ims[0].width; V=Image.new('RGBA',((W+8)*len(ims),ims[0].height+12+150+10),(255,255,255,255)); d=ImageDraw.Draw(V)
for i,im in enumerate(ims): V.alpha_composite(im,(i*(W+8),12)); d.text((i*(W+8),0),(fs+['model'])[i][:40],fill=(0,0,0))
y=ims[0].height+20; x=0
for f in fs:
    a=np.load(f); one=big(a,1,F,(248,248,240,255)); V.alpha_composite(one,(x,y)); V.alpha_composite(big(a,3,F,(248,248,240,255)),(x+56,y)); x+=56+150+10
V.save(sys.argv[1])
