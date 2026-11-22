# Indexraster <-> tekst. Tekens per paletindex:
CH='.#kdgwPpqLliYyEe'
import numpy as np,sys
def to_txt(a): return '\n'.join(''.join(CH[v] for v in r) for r in a)
def from_txt(s): return np.array([[CH.index(c) for c in r] for r in s.strip('\n').split('\n')])
if __name__=='__main__':
    a=np.loadtxt(sys.argv[1],dtype=int); r0,r1=(int(sys.argv[2]),int(sys.argv[3])) if len(sys.argv)>3 else (0,64)
    print('    '+''.join(str(c//10) for c in range(64))); print('    '+''.join(str(c%10) for c in range(64)))
    for r in range(r0,r1): print(f'{r:3d} '+''.join(CH[v] for v in a[r]))
