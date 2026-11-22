import sys,numpy as np
CH='.#Edsml' + 'LMpYtckbw'
def dump(a):
    print('    '+''.join(str(i%10) for i in range(a.shape[1])))
    for j,row in enumerate(a): print('%3d '%j+''.join(CH[v] for v in row))
def load(path):
    rows=[l[4:] for l in open(path).read().splitlines()[1:]]
    return np.array([[CH.index(c) for c in r] for r in rows],'uint8')
if __name__=='__main__': dump(np.load(sys.argv[1]))
