import sys
sys.path.insert(0,'../k1'); sys.path.insert(0,'../k5')
from gereedschap import *
from clusters import tel
from PIL import Image
a14,p14=laad('../k14/tempel.png'); a,p=laad('tempel.png')
im=Image.open('tempel.png'); o=[]
o.append('modus %s, transparantie-index %s, kleuren gebruikt %d'%(im.mode,im.info.get('transparency'),len(np.unique(a))))
o.append('palet gelijk aan k14: %s'%(p==p14))
al=((a!=0)!=(a14!=0)); ys,xs=np.nonzero(al)
o.append('alpha gewijzigd: %d px (%d weg, %d erbij), bereik x%d-%d y%d-%d'%(al.sum(),((a14!=0)&(a==0)).sum(),((a14==0)&(a!=0)).sum(),xs.min(),xs.max(),ys.min(),ys.max()))
z=np.zeros(a.shape,bool); z[0:11,30:47]=True
o.append('alpha buiten x30-46 y0-10: %d'%(al&~z).sum())
d=(a!=a14); bz=np.zeros(a.shape,bool); bz[0:15,30:47]=True
o.append('pixels gewijzigd totaal: %d; buiten x30-46 y0-14: %d'%(d.sum(),(d&~bz).sum()))
for (x0,y0,x1,y1) in OGEN: o.append('oog x%d-%d y%d-%d diff: %d'%(x0,x1,y0,y1,d[y0:y1+1,x0:x1+1].sum()))
o.append('gewijzigde px: '+', '.join('(%d,%d) %x->%s'%(x,y,a14[y,x],'.' if a[y,x]==0 else '%x'%a[y,x]) for y,x in zip(*np.nonzero(d))))
for c in (4,8):
    n14,_=tel('../k14/tempel.png',0,c); n15,l=tel('tempel.png',0,c)
    o.append('clusters <3 px hele sprite (%d-samenhang): k14 %d | k15 %d'%(c,n14,n15))
_,l14=tel('../k14/tempel.png',0,4); _,l15=tel('tempel.png',0,4)
s14={(c,tuple(sorted(q))) for c,q in l14}
o.append('nieuwe kleine clusters (4-samenhang): '+str([(int(c),q) for c,q in l15 if (c,tuple(sorted(q))) not in s14]))
open('bewijs.txt','w').write('\n'.join(o)+'\n'); print('\n'.join(o))
