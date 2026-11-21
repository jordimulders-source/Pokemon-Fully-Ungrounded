import numpy as np
PAL=[('.',(152,208,160)),('K',(24,22,32)),('W',(248,248,240)),('w',(220,220,208)),('v',(178,176,170)),
 ('u',(140,140,148)),('c',(204,208,220)),('b',(156,160,178)),('a',(110,112,132)),('n',(68,66,86)),
 ('y',(240,212,112)),('e',(206,168,72)),('d',(140,104,40))]
L={c:i for i,(c,_) in enumerate(PAL)}; RGB=np.array([c for _,c in PAL])
def lees(f):
    rows=[r.rstrip('\n') for r in open(f) if r.strip('\n')]; w=max(len(r) for r in rows); return np.array([list(r.ljust(w,'.')) for r in rows])
def schrijf(f,g): open(f,'w').write('\n'.join(''.join(r) for r in g)+'\n')
def rgb(g,bg=(232,232,232)):
    out=np.zeros(g.shape+(3,),'uint8')
    for c,i in L.items(): out[g==c]=RGB[i]
    out[g=='.']=bg; return out
