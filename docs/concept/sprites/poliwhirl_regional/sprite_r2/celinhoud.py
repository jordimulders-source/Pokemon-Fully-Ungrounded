# Per cel de samenstelling uit modelpixels: Z zwart(L<45) G donkergrijs(45-110,grijs) W wit(L>225) I ijs Y geel y donkergeel R rood .
# python3 celinhoud.py c0 c1 r0 r1  -> per cel de twee grootste klassen met percentage/10
import sys, numpy as np; from PIL import Image
z=np.load('reductie.npz'); xs,ys=z['xs'],z['ys']
a=np.asarray(Image.open('../referenties/gemini_gekozen_v1.png').convert('RGB')).astype(int)
R,G,B=a[...,0],a[...,1],a[...,2]; L=(R*299+G*587+B*114)/1000; sat=a.max(2)-a.min(2)
k=np.full(L.shape,'.',dtype='<U1')
k[(L<45)]='Z'; k[(L>=45)&(L<115)&(sat<40)]='G'
k[(B-R>10)&(L>=90)]='I'; k[(L>225)&(sat<40)]='W'
k[(R>140)&(G>110)&(B<120)&(R-B>50)&(L>=170)]='Y'; k[(R>120)&(G>90)&(B<100)&(R-B>40)&(L<170)]='y'
k[(R>130)&(R-G>50)&(R-B>40)]='R'
c0,c1,r0,r1=map(int,sys.argv[1:5])
print('     '+''.join('%-6d'%i for i in range(c0,c1+1)))
for j in range(r0,r1+1):
    s='%2d   '%j
    for i in range(c0,c1+1):
        blk=k[int(ys[j]):int(ys[j+1]),int(xs[i]):int(xs[i+1])].ravel()
        u,c=np.unique(blk,return_counts=True); o=np.argsort(-c); f=c/c.sum()
        t=u[o[0]]+str(min(9,int(f[o[0]]*10)))
        t+= (u[o[1]]+str(int(f[o[1]]*10))) if len(o)>1 and f[o[1]]>=0.2 else '  '
        s+=t+'  '
    print(s)
