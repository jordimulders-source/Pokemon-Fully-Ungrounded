import sys; sys.path.insert(0,'/home/user/Pokemon-Fully-Ungrounded/docs/concept/sprites/spooktrein_fase3/sprite_r18')
from proj import *
def wit(im):
    im=im.convert('RGBA'); bg=Image.new('RGBA',im.size,(255,255,255,255)); bg.alpha_composite(im); return bg
def kvcrop(path,Z=12,box=(0,40,30,61)):
    return wit(Image.open(path)).crop(box).resize(((box[2]-box[0])*Z,(box[3]-box[1])*Z),Image.NEAREST)
def modelkv(Z=12,box=(0,40,30,61),DY=-1):
    nx0,ny0=s2n(box[0],box[1],DY); nx1,ny1=s2n(box[2],box[3],DY)
    c=Image.fromarray(N.astype(np.uint8)).crop((int(round(nx0)),int(round(ny0)),int(round(nx1)),int(round(ny1))))
    return c.resize(((box[2]-box[0])*Z,(box[3]-box[1])*Z),Image.NEAREST).convert('RGBA')
def rij(ims,gap=8):
    W=sum(i.size[0] for i in ims)+gap*(len(ims)-1); H=max(i.size[1] for i in ims)
    o=Image.new('RGBA',(W,H),(255,255,255,255)); x=0
    for i in ims: o.alpha_composite(i,(x,0)); x+=i.size[0]+gap
    return o
if __name__=='__main__':
    rij([kvcrop(p) for p in sys.argv[2:]]+[modelkv()]).save(sys.argv[1])
