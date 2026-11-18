# blauwe klasse per spritepixel (Shuppets): . wit, k zwart, n marine, B donker, M mid, L licht, c iris (cyaan), w glans
import sys,numpy as np; from PIL import Image
a=np.asarray(Image.open('../../model/model.png').convert('RGB')).astype(float); S=968/62
x0,y0,x1,y1=[int(v) for v in sys.argv[1:5]]
def cl(m,kf):
    r,g,b=m; L=(r+g+b)/3
    if L>225 and kf<.2: return '.'
    if kf>.45: return 'k'
    if g-r>12 and L>120: return 'w' if L>200 else 'c'
    if L<85: return 'n'
    if L<118: return 'B'
    if L<150: return 'M'
    return 'L'
print('   '+''.join(str(i%10) for i in range(x0,x1)))
for j in range(y0,y1):
    s=''
    for i in range(x0,x1):
        xa,ya=24+(i-1)*S,1+(j-4)*S; b=a[int(round(ya)):int(round(ya+S)),int(round(xa)):int(round(xa+S))].reshape(-1,3)
        bb=b[b.sum(1)/3<235]; kf=((b.sum(1)/3)<50).mean()
        s+=cl(bb.mean(0) if len(bb)>len(b)*.3 else b.mean(0),kf)
    print('%2d '%j+s)
