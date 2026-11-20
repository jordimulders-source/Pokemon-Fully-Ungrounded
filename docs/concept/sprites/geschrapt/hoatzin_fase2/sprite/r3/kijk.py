import sys,numpy as np; from PIL import Image
def rgba(p):
    im=Image.open(p); a=np.asarray(im); pal=np.array(im.getpalette()[:768]).reshape(-1,3)
    o=np.zeros(a.shape+(4,),'uint8'); o[...,:3]=pal[a]; o[...,3]=(a!=0)*255
    b=Image.new('RGBA',(64,64),'white'); b.alpha_composite(Image.fromarray(o,'RGBA')); return b.resize((512,512),Image.NEAREST)
fs=sys.argv[2:]; out=Image.new('RGB',(520*len(fs),512),'white')
for i,f in enumerate(fs): out.paste(rgba(f),(i*520,0))
out.save(sys.argv[1])
