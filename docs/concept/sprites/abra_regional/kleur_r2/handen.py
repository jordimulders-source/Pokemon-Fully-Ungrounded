# handen.py: in de handenzone per spritepixel EEN modelpixel uit het 2x2-blok overnemen (fase dy,dx), i.p.v. meerderheid.
# Gebruik: python3 handen.py -> vier varianten naast elkaar (scratchpad) om de fase per hand te kiezen.
import numpy as np; from PIL import Image
from auto import nat,nlum,nbg,ndrk,PAL,K,P1,P2,P3,S2,S,M,B,H
def tint(l):
    for th,c in ((35,K),(60,P1),(80,P2),(102,P3),(122,S2),(146,S),(170,M),(195,B)):
        if l<th: return c
    return H
def neem(x,y,dy,dx):
    ny,nx=2*y-14+dy,2*x-1+dx
    return 0 if nbg[ny,nx] else tint(nlum[ny,nx])
if __name__=='__main__':
    base=np.array(Image.open('auto.png')).astype(int)
    X0,X1,Y0,Y1=17,41,42,59; Z=16; ims=[]
    for dy in (0,1):
        for dx in (0,1):
            o=base.copy()
            for y in range(Y0,Y1):
                for x in range(X0,X1): o[y,x]=neem(x,y,dy,dx)
            rgb=np.array([PAL[v] if v else (255,255,255) for v in o.ravel()]).reshape(64,64,3).astype('uint8')
            ims.append(Image.fromarray(rgb).crop((X0-3,Y0-3,X1+3,Y1+3)).resize(((X1-X0+6)*Z,(Y1-Y0+6)*Z),Image.NEAREST))
    v=Image.new('RGB',(ims[0].width*2+10,ims[0].height*2+10),'red')
    for k,im in enumerate(ims): v.paste(im,((k%2)*(im.width+10),(k//2)*(im.height+10)))
    v.save('/tmp/claude-0/-home-user-Pokemon-Fully-Ungrounded/e768f5de-0252-58bb-8bc9-76aca5f6423c/scratchpad/handen4.png')
