# Basis voor c1: p8 met de lijfpatronen (lila 6/7/8, creme 9/11) eruit; die pixels krijgen de meest voorkomende
# bruintint van hun niet-patroonburen (zoals p1/basis.py, maar op p8). Oog/tanden (zone OOG) blijven onaangeroerd.
import numpy as np
from PIL import Image
P8='../p8/welp_p8.png'
PAT=[6,7,8,9,11]; BRUIN=[3,4,5]
def p8(): return np.array(Image.open(P8))
def bevroren_kop():
    """Oog, neus, mond, tanden, tong, poot-aan-mond: rechthoeken waar NIETS verandert."""
    z=np.zeros((64,64),bool)
    z[26:30,9:24]=True   # oog-rij incl. oogwit/iris (rij 27-29)
    z[30:42,8:22]=True   # snuit, neus, mond, tanden, tong
    return z
def basis():
    a=p8(); b=a.copy(); K=bevroren_kop()
    todo=np.isin(a,PAT)&~K
    for it in range(30):
        nieuw=b.copy()
        for y,x in zip(*np.where(todo)):
            for r in (1,2,3):
                w=b[max(0,y-r):y+r+1,max(0,x-r):x+r+1]; m=todo[max(0,y-r):y+r+1,max(0,x-r):x+r+1]
                w=w[(~m)&np.isin(w,BRUIN)]
                if len(w): break
            if len(w): nieuw[y,x]=np.bincount(w,minlength=16).argmax(); todo[y,x]=False
        b=nieuw
        if not todo.any(): break
    return b
if __name__=='__main__':
    b=basis(); np.save('basis.npy',b)
    print('    '+''.join(str(x//10) for x in range(4,60))); print('    '+''.join(str(x%10) for x in range(4,60)))
    for y in range(17,63): print('%2d  '%y+''.join('.' if b[y,x]==0 else '%x'%b[y,x] for x in range(4,60)))
