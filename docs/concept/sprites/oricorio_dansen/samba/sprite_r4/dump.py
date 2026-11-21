# klassenraster (npy) -> tekst (één letter per pixel), en terug (tekst -> npy) met: dump.py naar x.npy x.txt | dump.py terug x.txt x.npy
import numpy as np, sys
LET={0:'.',1:'#',2:'a',3:'b',4:'c',5:'d',6:'y',7:'z',8:'x',9:'B',10:'C',11:'p',12:'q',13:'r',14:'w'}
INV={v:k for k,v in LET.items()}
if sys.argv[1]=='naar':
    o=np.load(sys.argv[2]); open(sys.argv[3],'w').write('\n'.join(''.join(LET[v] for v in r) for r in o)+'\n')
else:
    rows=[r for r in open(sys.argv[2]).read().split('\n') if r!='']
    assert len(rows)==64 and all(len(r)==64 for r in rows), [len(r) for r in rows]
    np.save(sys.argv[3],np.array([[INV[c] for c in r] for r in rows]))
