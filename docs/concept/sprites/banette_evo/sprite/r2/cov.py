# dekking per spritepixel van een modelklasse: python3 cov.py klasse x0 y0 x1 y1
import sys,numpy as np; from PIL import Image
a=np.asarray(Image.open('../../model/model.png').convert('RGB')).astype(int); L=a.sum(2)/3; sat=a.max(2)-a.min(2)
K={'donker':(L<95)&(sat<45),'zwart':L<40,'rood':(a[...,0]-np.maximum(a[...,1],a[...,2])>40),'grijs':(sat<30)&(L>=95)&(L<200),
   'blauw':(a[...,2]-a[...,0]>12),'licht':a.min(2)<235}[sys.argv[1]]
x0,y0,x1,y1=[int(v) for v in sys.argv[2:6]]; S=968/62
print('    '+''.join('%x'%(i%16) for i in range(x0,x1)))
out=np.zeros((64,64))
for j in range(y0,y1):
    s=''
    for i in range(x0,x1):
        xa,ya=24+(i-1)*S,1+(j-4)*S; blk=K[max(int(round(ya)),0):int(round(ya+S)),max(int(round(xa)),0):int(round(xa+S))]
        c=blk.mean() if blk.size else 0; out[j,i]=c; s+=' ' if c<0.05 else str(min(9,int(c*10)))
    print('%3d '%j+s)
np.save('/tmp/claude-0/cov_%s.npy'%sys.argv[1],out)
