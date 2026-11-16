# IJking van Jordi's screenshot (jordi/koeienvanger_lijnen2.png, links r22) naar spritecoordinaten: schaal + offset fitten
# door r22 opgeschaald te vergelijken met de screenshot (niet-gele pixels), daarna gele lijnpixels terugrekenen.
import numpy as np; from PIL import Image
D='/home/user/Pokemon-Fully-Ungrounded/docs/concept/sprites/spooktrein_fase3/'
J=np.array(Image.open(D+'jordi/koeienvanger_lijnen2.png').convert('RGB')).astype(int)[:, :620]
im=Image.open(D+'sprite_r22/sprite.png').convert('RGBA'); S=np.array(im).astype(int)
geel=(J[...,0]>200)&(J[...,1]>170)&(J[...,2]<90)
def score(s,ox,oy):
    H,W=J.shape[:2]; ys,xs=np.mgrid[0:H:3,0:W:3]
    sx=((xs-ox)/s).astype(int); sy=((ys-oy)/s).astype(int)
    m=(sx>=0)&(sx<64)&(sy>=0)&(sy<64)&~geel[ys,xs]
    sp=S[sy[m],sx[m]]; jp=J[ys[m],xs[m]]
    wit=sp[:,3]==0
    c=np.where(wit[:,None],255,sp[:,:3])
    return np.abs(c-jp).mean()
best=None
for s in np.arange(9.3,10.2,0.05):
    for ox in np.arange(-40,20,2):
        for oy in np.arange(-10,40,2):
            v=score(s,ox,oy)
            if best is None or v<best[0]: best=(v,s,ox,oy)
v,s,ox,oy=best
for s2 in np.arange(s-0.06,s+0.07,0.02):
    for ox2 in np.arange(ox-2,ox+2.1,0.5):
        for oy2 in np.arange(oy-2,oy+2.1,0.5):
            v2=score(s2,ox2,oy2)
            if v2<best[0]: best=(v2,s2,ox2,oy2)
print('fit fout %.1f schaal %.3f offset %.1f %.1f'%best)
_,s,ox,oy=best
ys,xs=np.where(geel)
P=np.stack([(xs-ox)/s,(ys-oy)/s],1)
np.save(D+'sprite_r23/jordi_lijnen.npy',P)
cells={}
for x,y in P: cells[(int(y),int(x))]=cells.get((int(y),int(x)),0)+1
g=np.zeros((64,64),int)
for (y,x),n in cells.items(): g[y,x]=n
for y in range(40,62): print('%2d'%y,''.join('#' if g[y,x]>8 else ('+' if g[y,x] else '.') for x in range(0,30)))
