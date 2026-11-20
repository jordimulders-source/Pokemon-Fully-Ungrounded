PAL=[('.',(152,208,160)),('K',(16,18,26)),('a',(54,62,78)),('b',(86,98,118)),('c',(128,142,164)),
 ('g',(136,134,156)),('h',(184,182,200)),('i',(224,224,236)),('W',(250,250,252)),('n',(40,44,58)),
 ('s',(54,72,94)),('t',(122,146,168)),('u',(192,214,230)),('m',(74,82,106)),('e',(200,144,48)),('d',(128,84,28))]
L={c:i for i,(c,_) in enumerate(PAL)}
import numpy as np
RGB=np.array([c for _,c in PAL])
def lees(f):
    rows=[r.rstrip('\n') for r in open(f) if r.strip('\n')]; return np.array([list(r.ljust(38,'.')) for r in rows])
def schrijf(f,g): open(f,'w').write('\n'.join(''.join(r) for r in g)+'\n')
def rgb(g,bg=(232,232,232)):
    out=np.zeros(g.shape+(3,),'uint8')
    for c,i in L.items(): out[g==c]=RGB[i]
    out[g=='.']=bg; return out
