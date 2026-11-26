# Sprite-uitsnede (12x) naast het model (zelfde schaal) en een overlay: spritelijnen (rood) over het model.
import sys, numpy as np; from PIL import Image; import kijk
def maak(sprite_png, nat, x0,y0,x1,y1, s=12):
    sp=kijk.op_wit(Image.open(sprite_png),s).crop((x0*s,y0*s,x1*s,y1*s))
    nx0=2+3*x0; ny0=2+3*(y0+2); m=Image.fromarray(nat).crop((nx0,ny0,nx0+3*(x1-x0),ny0+3*(y1-y0))).resize(sp.size,Image.NEAREST)
    a=np.asarray(Image.open(sprite_png).convert('RGB')).astype(int); idx=np.asarray(Image.open(sprite_png))
    ov=np.asarray(m).copy()
    for y in range(y0,y1):
        for x in range(x0,x1):
            if idx[y,x] in (1,2):   # zwart of lijntint
                ov[(y-y0)*s+s//2-2:(y-y0)*s+s//2+2,(x-x0)*s+s//2-2:(x-x0)*s+s//2+2]=(255,0,0)
            if idx[y,x]==0 and (y,x)!=(0,0):
                pass
    ov=Image.fromarray(ov)
    c=Image.new('RGB',(sp.width*3+20,sp.height),'white'); c.paste(sp,(0,0)); c.paste(m,(sp.width+10,0)); c.paste(ov,(2*sp.width+20,0)); return c
if __name__=='__main__':
    nat=np.asarray(Image.open(sys.argv[2])); x0,y0,x1,y1=map(int,sys.argv[4:8])
    maak(sys.argv[1],nat,x0,y0,x1,y1).save(sys.argv[3])
