# Zij-aan-zij: sprite (64x64 png) en het originele model op hetzelfde spriteraster, uitsnede in spritecoords.
import sys
from PIL import Image, ImageDraw
SRC='../../referenties/model_welp_gekozen.png'
def orig(box,z):
    m=Image.open(SRC).convert('RGBA'); k=16.896
    # spritecoord x -> arraycoord x-7, y -> y-18
    X=lambda x:99.3+(x-7)*k; Y=lambda y:191.5+(y-18)*k
    return m.crop((int(X(box[0])),int(Y(box[1])),int(X(box[2])),int(Y(box[3])))).resize(((box[2]-box[0])*z,(box[3]-box[1])*z),Image.LANCZOS)
def spr(f,box,z):
    im=Image.open(f).convert('RGBA').crop(box); bg=Image.new('RGBA',im.size,(255,255,255,255)); bg.alpha_composite(im)
    return bg.resize((im.width*z,im.height*z),Image.NEAREST)
def grid(im,box,z):
    d=ImageDraw.Draw(im)
    for i in range(box[2]-box[0]+1): d.line([(i*z,0),(i*z,im.height)],fill=(0,160,255,255) if (i+box[0])%5==0 else (150,150,150,70))
    for j in range(box[3]-box[1]+1): d.line([(0,j*z),(im.width,j*z)],fill=(0,160,255,255) if (j+box[1])%5==0 else (150,150,150,70))
    return im
if __name__=='__main__':
    box=tuple(map(int,sys.argv[1].split(','))); out=sys.argv[2]; z=int(sys.argv[3]); fs=sys.argv[4:]
    ims=[grid(spr(f,box,z),box,z) for f in fs]+[grid(orig(box,z),box,z)]
    V=Image.new('RGBA',(sum(i.width+8 for i in ims),ims[0].height),(255,255,255,255)); x=0
    for i in ims: V.alpha_composite(i,(x,0)); x+=i.width+8
    V.save(out)
