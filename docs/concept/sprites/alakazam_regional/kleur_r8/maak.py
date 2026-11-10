# maak.py: bouwt alle getoonde varianten op basis_r7.txt, schrijft var_*.txt/.png, bewijst diff 0 buiten de zones
import var,pal,numpy as np,subprocess
NAAM={'links_A':['L3'],'links_B':['L4'],'links_C':['L5b'],
      'rechts_A':['RA2'],'rechts_B':['RB2'],'rechts_C':['RC3'],
      'pupil_1px':['P1'],'pupil_2px':['P2'],
      'beste_linksA_rechtsA_pupil1':['L3','RA2','P1']}
ZONES=[(31,15,36,18),(3,37,20,45),(46,26,59,37)]   # x0,y0,x1,y1 inclusief: oog, linkerhand, rechterhand
B=np.array([list(r) for r in var.B])
def inzone(x,y): return any(x0<=x<=x1 and y0<=y<=y1 for x0,y0,x1,y1 in ZONES)
for n,keys in NAAM.items():
    R=var.build(keys); A=np.array([list(r) for r in R])
    d=[(x,y) for y,x in zip(*np.where(A!=B))]
    buiten=[p for p in d if not inzone(*p)]
    open(f'var_{n}.txt','w').write('\n'.join(R)+'\n'); pal.topng(R,f'var_{n}.png')
    print(f'{n}: {len(d)} px gewijzigd, buiten de zones: {len(buiten)} {buiten}')
