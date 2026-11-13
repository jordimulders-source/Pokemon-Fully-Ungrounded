# r12b.py: rechterbovenarm duidelijker. Silhouet gelijk, binnenlijnen mogen schuiven. Zone x33-41, y27-35.
# V1: arm 3 px (x37-39) van schouder tot elleboog, eigen omlijning x36; witte front rij 29-31 1 px smaller (x34 w->o) zodat er 1 px zwart lijf (x35) blijft.
# V2: armbreedte zoals het model (q.py: arm x37-38 rij 29, x38-39 rij 30-31, x39 rij 32, x40 rij 33; lijn x37 rij 30-31), tinten lichter (a/b) voor contrast.
import pal,numpy as np
B0=[list(r) for r in pal.load('basis_r12.txt')]
V={'V1':{(34,29):'o',(35,29):'k',(36,29):'o',(37,29):'a',(38,29):'a',
         (34,30):'o',(35,30):'k',(36,30):'o',(37,30):'a',(38,30):'b',(39,30):'c',
         (34,31):'o',(35,31):'k',(36,31):'o',(37,31):'b',(38,31):'b',(39,31):'c',
         (36,32):'k',(37,32):'o',(38,32):'b',(39,32):'c',
         (36,33):'k',(37,33):'k',(38,33):'o',(39,33):'c',(40,33):'c'},
   'V2':{(37,29):'a',(38,29):'a',(38,30):'a',(39,30):'b',(38,31):'b',(39,31):'b',(39,32):'b',(40,33):'b'}}
for n,ch in V.items():
    R=[r[:] for r in B0]
    for (x,y),c in ch.items():
        if (R[y][x]=='.')!=(c=='.'): print('SILHOUET',n,x,y)
        R[y][x]=c
    R=[''.join(r) for r in R]; open(f'var_{n}.txt','w').write('\n'.join(R)+'\n'); pal.topng(R,f'var_{n}.png')
    a=np.array([list(r) for r in R]); b=np.array(B0); ys,xs=np.where(a!=b)
    print(n,len(xs),'px gewijzigd; buiten x33-41,y27-35:',[(x,y) for x,y in zip(xs,ys) if not (33<=x<=41 and 27<=y<=35)])
