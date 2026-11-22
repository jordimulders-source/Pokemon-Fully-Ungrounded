# Palpaca r3: kleur-/schaduwronde met de hand als tekstraster (kolom 0 = x 14, rij = y). Silhouet = r2 (alfa-diff 0, gecontroleerd).
# Rijen die hier niet staan blijven exact r2 (oren, kwastjes, handschoenen, verre achterpoot, onderste hoefjes).
# Variant B: verre oog op de modelplek (x18, y26-27), zie NOTITIES.md.
import numpy as np; from PIL import Image
R2='../../r2/palpaca.png'
src=np.array(Image.open(R2))
NEW={
18:'...a4e4422266664ee1',
19:'...aa2222233344eee1',
20:'..a9222223333344ee91',
21:'..192223333333444981',
22:'...632234322343445881',
23:'...64334343343445111',
24:'...634433344334451',
25:'....62333333334451',
26:'....623333213334451',
27:'....623333113334451',
28:'...6223333663334451',
29:'...645333311334451',
30:'...643333333344551',
31:'...15535333344551',
32:'....1114433445551',
33:'.......154444451............661',
34:"........64323341..........662231",
35:".......622333341.........6222341",
36:"........62333ee1.........6233341",
37:"........1dedcd111....61.63443341",
38:"........64455432266662262233344 1".replace(' ',''),
39:'.......6223322222222223333334451',
40:'.......6223332223222233333344551',
41:'.......622333323332233333444551',
42:'.......62333333333333333334451',
43:'.......62333333333333333444451',
44:'.......63333333333333333444451',
45:'......64333333333333334444455f1',
46:'....662254433333443332234455bf1',
47:'...622335444522334445233455b1f1',
48:'...62333455453333445533451bbfb1',
49:"...633344515533334453334451ffb1",
50:"...6334d11.11233345114434 51ffbb1".replace(' ',''),
51:"...aeeed1....6233 41..14445111bbb1".replace(' ',''),
52:"...1dcdc91...62334 1...6341...1bb1".replace(' ',''),
53:"....a88991....6341....6341....1bb1",
54:"....a888991...a341....631.....6bb1",
55:"....1888991..aeee1...6341.....1bb1",
}
def maak(B=False):
    a=src.copy()
    for y,row in NEW.items():
        for c,ch in enumerate(row):
            if ch=='.': continue
            a[y,14+c]=int(ch,16)
    if B:  # verre oog: model (18,26) donker 0,78 en (18,27) 0,56 (lum<120), zie NOTITIES
        a[26,18]=1; a[27,18]=1
    return a
pal=[]
for l in open('../normal.pal').read().split('\n')[3:19]: pal+= [int(v) for v in l.split()]
for B,naam in ((False,'palpaca'),(True,'palpaca_B')):
    a=maak(B)
    d=((a>0)!=(src>0)).sum(); assert d==0, ('alfa-diff',d)
    for y,row in NEW.items():
        n=len(row.rstrip('.')); m=np.nonzero(src[y])[0]
        assert 14+n-1==m.max(), ('rijlengte',y,14+n-1,m.max())
    im=Image.fromarray(a.astype('uint8'),'P'); im.putpalette(pal); im.save('../%s.png'%naam,transparency=0)
    print(naam,'alfa-diff 0, kleuren',len(np.unique(a)),'anders dan r2',(a!=src).sum())
