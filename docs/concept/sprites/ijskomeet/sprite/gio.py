import numpy as np
CH='KWLMDSijnvwcCrg'
def to_txt(o,fn):
    with open(fn,'w') as f:
        for row in o: f.write(''.join('.' if v<0 else CH[v] for v in row)+'\n')
def from_txt(fn):
    rows=[l.rstrip('\n') for l in open(fn)]
    return np.array([[-1 if c=='.' else CH.index(c) for c in r] for r in rows])
