# mondmasker: spritepixel = band als >=50% van het modelblok helderheid < 75. python3 mask.py x0 y0 x1 y1 [thr] [Lthr]
import sys,numpy as np; from PIL import Image
a=np.asarray(Image.open('../../model/model.png').convert('RGB')).astype(float); S=968/62
def frac(i,j,L=75):
    xa,ya=24+(i-1)*S,1+(j-4)*S; b=a[max(0,int(round(ya))):int(round(ya+S)),max(0,int(round(xa))):int(round(xa+S))].reshape(-1,3)
    return ((b.sum(1)/3)<L).mean()
if __name__=='__main__':
    x0,y0,x1,y1=[int(v) for v in sys.argv[1:5]]; t=float(sys.argv[5]) if len(sys.argv)>5 else .5
    print('   '+''.join(str(i%10) for i in range(x0,x1)))
    for j in range(y0,y1):
        print('%2d '%j+''.join(('#' if frac(i,j)>=t else ('+' if frac(i,j)>=.25 else '.')) for i in range(x0,x1)))
