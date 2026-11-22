# per spritepixel modelklasse: '.' wit, 'k' zwart, 'b' donkerbruin, grijs l/m/d naar helderheid, rood r/R, 'B' blauw. python3 mch.py x0 y0 x1 y1 [thr]
import sys,numpy as np; from PIL import Image
a=np.asarray(Image.open('../../model/model.png').convert('RGB')).astype(float); S=968/62
x0,y0,x1,y1=[int(v) for v in sys.argv[1:5]]; thr=float(sys.argv[5]) if len(sys.argv)>5 else .4
def cl(p):
    r,g,b=p; L=(r+g+b)/3
    if L>235: return '.'
    if L<50: return 'k'
    if r-g>60: return 'r' if r>185 else 'R'
    if b-r>25: return 'B'
    if L<95: return 'b'
    return 'l' if L>160 else ('m' if L>120 else 'd')
print('   '+''.join(str(i%10) for i in range(x0,x1)))
for j in range(y0,y1):
    s=''
    for i in range(x0,x1):
        xa,ya=24+(i-1)*S,1+(j-4)*S; b=a[max(0,int(round(ya))):int(round(ya+S)),max(0,int(round(xa))):int(round(xa+S))].reshape(-1,3)
        cs=[cl(p) for p in b]; from collections import Counter; C=Counter(cs)
        if C['k']/len(cs)>=thr: s+='k'
        else: s+=C.most_common(1)[0][0]
    print('%2d '%j+s)
