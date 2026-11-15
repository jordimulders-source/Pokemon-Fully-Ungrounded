# Basis-bruin onder de huidige patronen van r11 terughalen: patroonpixels (lila 6/7/8, creme b) buiten kop/staartband
# krijgen iteratief de meest voorkomende bruintint van hun niet-patroonburen (8-buren, daarna 5x5).
import numpy as np
from PIL import Image
R11='../r11/welp_r11.png'
def laad(f=R11): return np.array(Image.open(f))
PAT=[6,7,8,11]; BRUIN=[3,4,5,14]
def basis(a):
    b=a.copy(); todo=np.isin(a,PAT)
    todo[:26,:]=False if False else todo[:26,:]  # voorhoofd telt mee
    for it in range(20):
        nieuw=b.copy(); ch=0
        for y,x in zip(*np.where(todo)):
            for r in (1,2,3):
                w=b[max(0,y-r):y+r+1,max(0,x-r):x+r+1].ravel(); w=w[np.isin(w,BRUIN)]
                if len(w): break
            if len(w):
                v=np.bincount(w,minlength=16); nieuw[y,x]=v.argmax(); todo[y,x]=False; ch+=1
        b=nieuw
        if not todo.any(): break
    return b
if __name__=='__main__':
    a=laad(); b=basis(a); np.save('basis.npy',b)
    f=np.load('../r6/facet.npy'); F=np.full((64,64),-1); F[18:63,7:57]=f
    for y in range(17,63):
        print('%2d '%y+''.join('.' if b[y,x]==0 else '%x'%b[y,x] for x in range(5,60))+'   '+''.join('.' if F[y,x]<0 else 'SMLH'[F[y,x]] for x in range(5,60)))
