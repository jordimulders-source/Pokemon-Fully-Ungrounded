# vergelijk.py a.png b.png uit.png: a | b | model op 8x
import sys, numpy as np; from PIL import Image
def rgba(p):
    im=Image.open(p); a=np.asarray(im)[:64]; pal=np.array(im.getpalette()[:768]).reshape(-1,3)
    o=np.zeros(a.shape+(4,),'uint8'); o[...,:3]=pal[a]; o[...,3]=(a!=0)*255; return Image.fromarray(o,'RGBA')
s=2.8888889; x0=32; y0=8
f=lambda cx,cy:((x0+(cx-6)*s)*5.12-0.12,(y0+(cy-1)*s)*5.12-0.12)
M=Image.open('../../MODEL.png').convert('RGB'); a=f(0,0); b=f(64,64)
model=M.crop((int(a[0]),int(a[1]),int(b[0]),int(b[1]))).resize((512,512),Image.LANCZOS).convert('RGBA')
W=Image.new('RGBA',(3*520,512),(255,255,255,255))
for i,p in enumerate(sys.argv[1:3]):
    w=Image.new('RGBA',(512,512),(255,255,255,255)); w.alpha_composite(rgba(p).resize((512,512),Image.NEAREST)); W.paste(w,(i*520,0))
W.paste(model,(1040,0)); W.save(sys.argv[3])
