# bewijs: verschil r4 -> r5 per zone; buiten de genoemde zones moet het 0 zijn
import numpy as np, pickle
r4=np.loadtxt('vlieg_r4.txt',dtype=int); b4=np.loadtxt('basis_r4_zonder_verre.txt',dtype=int)
Z=pickle.load(open('zones.pkl','rb')); alle=set().union(*Z.values())
verre4={(x,y) for y,x in zip(*np.where(r4!=b4))}
for n in 'ABC':
    f=np.loadtxt(f'vlieg_r5_{n}.txt',dtype=int); basis=np.loadtxt('r5_basis_vol.txt',dtype=int)
    verre5={(x,y) for y,x in zip(*np.where(f!=basis))}
    d={(x,y) for y,x in zip(*np.where(f!=r4))}
    buiten=d-alle-verre4-verre5
    print(f'variant {n}: anders dan r4 {len(d)} px; buiten de zones: {len(buiten)}',sorted(buiten)[:10])
f=np.loadtxt('r5_basis_vol.txt',dtype=int)
for z,s in Z.items(): print(f'  {z:18s} {sum(1 for x,y in s if f[y,x]!=b4[y,x])} px anders')
print('  r4-verre poten weg:',len(verre4),'px')
