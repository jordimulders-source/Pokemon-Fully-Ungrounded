# Per spritepixel de meest voorkomende paletletter in de modelcel (gewogen), naast de huidige sprite. Gebruik: meerderheid.py sprite x0 y0 x1 y1
import sys,numpy as np; from PIL import Image
a=np.asarray(Image.open('natief.png').convert('RGB')).astype(int)
P=np.array(Image.open('r1/kaal.png').getpalette()[:36]).reshape(-1,3); P[0]=(255,255,255); ch='.#abcdGHIstu'
S=np.asarray(Image.open(sys.argv[1]))
o=np.load('r1/kaal.npy'); yy,xx=np.where(o>0); oy0,ox0=yy.min(),xx.min(); hh=yy.max()-oy0+1; ww=xx.max()-ox0+1
top=63-hh; fx=(64-ww)//2; s=1.75; NY0,NX0=8+0.4,16+0.6
q=((a[...,None,:]-P[None,None])**2).sum(-1).argmin(-1)
def wts(lo,hi,n):
    w=np.zeros(n)
    for k in range(int(np.floor(lo)),int(np.ceil(hi))):
        if 0<=k<n: w[k]=min(hi,k+1)-max(lo,k)
    return w
X0,Y0,X1,Y1=map(int,sys.argv[2:6])
print('    model'+' '*(X1-X0-3)+'   sprite')
for sy in range(Y0,Y1+1):
    r=''
    for sx in range(X0,X1+1):
        ly=NY0+(sy-top+oy0)*s; lx=NX0+(sx-fx+ox0)*s
        w=wts(ly,ly+s,100)[:,None]*wts(lx,lx+s,100)[None,:]
        st=[(w*(q==t)).sum() for t in range(12)]; r+=ch[int(np.argmax(st))]
    print('%2d  %s   %s'%(sy,r,''.join(ch[v] for v in S[sy,X0:X1+1])))
