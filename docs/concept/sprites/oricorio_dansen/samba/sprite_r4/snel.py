# snelle kijk: raster (npy) op 4x en 1x (wit en gevechtsgroen) naast het model op dezelfde schaal
import numpy as np, sys, json; from PIL import Image
from palet import pal
o=np.load(sys.argv[1]); P=pal('gen3'); z=int(sys.argv[3]) if len(sys.argv)>3 else 5
im=np.zeros((64,64,4),'uint8')
for k,c in enumerate(P):
    if k: im[o==k,:3]=c; im[o==k,3]=255
spr=Image.fromarray(im,'RGBA')
pl=json.load(open('plaats.json')); F=2.9
m=Image.open('../model/gemini_r10.png').convert('RGB')
# model-uitsnede die overeenkomt met het 64x64-vak: spritepixel X <- natief (X-dx)*F+OX -> modelpx *5.12
def mp(v,d,o0): return ((v-d)*F+o0)*5.12+2.08-2.56
x0=mp(0,pl['dx'],0.97); y0=mp(0,pl['dy'],0); s=F*5.12*64
mc=m.crop((int(x0),int(y0),int(x0+s),int(y0+s))).resize((64*z,64*z),Image.LANCZOS)
W=Image.new('RGB',(64*z*2+20+3*70,64*z),'white')
b=Image.new('RGB',(64*z,64*z),'white'); b.paste(spr.resize((64*z,64*z),Image.NEAREST),(0,0),spr.resize((64*z,64*z),Image.NEAREST))
W.paste(b,(0,0)); W.paste(mc,(64*z+10,0))
for i,bg in enumerate([(255,255,255),(152,208,160),(40,40,48)]):
    t=Image.new('RGB',(64,64),bg); t.paste(spr,(0,0),spr); W.paste(t,(64*z*2+20+i*70,0))
W.save(sys.argv[2])
