# gedeelde export + bevriezingsbewijs (alpha-diff en kop-diff tegen r1)
import sys; sys.path.insert(0,'r1'); from pal import *
from collections import Counter
def export(g,r1,log,d='r2'):
    a=int(((g>0)!=(r1>0)).sum())
    from proef import kopmasker
    kop=int(sum(1 for y in range(0,64) for x in range(0,64) if kopmasker(x,y) and g[y,x]!=r1[y,x]))
    print('alpha-diff met r1:',a,'| pixeldiff kop (alles binnen de kopomtrek, nek omhoog):',kop)
    assert a==0 and kop==0
    np.save(d+'/'+d+'.npy',g)
    full=np.zeros((128,64),'uint8'); full[:64]=g; full[64:]=g
    im=Image.fromarray(full,'P'); flat=[]
    for c in PAL: flat+=list(c)
    im.putpalette(flat); im.save(d+'/anim_front.png',transparency=0)
    open(d+'/normal.pal','w').write('JASC-PAL\r\n0100\r\n16\r\n'+''.join('%d %d %d\r\n'%c for c in PAL))
    print(dict(Counter(z for z,*_ in log)),'totaal',len(log), '| totaal diff met r1:',int((g!=r1).sum()))
