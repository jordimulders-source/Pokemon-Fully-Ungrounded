# r8: beenstrepen rechts op dezelfde rijen als links (blauw 54, rood 55-56, blauw 57), rij 58 creme. Per pixel.
import numpy as np; from PIL import Image
KL={'.':(0,0,0),'K':(16,14,22),'1':(30,28,44),'2':(48,46,70),'3':(76,74,108),'g':(128,126,166),
    'L':(246,236,202),'M':(228,208,158),'D':(186,156,104),'S':(126,94,54),'B':(80,120,200),'b':(44,66,140),
    'R':(214,66,58),'r':(140,36,40),'W':(248,248,248),'G':(56,160,72),'H':(40,104,56)}
INV={v:k for k,v in KL.items()}
def rollen(f):
    im=Image.open(f); n=len(set(np.asarray(im).ravel())|{0}); pal=np.array(im.getpalette()[:3*16]).reshape(16,3)
    return np.array([INV.get(tuple(c),'?') for c in pal])[np.asarray(im)]
WIJZ=[((34,54),'b'),((35,54),'B'),((36,54),'B'),((37,54),'B'),((38,54),'B'),
      ((35,55),'r'),((36,55),'R'),((37,55),'R'),((38,55),'R'),
      ((35,57),'b'),((36,57),'b'),((37,57),'b'),((38,57),'b'),((39,57),'b'),
      ((35,58),'S'),((36,58),'L'),((37,58),'M'),((38,58),'M'),((39,58),'D')]
def schrijf(naam,r):
    keys=['.']+sorted(set(r.ravel())-{'.'}); assert len(keys)<=16 and '?' not in keys,keys
    im=Image.fromarray(np.vectorize(keys.index)(r).astype('uint8'),'P')
    flat=[v for k in keys for v in KL[k]]; im.putpalette(flat+[0]*(768-len(flat))); im.save(naam,transparency=0)
for v in ('P1','P2'):
    R=rollen('../sprite_r7/astro_%s.png'%v); r7=R.copy(); uit=[]
    for (x,y),c in WIJZ:
        if v=='P1' and c=='r': c='K'   # P1 heeft geen donkerrood (zelfde regel als links)
        if R[y,x]!=c: uit.append('(%d,%d) %s->%s'%(x,y,R[y,x],c)); R[y,x]=c
    schrijf('astro_%s.png'%v,R)
    d=(R!=r7); ys,xs=np.where(d)
    print(v,len(uit),'px:',', '.join(uit))
    print('  zone x %d-%d y %d-%d | alpha-diff t.o.v. r7:'%(xs.min(),xs.max(),ys.min(),ys.max()),((R=='.')!=(r7=='.')).sum(),'| kopvak:',d[6:26,23:45].sum())
    for y in range(53,60): print('  ',y,''.join(R[y,24:42]))
