# Model per spritepixel op de lokaal gefitte schaal (uniform): lijnfractie + gemiddelde kleur zonder lijn -> dichtstbijzijnde ringtint.
import sys; sys.path.insert(0,'docs/concept/sprites/hitmonlee_regional/sprite/r14')
from uni import *
pal=np.array(Image.open(D+'eindkeuring/ek2.png').getpalette()[:48]).reshape(16,3)
def meet(sc,dy,dx,k=8):
    lum=a.mean(2); dk=(lum<80)&fig
    t=(np.arange(64*k)+.5)/k
    ny=np.floor((t-dy)/sc).astype(int); nx=np.floor((t-dx)/sc).astype(int)
    vy=(ny>=0)&(ny<148); vx=(nx>=0)&(nx<136)
    B=np.zeros((64*k,64*k)); Bc=np.zeros((64*k,64*k,3)); Bm=np.zeros((64*k,64*k))
    B[np.ix_(vy,vx)]=dk[np.ix_(ny[vy],nx[vx])]
    m=fig&~dk
    Bm[np.ix_(vy,vx)]=m[np.ix_(ny[vy],nx[vx])]
    Bc[np.ix_(vy,vx)]=a[np.ix_(ny[vy],nx[vx])]
    L=B.reshape(64,k,64,k).mean((1,3))
    w=Bm.reshape(64,k,64,k).sum((1,3))
    col=(Bc*Bm[...,None]).reshape(64,k,64,k,3).sum((1,3))/np.maximum(w,1)[...,None]
    return L,col
def naar(col,allowed):
    d=((col[...,None,:]-pal[allowed][None,None])**2).sum(-1)
    return np.array(allowed)[d.argmin(-1)]
if __name__=='__main__':
    sc,dy,dx=map(float,sys.argv[1:4]); y0,y1,x0,x1=map(int,sys.argv[4:8])
    L,col=meet(sc,dy,dx)
    T=naar(col,[15,8,7,6,5,4,3,13,14,12,11])
    e=np.array(Image.open(D+'eindkeuring/ek2.png'))
    for y in range(y0,y1):
        print('%2d '%y+''.join(('.' if e[y,x]==0 else ('#' if L[y,x]>=0.4 else ('+' if L[y,x]>=0.25 else '%x'%T[y,x]))) for x in range(x0,x1))+'   ek2 '+''.join('.' if v==0 else '%x'%v for v in e[y,x0:x1]))
