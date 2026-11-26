# Snel kijken: sprite 8x naast het model op dezelfde schaal (natief raster, figuur op dezelfde plek), optioneel uitsnede.
import sys, numpy as np; from PIL import Image
from gemeen import *
def model_op_schaal(breed,z=8):
    s,X0,Y0,h=schaal(breed)
    n=Image.open('natief.png').convert('RGB'); f=z*s
    big=n.resize((int(n.width*f),int(n.height*f)),Image.NEAREST)
    can=Image.new('RGB',(64*z,64*z),(255,255,255))
    can.paste(big,(int(round(X0*z-U0*f)),int(round(Y0*z-V0*f))))
    return can
def vel(pngs,breed,uit,box=None,z=8):
    ims=[Image.fromarray(rgb(np.array(Image.open(p)),(255,255,255))).resize((64*z,64*z),Image.NEAREST) for p in pngs]
    ims.append(model_op_schaal(breed,z))
    if box: ims=[i.crop(tuple(v*z for v in box)) for i in ims]
    W=sum(i.width for i in ims)+8*len(ims); can=Image.new('RGB',(W,ims[0].height),(200,200,200)); x=0
    for i in ims: can.paste(i,(x,0)); x+=i.width+8
    can.save(uit)
if __name__=='__main__':
    breed=int(sys.argv[1]); box=tuple(map(int,sys.argv[3].split(','))) if len(sys.argv)>3 else None
    z=int(sys.argv[4]) if len(sys.argv)>4 else 8
    vel(sys.argv[2].split(','),breed,'/tmp/claude-0/kijk.png',box,z)
