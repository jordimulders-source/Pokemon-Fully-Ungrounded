# kijk.py a.png [b.png ...] -> kijk.png: sprites op 8x naast het model op schaal (gedeelde geometrie), 8x
import sys, numpy as np; from PIL import Image
from reductie_gedeeld import P, X0M,X0S,Y0M,Y0S
def model_op_schaal(pad='../r3/gemini_r3_lijf.png',n=64):
    a=Image.open(pad).convert('RGB')
    # sprite (0,0) = model (X0M-X0S*P, Y0M-Y0S*P); 64 px = 64P modelpx
    x0=X0M-X0S*P; y0=Y0M-Y0S*P
    W=Image.new('RGB',(1600,1600),'white'); W.paste(a,(int(round(-x0))+400,int(round(-y0))+400))
    c=W.crop((400,400,400+int(round(64*P)),400+int(round(64*P))))
    return c.resize((n,n),Image.LANCZOS)
def sprite(p,bg=(255,255,255)):
    im=Image.open(p); o=np.asarray(im).astype(int); pal=np.array(im.getpalette()[:48]).reshape(-1,3)
    img=np.zeros((64,64,3),'uint8'); img[:]=bg
    for k in range(1,16): img[o==k]=pal[k]
    return Image.fromarray(img)
if __name__=='__main__':
    ps=[sprite(p).resize((512,512),Image.NEAREST) for p in sys.argv[1:]]+[model_op_schaal(n=512)]
    W=Image.new('RGB',(len(ps)*520,512),'white')
    for i,p in enumerate(ps): W.paste(p,(i*520,0))
    W.save('kijk.png')
