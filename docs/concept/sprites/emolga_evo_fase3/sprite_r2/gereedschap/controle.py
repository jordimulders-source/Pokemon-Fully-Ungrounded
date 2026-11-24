# controle.py: technische checks (kleuren, losse pixels, kleine clusters, losse zwarte pixels binnen een vlak, maat)
import sys; sys.path.insert(0,'/home/user/Pokemon-Fully-Ungrounded/docs/concept/sprites/emolga_evo_fase3/sprite_r1/gereedschap')
from fv import *; import palet
def rapport(pad):
    im=Image.open(pad); o=np.asarray(im).astype(int)
    ks=sorted(set(o.ravel().tolist())); yy,xx=np.where(o>0)
    print(pad.split('/')[-1],im.mode,im.size,'| indices',ks,'n=',len(ks),'| bbox x%d-%d y%d-%d (%dx%d)'%(xx.min(),xx.max(),yy.min(),yy.max(),xx.max()-xx.min()+1,yy.max()-yy.min()+1),
          '| fig px',len(yy))
    los=[]; klein=[]
    for v in range(2,16):
        lab,n=label(o==v)
        for i in range(1,n+1):
            m=lab==i; k=m.sum()
            if k==1: y_,x_=np.argwhere(m)[0]; los.append((int(x_),int(y_),palet.CH[v]))
            elif k==2: klein.append([(int(x_),int(y_),palet.CH[v]) for y_,x_ in np.argwhere(m)])
    zw=[]
    for y_,x_ in zip(*np.where(o==1)):
        nb=o[max(0,y_-1):y_+2,max(0,x_-1):x_+2]
        if (nb==1).sum()==1 and not (nb==0).any(): zw.append((int(x_),int(y_)))
    print('  losse tintpixels (1 px):',los); print('  clusters 2 px:',klein); print('  losse zwarte pixels:',zw)
if __name__=='__main__':
    for p in sys.argv[1:]: rapport(p)
