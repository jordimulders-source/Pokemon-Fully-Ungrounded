# maak9.py: bouwt var_L1 (model nagemaakt) en var_L2 (vuist, voorstel), bewijst pixeldiff buiten de zone, meet alpha-diff en lijnkaart in de handzone
import subprocess,numpy as np,pal
subprocess.run(['python3','onder_L1.py'],check=True,capture_output=True)
open('var_L1.txt','w').write(open('onderlaag_L1.txt').read())
subprocess.run(['python3','l2.py','var_L2.txt'],check=True)
B=np.array([list(r) for r in pal.load('basis_r8.txt')]); d=np.load('meet5.npz'); fo,sil=d['fo'],d['sil']
for n,(x0,y0,x1,y1) in {'L1':(3,34,20,46),'L2':(3,34,20,49)}.items():
    R=pal.load(f'var_{n}.txt'); pal.topng(R,f'var_{n}.png'); A=np.array([list(r) for r in R])
    ys,xs=np.where(A!=B); buiten=[(x,y) for x,y in zip(xs,ys) if not (x0<=x<=x1 and y0<=y<=y1)]
    m=A!='.'; erbij=[(x,y) for y,x in zip(*np.where(m&~sil))]; eraf=[(x,y) for y,x in zip(*np.where(sil&~m))]
    rood=[(x,y) for y in range(y0,y1+1) for x in range(x0,x1+1) if fo[y,x]>=.3 and A[y,x]!='o' and A[y,x]!='.']
    blauw=[(x,y,round(float(d['med'][y,x].mean()))) for y in range(y0,y1+1) for x in range(x0,x1+1) if A[y,x]=='o' and fo[y,x]<.3 and sil[y,x]]
    print(f'{n}: {len(xs)} px anders dan r8, buiten x{x0}-{x1},y{y0}-{y1}: {len(buiten)}; alpha erbij {len(erbij)} eraf {len(eraf)}')
    print(f'   lijnkaart zone: rood {rood}  blauw (x,y,model-L) {blauw}')
