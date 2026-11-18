import sys,numpy as np
from PIL import Image
R='/home/user/Pokemon-Fully-Ungrounded/docs/concept/sprites/viscacha/'
icon=Image.open(sys.argv[1]).convert('RGBA'); out=sys.argv[2]; lines=len(sys.argv)>3 and sys.argv[3]=='lijnen'
K=np.array(Image.open(R+'icoon/krabbel_jordi_v8.png').convert('RGB')).astype(int)
blk=K.sum(2)<60; blk[:,:430]=0; blk[:,820:]=0; ky,kx=np.nonzero(blk)
front=Image.open(R+'af/viscacha.png').convert('RGBA').crop((0,0,64,64))
def on_white(im):
    w=Image.new('RGBA',im.size,(255,255,255,255)); w.alpha_composite(im); return w
fr=on_white(front).resize((384,384),Image.NEAREST)
def panel(fr_i,ln):
    p=on_white(icon.crop((0,32*fr_i,32,32*fr_i+32))).resize((384,384),Image.NEAREST)
    if ln:
        a=np.array(p)
        for X,Y in zip(kx,ky):
            x=int((X-425)/12.94*12); y=int((Y+3)/12.9*12)+(12 if fr_i else 0)
            if 0<=x<384 and 0<=y<384: a[y,x]=(0,0,0,255)
        p=Image.fromarray(a)
    return p
W=Image.new('RGBA',(384*3+40,384),(255,255,255,255))
W.paste(fr,(0,0)); W.paste(panel(0,lines),(404,0)); W.paste(panel(1,lines),(808,0))
W.convert('RGB').save(out)
