# Reductie ronde 9: identiek aan r8 (natief raster, zelfde mapping, vlakgewogen per spritecel, dekking<0,5 transparant,
# zwart>=0,2 -> '#', lijn>=0,5 -> 'a', anders vlakgemiddelde -> b/c/d), maar met de klassegrenzen op de middens
# tussen de paletkleuren: zwart L<28 (tussen # 10 en a 46), donkerbruin 28<=L<54 (tussen a 46 en b 62).
# Reden: de mondholte in het model is donkerbruin (L 35-45) en werd met de r8-grens (L<45) zwart.
import numpy as np; from PIL import Image
D='/home/user/Pokemon-Fully-Ungrounded/docs/concept/sprites/mate/sprite/'
N=np.asarray(Image.open(D+'natief.png').convert('RGB')).astype(float)
P=np.array(Image.open(D+'r8/mate.png').getpalette()[:36]).reshape(-1,3).astype(float)
o=np.load(D+'r1/kaal.npy'); yy,xx=np.where(o>0); oy0,ox0=yy.min(),xx.min(); hh=yy.max()-oy0+1; ww=xx.max()-ox0+1
top=63-hh; fx=(64-ww)//2; s=1.75; NY0,NX0=8+0.4,16+0.6
L=(N*[.299,.587,.114]).sum(2); FG=N.min(2)<200; BL=FG&(L<28); LN=FG&~BL&(L<54); VL=FG&(L>=54)
GR=FG&(N[...,1]>N[...,0]+8)   # groen (yerba in de ogen)
def w(lo,hi,n):
    v=np.zeros(n)
    for k in range(int(np.floor(lo)),int(np.ceil(hi))):
        if 0<=k<n: v[k]=min(hi,k+1)-max(lo,k)
    return v
def cel(sx,sy):
    ny=NY0+(sy-top+oy0)*s; nx=NX0+(sx-fx+ox0)*s
    return w(ny,ny+s,100)[:,None]*w(nx,nx+s,100)[None,:]
def red(sx,sy,groen=False):
    W=cel(sx,sy); t=W.sum(); fg=(W*FG).sum()
    if fg/t<0.5: return 0
    if (W*BL).sum()/fg>=0.2: return 1
    if groen and (W*GR).sum()/fg>=0.4:
        v=W*GR; m=(N*v[...,None]).sum((0,1))/v.sum(); k=[6,7,8]; return k[int(((P[k]-m)**2).sum(1).argmin())]
    if (W*LN).sum()/fg>=0.5 or (W*VL).sum()==0: return 2
    v=W*VL&~GR if False else W*(VL&~GR); 
    if v.sum()==0: v=W*VL
    m=(N*v[...,None]).sum((0,1))/v.sum(); k=[3,4,5]
    return k[int(((P[k]-m)**2).sum(1).argmin())]
if __name__=='__main__':
    import sys; X0,Y0,X1,Y1=map(int,sys.argv[1:5]); g=len(sys.argv)>5; ch='.#abcdGHIstu'
    r8=np.asarray(Image.open(D+'r8/mate.png'))
    print('   '+''.join(str(x%10) for x in range(X0,X1+1)),'  r8')
    for y in range(Y0,Y1+1): print('%2d '%y+''.join(ch[red(x,y,g)] for x in range(X0,X1+1)),' '+''.join(ch[v] for v in r8[y,X0:X1+1]))
